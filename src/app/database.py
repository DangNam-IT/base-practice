from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL_SYNC,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=Session
)

Base = declarative_base()


def get_db():
    """Dependency: cung cấp DB session, tự đóng sau mỗi request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()