from typing import Optional, Tuple, List

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.schemas.authors import AuthorBase, AuthorUpdate
from app.models.author import Author
from app.models.book import Book
from app.logger import get_logger

logger = get_logger(__name__)
def get_author_by_id(db: Session, author_id: int) -> Optional[Author]:
    return db.query(Author).filter(Author.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> Optional[Author]:
    return db.query(Author).filter(
        func.lower(Author.name) == name.lower()
    ).first()


def get_authors(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
) -> Tuple[List[Author], int]:
    """
    Trả về (items, total) để build PaginatedResponse.
    - search: tìm theo tên (ILIKE)
    - nationality: filter chính xác
    """
    query = db.query(Author)

    if search:
        query = query.filter(Author.name.ilike(f"%{search}%"))

    total = query.count()
    items = (
        query
        .order_by(Author.name)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    logger.debug(f"get_authors: page={page}, total={total}")
    return items, total


def create_new_author(db: Session, author_in: AuthorBase) -> Author:
    author = Author(**author_in.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    logger.info(f'Author created: id = {author.id}, name = {author.name}')
    return author


def update_current_author(
    db: Session,
    author: Author,
    author_in: AuthorUpdate,
) -> Author:
    update_data = author_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(author, field, value)
    db.commit()
    db.refresh(author)
    logger.info(f'Author updated: id = {author.id}, name = {author.name}')
    return author


def delete_current_author(db: Session, author: Author) -> None:
    db.delete(author)
    db.commit()
    logger.warning(f'Author deleted: id = {author.id}, name = {author.name}')

def get_book_count(db: Session, author_id: int) -> int:
    return db.query(func.count(Book.id)).filter(
        Book.author_id == author_id
    ).scalar()