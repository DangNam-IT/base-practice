from typing import Optional, Tuple, List

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.schemas.authors import AuthorBase, AuthorUpdate
from app.models.author import Author 



def get_author(db: Session, author_id: int) -> Optional[Author]:
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
    return items, total


def create_author(db: Session, author_in: AuthorBase) -> Author:
    author = Author(**author_in.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def update_author(
    db: Session,
    author: Author,
    author_in: AuthorUpdate,
) -> Author:
    update_data = author_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(author, field, value)
    db.commit()
    db.refresh(author)
    return author


def delete_author(db: Session, author: Author) -> None:
    db.delete(author)
    db.commit()