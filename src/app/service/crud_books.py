from typing import List, Optional, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.book import Book 
from app.schemas.books import BookCreate, BookUpdate
from app.logger import get_logger

logger = get_logger(__name__)


def get_book(db: Session, book_id: int) -> Optional[Book]:
    return (
        db.query(Book)
        .options(joinedload(Book.author))
        .filter(Book.id == book_id)
        .first()
    )
def get_book_by_isbn(db: Session, isbn: str) -> Optional[Book]:
    return db.query(Book).filter(Book.isbn == isbn).first()

def get_books(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    author_id: Optional[int] = None,
    is_available: Optional[bool] = None,
) -> Tuple[List[Book], int]:
    """
    Trả về (items, total).
    - search   : tìm theo title (ILIKE)
    - author_id: filter theo tác giả
    """
    query = db.query(Book).options(joinedload(Book.author))

    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))

    if author_id is not None:
        query = query.filter(Book.author_id == author_id)

    if is_available is not None:
        query = query.filter(Book.is_available == is_available)

    total = query.count()
    items = (
        query
        .order_by(Book.title)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    logger.debug(f"get_books: page={page}, total={total}")
    return items, total


def create_book(db: Session, book_in: BookCreate) -> Book:
    book = Book(**book_in.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    # Reload với author để response trả đủ data
    db.refresh(book)
    logger.info(f'Book created: id = {book.id}, title = {book.title}')
    return get_book(db, book.id)


def update_book(
    db: Session,
    book: Book,
    book_in: BookUpdate,
) -> Book:
    update_data = book_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    logger.info(f'Book updated: id = {book.id}, title = {book.title}')
    return get_book(db, book.id)


def delete_book(db: Session, book: Book) -> None:
    db.delete(book)
    db.commit()
    logger.warning(f"Book hard-deleted: id={book.id} title='{book.title}'")