"""
Fixtures dùng chung cho toàn bộ test suite.
Dùng SQLite in-memory để test nhanh, độc lập với DB thật.
"""

import os
# ← PHẢI là dòng đầu tiên trước mọi import từ app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key-32-chars-minimum!"
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from main import app
from app.models.author import Author
from app.models.book import Book
from app.models.user import User 
from app.security import hash_password

# ── In-memory SQLite chỉ tồn tại trong 1 test session ────
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,   # đảm bảo dùng cùng 1 connection
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=False)
def db():
    """Tạo fresh DB cho mỗi test — tự rollback sau khi xong."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """TestClient với DB override."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Helpers tạo dữ liệu test ──────────────────────────────

@pytest.fixture
def admin_user(db):
    user = User(
        username="admin",
        hashed_password=hash_password("adminpass"),
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def normal_user(db):
    user = User(
        username="testuser",
        hashed_password=hash_password("userpass"),
        role = "user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def sample_author(db):
    author = Author(name="Nam Cao", bio="Nhà văn hiện thực")
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@pytest.fixture
def sample_book(db, sample_author):
    book = Book(
        title="Chí Phèo",
        isbn="978-604-84-1234-5",
        author_id=sample_author.id,
        is_available=True,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_admin_token(client, admin_user) -> str:
    """Helper: đăng nhập và trả về Bearer token."""
    res = client.post("/auth/login", data={"username": "admin", "password": "adminpass"})
    assert res.status_code == 200
    return res.json()["access_token"]


def get_user_token(client, normal_user) -> str:
    res = client.post("/auth/login", data={"username": "testuser", "password": "userpass"})
    assert res.status_code == 200
    return res.json()["access_token"]