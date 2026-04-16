"""Test suite cho Authors endpoints."""
import pytest
from test.conftest import get_admin_token
from fastapi.testclient import TestClient

class TestAuthors:
    def test_list_authors_public(self, client: TestClient, sample_author):
        res = client.get("/authors/")
        assert res.status_code == 200
        assert res.json()["total"] == 1

    def test_get_author_detail(self, client: TestClient, sample_author, sample_book):
        res = client.get(f"/authors/{sample_author.id}")
        assert res.status_code == 200
        data = res.json()
        assert data["name"] == "Nam Cao"

    def test_create_author_admin(self, client: TestClient, admin_user):
        token = get_admin_token(client, admin_user)
        res = client.post(
            "/authors/",
            json={"name": "Nguyễn Du"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res.status_code == 201
        assert res.json()["name"] == "Nguyễn Du"

    def test_delete_author_with_books_blocked(self, client: TestClient, admin_user, sample_author, sample_book):
        """Không thể xóa tác giả còn sách — phải dùng /force."""
        token = get_admin_token(client, admin_user)
        res = client.delete(
            f"/authors/{sample_author.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res.status_code == 400
        assert "sách" in res.json()["detail"]