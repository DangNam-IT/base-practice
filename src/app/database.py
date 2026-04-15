from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from app.config import settings

Base = declarative_base()
_engine = None
_SessionLocal = None
def get_engine():
    global _engine
    if _engine is None:
        connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
        _engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
    return _engine


def get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine(), class_=Session)
    return _SessionLocal


# Giữ lại engine và SessionLocal như property để không break code cũ
engine = get_engine()

def get_db():
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()