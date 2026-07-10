from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.db import get_db
from models.user_auth import UserAuth
from schemas.post import CreatePostRequest, DeletePostRequest, SuccessResponse, UpdatePostRequest
from services.auth import get_token_data
from services.post import CreatePostParams, DeletePostParams, FindPostParams, UpdatePostParams, create_post, delete_post, find_post, update_post

router = APIRouter(prefix="/post", tags=["post"])


# list posts
@router.get("/")
def list_posts(
    usr: UserAuth = Depends(get_token_data), session: Session = Depends(get_db)
):
    posts = find_post(FindPostParams(user_id=usr.id), session).all()

    return [p._mapping for p in posts]


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
def update_post_route(body: UpdatePostRequest, session: Session = Depends(get_db), usr: UserAuth = Depends(get_token_data)):
    update_post(UpdatePostParams(content=body.content, post_id=body.id, user_id=usr.id), session)
    session.commit()

    return { "success": True }


# delete post
@router.delete("/", response_model=SuccessResponse)
def delete_post_route(body: DeletePostRequest, session: Session = Depends(get_db), usr: UserAuth = Depends(get_token_data)):
    delete_post(DeletePostParams(post_id=body.id, user_id=usr.id), session)
    session.commit()

    return { "success": True}


# like post

# comment post

# share post (?
# cross-post (?
