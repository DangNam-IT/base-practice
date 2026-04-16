"""
Test suite cho Auth endpoints.
Covers: register, login, /me, phân quyền.
"""
import pytest
from fastapi.testclient import TestClient


class TestRegister:
    def test_register_success(self, client: TestClient):
        res = client.post("/auth/register", json={
            "username": "newuser",
            "password": "secret123",
        })
        assert res.status_code == 201
        data = res.json()
        assert data["username"] == "newuser"
        assert data["role"] == "user"  # mặc định role là user
        assert "hashed_password" not in data  # không lộ password

    def test_register_duplicate_username(self, client: TestClient, normal_user):
        res = client.post("/auth/register", json={
            "username": "testuser",   # đã tồn tại trong fixture
            "password": "secret123",
        })
        assert res.status_code == 400
        assert "Username" in res.json()["detail"]

    def test_register_short_password(self, client: TestClient):
        res = client.post("/auth/register", json={
            "username": "validuser",
            "password": "123",  # < 6 ký tự
        })
        assert res.status_code == 422


class TestLogin:
    def test_login_success(self, client: TestClient, normal_user):
        res = client.post("/auth/login", data={
            "username": "testuser",
            "password": "userpass",
        })
        assert res.status_code == 200
        data = res.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient, normal_user):
        res = client.post("/auth/login", data={
            "username": "testuser",
            "password": "wrongpass",
        })
        assert res.status_code == 401

    def test_login_nonexistent_user(self, client: TestClient):
        res = client.post("/auth/login", data={
            "username": "ghost",
            "password": "anything",
        })
        assert res.status_code == 401


class TestGetMe:
    def test_get_me_authenticated(self, client: TestClient, normal_user):
        token_res = client.post("/auth/login", data={"username": "testuser", "password": "userpass"})
        token = token_res.json()["access_token"]

        res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        assert res.json()["username"] == "testuser"

    def test_get_me_no_token(self, client: TestClient):
        res = client.get("/auth/me")
        assert res.status_code == 401

    def test_get_me_invalid_token(self, client: TestClient):
        res = client.get("/auth/me", headers={"Authorization": "Bearer invalidtoken"})
        assert res.status_code == 401