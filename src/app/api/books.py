import math

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.service import crud_authors, crud_books
from app.database import get_db
from app.security import require_admin
from app.models import user, book
from app.schemas import books


router = APIRouter(prefix="/books", tags=["Books"])


# ── Helper ────────────────────────────────────────────────

def _get_or_404(book_id: int, db: Session) -> book.Book:
    book = crud_books.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sách không tồn tại")
    return book


# ── Endpoints ─────────────────────────────────────────────

@router.get(
    "/",
    response_model= books.PaginatedResponse[books.BookResponse],
    summary="Danh sách sách (search + filter)",
)
def list_books(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    search: str = Query(default=None, description="Tìm theo tiêu đề"),
    author_id: int = Query(default=None, description="Lọc theo tác giả"),
    db: Session = Depends(get_db),
):
    # Nếu filter theo author_id thì kiểm tra author có tồn tại không
    if author_id is not None and not crud_authors.get_author_by_id(db, author_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tác giả không tồn tại")

    items, total = crud_books.get_books(
        db,
        page=page,
        page_size=page_size,
        search=search,
        author_id=author_id,
    )
    return books.PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total else 0,
    )


@router.get(
    "/{book_id}",
    response_model=books.BookResponse,
    summary="Chi tiết sách",
)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return _get_or_404(book_id, db)


@router.post(
    "/",
    response_model=books.BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="[Admin] Tạo sách mới",
)
def create_book(
    book_in: books.BookCreate,
    db: Session = Depends(get_db),
    _admin: user.User = Depends(require_admin),
):
    # Kiểm tra author tồn tại
    if not crud_authors.get_author_by_id(db, book_in.author_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tác giả id={book_in.author_id} không tồn tại",
        )

    # Kiểm tra ISBN trùng
    if book_in.isbn and crud_books.get_book_by_isbn(db, book_in.isbn):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ISBN '{book_in.isbn}' đã tồn tại trong hệ thống",
        )

    return crud_books.create_book(db, book_in)


@router.put(
    "/{book_id}",
    response_model= books.BookResponse,
    summary="[Admin] Cập nhật sách",
)
def update_book(
    book_id: int,
    book_in: books.BookUpdate,
    db: Session = Depends(get_db),
    _admin: user.User = Depends(require_admin),
):
    book = _get_or_404(book_id, db)

    # Nếu đổi author thì kiểm tra author mới tồn tại
    if book_in.author_id is not None and book_in.author_id != book.author_id:
        if not crud_authors.get_author_by_id(db, book_in.author_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tác giả id={book_in.author_id} không tồn tại",
            )

    # Kiểm tra ISBN trùng với sách khác
    if book_in.isbn and book_in.isbn != book.isbn:
        existing = crud_books.get_book_by_isbn(db, book_in.isbn)
        if existing and existing.id != book_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"ISBN '{book_in.isbn}' đã được dùng bởi sách khác",
            )

    return crud_books.update_book(db, book, book_in)


@router.patch(
    "/{book_id}/toggle-availability",
    response_model=books.BookResponse,
    summary="[Admin] Bật/tắt trạng thái bán sách",
)
def toggle_availability(
    book_id: int,
    db: Session = Depends(get_db),
    _admin: user.User = Depends(require_admin),
):
    book = _get_or_404(book_id, db)
    book_in = books.BookUpdate(is_available=not book.is_available)
    return crud_books.update_book(db, book, book_in)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="[Admin] Xóa sách",
)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    _admin: user.User = Depends(require_admin),
):
    book = _get_or_404(book_id, db)
    crud_books.delete_book(db, book)