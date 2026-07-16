
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

    response = client.get(
        "/notifications", headers={"Authorization": "Bearer {}".format(followed_cred.get("access_token"))}
    )
    assert response.status_code == 200
    notifications = response.json()
    found = next((n for n in notifications if n.get("event_type") == "FOLLOW" and n.get("author_id") == 140), None)
    assert found is not None


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
    # should unfollow user

def test_directmessage_user():
    # test user exist
    response = client.post(
        "/login", json={"email": "dm_sender1@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    sender_cred = response.json()

    response = client.post(
        "/message/99", json={"content": "dm 1"}, headers={"Authorization": "Bearer {}".format(sender_cred.get("access_token"))}
    )
    assert response.status_code == 404
    data = response.json()
    assert data.get("detail") == "User not found"
    # test user receives message
    response = client.post(
        "/message/152", json={"content": "dm 1"}, headers={"Authorization": "Bearer {}".format(sender_cred.get("access_token"))}
    )
    assert response.status_code == 200

    response = client.post(
        "/login", json={"email": "dm_receiver1@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    receiver_cred = response.json()

    response = client.get(
        "/messages", headers={"Authorization": "Bearer {}".format(receiver_cred.get("access_token"))}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    # test user cannot send message to block user

    response = client.post(
        "/message/154", json={"content": "dm 1"}, headers={"Authorization": "Bearer {}".format(sender_cred.get("access_token"))}
    )
    data = response.json()
    assert response.status_code == 400
    assert data.get("detail") == "Cannot send message to blocked user"

    response = client.get(
        "/notifications", headers={"Authorization": "Bearer {}".format(receiver_cred.get("access_token"))}
    )
    assert response.status_code == 200
    notifications = response.json()
    found = next((n for n in notifications if n.get("event_type") == "DM" and n.get("author_id") == 150), None)
    assert found is not None

