from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.db import get_db
from models.app_notification import AppNotification, NotificationKind
from models.user_auth import UserAuth
from schemas.post import (
    CommentPostRequest,
    CreatePostRequest,
    DeletePostRequest,
    LikePostRequest,
    PostListResponse,
    SuccessResponse,
    UpdatePostRequest,
)
from services.auth import get_token_data
from services.post import (
    CommentPostParams,
    CreatePostParams,
    DeleteLikePostParams,
    DeletePostParams,
    FindPostParams,
    LikePostParams,
    UpdatePostParams,
    comment_post,
    create_post,
    delete_like_post,
    delete_post,
    find_post,
    like_post,
    update_post,
)

router = APIRouter(prefix="/post", tags=["post"])


# list posts
@router.get("/", response_model=List[PostListResponse])
def list_posts(
    usr: UserAuth = Depends(get_token_data), session: Session = Depends(get_db)
):
    posts = find_post(
        FindPostParams(user_id=usr.id, include_likes=True, include_comments=True),
        session,
    ).all()
    return posts


# create post
@router.post("/", response_model=SuccessResponse)
def create_post_req(
    body: CreatePostRequest,
    session: Session = Depends(get_db),
    usr: UserAuth = Depends(get_token_data),
):
    create_post(CreatePostParams(user_id=usr.id, content=body.content), session)
    session.commit()
    return {"success": True}


# edit post
@router.put("/", response_model=SuccessResponse)
def update_post_route(
    body: UpdatePostRequest,
    session: Session = Depends(get_db),
    usr: UserAuth = Depends(get_token_data),
):
    post = find_post(
        FindPostParams(user_id=usr.id, id=body.id.__str__()), session
    ).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    update_post(
        UpdatePostParams(
            content=body.content, post_id=body.id.__str__(), user_id=usr.id
        ),
        session,
    )
    session.commit()

    return {"success": True}


# delete post
@router.delete("/", response_model=SuccessResponse)
def delete_post_route(
    body: DeletePostRequest,
    session: Session = Depends(get_db),
    usr: UserAuth = Depends(get_token_data),
):
    post = find_post(
        FindPostParams(user_id=usr.id, id=body.id.__str__()), session
    ).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    delete_post(DeletePostParams(post_id=body.id.__str__(), user_id=usr.id), session)
    session.commit()

    return {"success": True}


# like post
@router.post("/like")
def like_post_request(
    body: LikePostRequest,
    session: Session = Depends(get_db),
    usr: UserAuth = Depends(get_token_data),
):
    post_id = body.post_id.__str__()
    post = find_post(FindPostParams(id=post_id, include_likes=True), session).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    like_found = next((like for like in post.likes if like.author_id == usr.id), None)

    if like_found is None:
        like_post(LikePostParams(post_id=post_id, author_id=usr.id), session)
        notf = AppNotification(event_type=NotificationKind.LIKE, author_id=usr.id, resource_id=post_id, receiver_id=post.user_id)
        session.add(notf)
    else:
        delete_like_post(
            DeleteLikePostParams(post_id=post_id, author_id=usr.id, like_id=like_found.id), session
        )

    session.commit()
    return {"succes": True}


# comment post
@router.post("/comment")
def comment_post_request(
    body: CommentPostRequest,
    session: Session = Depends(get_db),
    usr: UserAuth = Depends(get_token_data),
):
    post_id = body.post_id.__str__()
    post = find_post(FindPostParams(id=post_id, include_likes=True), session).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    comment_post(
        CommentPostParams(
            post_id=body.post_id.__str__(),
            author_id=usr.id,
            content=body.content,
            parent_comment_id=body.parent_comment_id,
        ),
        session,
    )
    notf = AppNotification(event_type=NotificationKind.COMMENT, author_id=usr.id, resource_id=post_id, receiver_id=post.user_id)
    session.add(notf)
    session.commit()

    return {"succes": True}


# share post (?
# cross-post (?
