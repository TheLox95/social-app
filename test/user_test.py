
from dotenv import load_dotenv
from fastapi.testclient import TestClient
import pytest

from app.main import app

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv(dotenv_path=".env")


client = TestClient(app=app)

def test_follow_user():
    response = client.post(
        "/login", json={"email": "follower_user1@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    follower_cred = response.json()

    response = client.get(
        "/follow/100", headers={"Authorization": "Bearer {}".format(follower_cred.get("access_token"))}
    )
    assert response.status_code == 200

    response = client.post(
        "/login", json={"email": "followed_user1@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    followed_cred = response.json()

    response = client.get(
        "/profile", headers={"Authorization": "Bearer {}".format(followed_cred.get("access_token"))}
    )
    assert response.status_code == 200
    profile = response.json()
    assert len(profile.get("followed_by")) == 1

    # call follow API again to un-follow the same user
    response = client.get(
        "/follow/100", headers={"Authorization": "Bearer {}".format(follower_cred.get("access_token"))}
    )
    assert response.status_code == 200

    response = client.get(
        "/profile", headers={"Authorization": "Bearer {}".format(followed_cred.get("access_token"))}
    )
    assert response.status_code == 200
    profile = response.json()
    assert len(profile.get("followed_by")) == 0

def test_block_user():
    response = client.post(
        "/login", json={"email": "follower_user1@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    follower_cred = response.json()

    response = client.get(
        "/block/100", headers={"Authorization": "Bearer {}".format(follower_cred.get("access_token"))}
    )
    assert response.status_code == 200

    response = client.post(
        "/login", json={"email": "followed_user1@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    followed_cred = response.json()

    response = client.get(
        "/profile", headers={"Authorization": "Bearer {}".format(followed_cred.get("access_token"))}
    )
    assert response.status_code == 200
    profile = response.json()
    assert len(profile.get("blocked_by")) == 1

    # call block API again to un-block the same user
    response = client.get(
        "/block/100", headers={"Authorization": "Bearer {}".format(follower_cred.get("access_token"))}
    )
    assert response.status_code == 200

    response = client.get(
        "/profile", headers={"Authorization": "Bearer {}".format(followed_cred.get("access_token"))}
    )
    assert response.status_code == 200
    profile = response.json()
    assert len(profile.get("blocked_by")) == 0
