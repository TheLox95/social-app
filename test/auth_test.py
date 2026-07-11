from fastapi.testclient import TestClient
from dotenv import load_dotenv
from app.main import app
import pytest


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv(dotenv_path=".env")


client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to my project"}


def test_failed_login():
    """Should fail when user does not exits on DB"""
    response = client.post(
        "/login", json={"email": "error@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 404


def test_sucess_login():
    """should return access token in the cookies when user exits on DB"""
    response = client.post(
        "/login", json={"email": "mail10@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    token = response.cookies.get("refresh_token")
    assert token is not None

    body = response.json()
    assert "access_token" in body


def test_register():
    """should register with the correct body"""

    response = client.post(
        "/register",
        json={
            "email": "joe1@mail.com",
            "password": "123456Abc!",
            "confirmPassword": "123456Abc!",
            "fullname": "Joe doe",
            "username": "joe",
        },
    )
    assert response.status_code == 200
