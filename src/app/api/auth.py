from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models import user
from app.schemas import users, tokens
from app.database import get_db
from app.security import create_access_token, get_current_active_user, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=users.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản mới",
)
def register(user_in: users.UserCreate, db: Session = Depends(get_db)):
    # Kiểm tra username trùng
    if db.query(user.User).filter(user.User.username == user_in.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username đã tồn tại",
        )

    new_user = user.User(
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post(
    "/login",
    response_model=tokens.Token,
    summary="Đăng nhập, nhận JWT token",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Sử dụng form `username` + `password` (chuẩn OAuth2).
    Swagger UI sẽ tự render form này trong nút Authorize.
    """
    user_db = db.query(user.User).filter(user.User.username == form_data.username).first()

    if not user_db or not verify_password(form_data.password, user_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai username hoặc password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user_db.username, "role": user_db.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=users.UserResponse,
    summary="Xem thông tin tài khoản hiện tại",
)
def get_me(current_user: user.User = Depends(get_current_active_user)):
    return current_user