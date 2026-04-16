"""
Test suite cho Books endpoints.
Covers: list, get, create, update, soft delete, restore.
"""
import pytest
from test.conftest import get_admin_token, get_user_token
from fastapi.testclient import TestClient

class TestListBooks:
    def test_list_books_public(self, client: TestClient, sample_book):
        """Bất kỳ ai cũng có thể xem danh sách sách."""
        res = client.get("/books/")
        assert res.status_code == 200
        data = res.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Chí Phèo"

    def test_list_books_pagination(self, client: TestClient, db, sample_author):
        """Kiểm tra pagination hoạt động đúng."""
        from app.models.book import Book
        for i in range(15):
            db.add(Book(title=f"Book {i:02d}", author_id=sample_author.id))
        db.commit()

        res = client.get("/books/?page=1&page_size=10")
        assert res.status_code == 200
        data = res.json()
        assert len(data["items"]) == 10
        assert data["total"] == 15
        assert data["total_pages"] == 2

    def test_list_books_search(self, client: TestClient, sample_book):
        """Tìm kiếm theo title."""
        res = client.get("/books/?search=chí")
        assert res.status_code == 200
        assert res.json()["total"] == 1

        res = client.get("/books/?search=khongcosach")
        assert res.json()["total"] == 0

    def test_list_books_filter_by_author(self, client: TestClient, sample_book, sample_author):
        res = client.get(f"/books/?author_id={sample_author.id}")
        assert res.status_code == 200
        assert res.json()["total"] == 1

    def test_list_books_filter_invalid_author(self, client: TestClient):
        res = client.get("/books/?author_id=99999")
        assert res.status_code == 404


class TestGetBook:
    def test_get_book_success(self, client: TestClient, sample_book):
        res = client.get(f"/books/{sample_book.id}")
        assert res.status_code == 200
        data = res.json()
        assert data["title"] == "Chí Phèo"
        assert "author" in data
        assert data["author"]["name"] == "Nam Cao"

    def test_get_book_not_found(self, client: TestClient):
        res = client.get("/books/99999")
        assert res.status_code == 404


class TestCreateBook:
    def test_create_book_as_admin(self, client: TestClient, admin_user, sample_author):
        token = get_admin_token(client, admin_user)
        res = client.post(
            "/books/",
            json={
                "title": "Lão Hạc",
                "author_id": sample_author.id,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res.status_code == 201
        assert res.json()["title"] == "Lão Hạc"

    def test_create_book_as_user_forbidden(self, client: TestClient, normal_user, sample_author):
        """User thường không được tạo sách."""
        token = get_user_token(client, normal_user)
        res = client.post(
            "/books/",
            json={"title": "Test","author_id": sample_author.id},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res.status_code == 403

    def test_create_book_author_not_found(self, client: TestClient, admin_user):
        token = get_admin_token(client, admin_user)
        res = client.post(
            "/books/",
            json={"title": "Test","author_id": 99999},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res.status_code == 404

    def test_create_book_isbn_already_exists(self, client: TestClient, admin_user, sample_author, sample_book):
        token = get_admin_token(client, admin_user)
        res = client.post(
            "/books/",
            json={
                "title": "Different Title",
                "author_id": sample_author.id,
                "isbn": sample_book.isbn,   # ISBN already exists
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res.status_code == 400

    def test_create_book_valid_isbn13(self, client: TestClient, admin_user, sample_author):
        token = get_admin_token(client, admin_user)
        res = client.post(
            "/books/",
            json={
                "title": "Test ISBN",
                "author_id": sample_author.id,
                "isbn": "978-3-16-148410-0",  # ISBN-13 hợp lệ
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res.status_code == 201


class TestSoftDelete:
    def test_soft_delete_book(self, client: TestClient, admin_user, sample_book):
        """Sau khi xóa mềm, sách không còn xuất hiện trong list."""
        token = get_admin_token(client, admin_user)

        # Xóa mềm
        res = client.delete(
            f"/books/{sample_book.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res.status_code == 204

        # Kiểm tra không còn trong list
        res = client.get("/books/")
        assert res.json()["total"] == 0

        # Kiểm tra GET trực tiếp cũng trả 404
        res = client.get(f"/books/{sample_book.id}")
        assert res.status_code == 404
