import json

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from app.main import app
from models.post_comment import PostComment
from models.post_like import PostLike
import pytest


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv(dotenv_path=".env")


client = TestClient(app=app)


# list post
def test_list_post():
    response = client.post(
        "/login", json={"email": "poster1@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    data = response.json()

    response = client.get(
        "/post", headers={"Authorization": "Bearer {}".format(data.get("access_token"))}
    )
    posts = response.json()
    assert len(posts) == 3


# create post
def test_create_post():
    response = client.post(
        "/login", json={"email": "poster2@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    data = response.json()

    response = client.post(
        "/post",
        json={"content": "this is a new created post from pytest"},
        headers={"Authorization": "Bearer {}".format(data.get("access_token"))},
    )
    assert response.status_code == 200
    data = response.json()
    assert "success" in data


# update post
def test_update_post():
    response = client.post(
        "/login", json={"email": "poster3@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    data = response.json()

    post_content = "this was edited from pytest"
    response = client.put(
        "/post",
        json={"content": post_content, "id": "019f4d45-18c8-7776-99ca-3591a962435c"},
        headers={"Authorization": "Bearer {}".format(data.get("access_token"))},
    )
    assert response.status_code == 200

    response = client.get(
        "/post", headers={"Authorization": "Bearer {}".format(data.get("access_token"))}
    )
    posts = response.json()
    assert posts[0].get("content") == post_content


# throw error on update when post do not exits
def test_update_post_not_found():
    response = client.post(
        "/login", json={"email": "poster3@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    data = response.json()

    response = client.put(
        "/post",
        json={
            "content": "this was edited from pytest",
            "id": "019f4d45-18c8-7776-99ca-3591a962435a",
        },
        headers={"Authorization": "Bearer {}".format(data.get("access_token"))},
    )
    assert response.status_code == 404


# delete post
def test_delete_user():
    response = client.post(
        "/login", json={"email": "poster4@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    data = response.json()

    post_content = "this was edited from pytest"
    response = client.request(
        "DELETE",
        "/post",
        json={"content": post_content, "id": "019f4d5b-ca42-75e4-90e7-01a8d06e7acd"},
        headers={"Authorization": "Bearer {}".format(data.get("access_token"))},
    )
    assert response.status_code == 200

    response = client.get(
        "/post", headers={"Authorization": "Bearer {}".format(data.get("access_token"))}
    )
    posts = response.json()
    assert len(posts) == 0


# throw error on delete when post do not exits
def test_delete_post_not_foun():
    response = client.post(
        "/login", json={"email": "poster4@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    data = response.json()

    response = client.request(
        "DELETE",
        "/post",
        json={
            "content": "this was edited from pytest",
            "id": "019f4d45-18c8-7776-99ca-3591a962435b",
        },
        headers={"Authorization": "Bearer {}".format(data.get("access_token"))},
    )
    assert response.status_code == 404


def test_like_post():
    response = client.post(
        "/login", json={"email": "like1@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    data = response.json()

    post_id = "019f52f8-905e-7e34-9456-071da4df492b"
    response = client.post(
        "/post/like",
        json={"post_id": post_id},
        headers={"Authorization": "Bearer {}".format(data.get("access_token"))},
    )
    assert response.status_code == 200

    response = client.post(
        "/login", json={"email": "liked1@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    data = response.json()

    response = client.get(
        "/post", headers={"Authorization": "Bearer {}".format(data.get("access_token"))}
    )
    posts = response.json()
    assert len(posts) == 1
    found = next((p for p in posts if p.get("id") == post_id), None)
    assert found is not None
    assert len(found.get("likes")) == 1

    # call like API again to 'delete' the like
    response = client.post(
        "/login", json={"email": "like1@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    data = response.json()

    response = client.post(
        "/post/like",
        json={"post_id": post_id},
        headers={"Authorization": "Bearer {}".format(data.get("access_token"))},
    )
    assert response.status_code == 200

    response = client.post(
        "/login", json={"email": "liked1@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    data = response.json()

    response = client.get(
        "/post", headers={"Authorization": "Bearer {}".format(data.get("access_token"))}
    )
    posts = response.json()
    assert len(posts) == 1
    found = next((p for p in posts if p.get("id") == post_id), None)
    assert found is not None
    assert len(found.get("likes")) == 0

def test_comment_post():
    response = client.post(
        "/login", json={"email": "commenter1@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    data = response.json()

    post_id = "019f53c8-44a6-7910-a289-548a53ee444e"
    response = client.post(
        "/post/comment",
        json={"post_id": post_id, "content": "this test is good"},
        headers={"Authorization": "Bearer {}".format(data.get("access_token"))},
    )
    assert response.status_code == 200

    response = client.post(
        "/login", json={"email": "commented1@mail.com", "password": "123456Abc!"}
    )
    assert response.status_code == 200
    data = response.json()

    response = client.get(
        "/post", headers={"Authorization": "Bearer {}".format(data.get("access_token"))}
    )
    posts = response.json()
    assert len(posts) == 1
    found = next((p for p in posts if p.get("id") == post_id), None)
    assert found is not None
    assert len(found.get("comments")) == 1
