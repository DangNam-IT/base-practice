import math

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.service.crud_authors import  get_author_by_name, get_author_by_id, get_authors, create_new_author, update_current_author, delete_current_author, get_book_count
from app.database import get_db
from app.security import require_admin
from app.models.author import Author
from app.models.user import User
from app.schemas.books import PaginatedResponse
from app.schemas.authors import AuthorBase, AuthorResponse, AuthorUpdate

router = APIRouter(prefix="/authors", tags=["Authors"])


# ── Helper ────────────────────────────────────────────────

def _get_or_404(author_id, db: Session) -> Author:
    author = get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tác giả không tồn tại")
    return author


# ── Endpoints ─────────────────────────────────────────────

@router.get(
    "/",
    response_model=PaginatedResponse[AuthorResponse],
    summary="Danh sách tác giả (có search + filter)",
)
def list_authors(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    search: str = Query(default=None, description="Tìm theo tên tác giả"),
    db: Session = Depends(get_db),
):
    items, total = get_authors(
        db, page=page, 
        page_size=page_size,
        search=search,
    )
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total else 0,
    )


@router.get(
    "/{author_id}",
    response_model=AuthorResponse,
    summary="Chi tiết tác giả",
)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = _get_or_404(author_id, db)
    return author


@router.post(
    "/",
    response_model=AuthorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="[Admin] Tạo tác giả mới",
)
def create_author(
    author_in: AuthorBase,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    # Kiểm tra tên trùng
    if get_author_by_name(db, author_in.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tác giả '{author_in.name}' đã tồn tại",
        )
    return create_new_author(db, author_in)


@router.put(
    "/{author_id}",
    response_model=AuthorResponse,
    summary="[Admin] Cập nhật tác giả",
)
def update_author(
    author_id: int,
    author_in: AuthorUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    author = _get_or_404(author_id, db)

    # Kiểm tra tên mới có trùng với author khác không
    if author_in.name and author_in.name != author.name:
        existing = get_author_by_name(db, author_in.name)
        if existing and existing.id != author_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tên '{author_in.name}' đã được dùng bởi tác giả khác",
            )

    return update_current_author(db, author, author_in)


@router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="[Admin] Xóa tác giả",
)
def delete_author(
    author_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    author = _get_or_404(author_id, db)
    book_count = get_book_count(db, author_id)
    if book_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Không thể xóa: tác giả đang có {book_count} cuốn sách. Xóa sách trước hoặc dùng ?force=true",
        )
    delete_current_author(db, author)


@router.delete(
    "/{author_id}/force",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="[Admin] Xóa tác giả + toàn bộ sách liên quan",
)
def force_delete_author(
    author_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """Cascade delete: xóa author sẽ xóa tất cả books của author đó."""
    author = _get_or_404(author_id, db)
    delete_current_author(db, author)