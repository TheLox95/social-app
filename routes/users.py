from operator import and_, or_
from typing import List

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from db import db
from models.direct_message import DirectMessage
from models.user import User
from models.user_auth import UserAuth
from models.user_blocking import UserBlocking
from schemas.users import MessageListResponse, MessageUserRequest
from services.auth import get_token_data
from services.user import (
    FindUsersParams,
    FollowUserParams,
    block_user,
    delete_block_user,
    delete_follow_user,
    find_users,
    follow_user,
    BlockUserParams,
)

router = APIRouter(tags=["auth"])


@router.get("/profile")
def login(
    usr: UserAuth = Depends(get_token_data), driver: Session = Depends(db.get_db)
):
    user = (
        driver.query(User)
        .where(User.id == usr.id)
        .options(joinedload(User.followed_by))
        .options(joinedload(User.blocked_by))
        .first()
    )

    return user


@router.get("/follow/{user_id}")
async def follow_user_route(
    user_id: int,
    usr: UserAuth = Depends(get_token_data),
    session: Session = Depends(db.get_db),
):
    user = (await find_users(FindUsersParams(id=user_id), session)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if len(user.followed_by) > 0:
        found = next(
            (u for u in user.followed_by if u.following_user_id == usr.id), None
        )
        if found is not None:
            delete_follow_user(
                FollowUserParams(follower_id=user_id, following_id=usr.id), session
            )
        else:
            follow_user(
                FollowUserParams(follower_id=user_id, following_id=usr.id), session
            )
    else:
        follow_user(FollowUserParams(follower_id=user_id, following_id=usr.id), session)

    session.commit()
    return {"success": True}


@router.get("/block/{user_id}")
async def block_user_route(
    user_id: int,
    usr: UserAuth = Depends(get_token_data),
    session: Session = Depends(db.get_db),
):
    user = (await find_users(FindUsersParams(id=user_id), session)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if len(user.blocked_by) > 0:
        found = next(
            (u for u in user.blocked_by if u.blocked_by_user_id == usr.id), None
        )
        print(found)
        if found is not None:
            delete_block_user(
                BlockUserParams(blocking_user_id=user_id, blocked_by_user_id=usr.id),
                session,
            )
        else:
            block_user(
                BlockUserParams(blocking_user_id=user_id, blocked_by_user_id=usr.id),
                session,
            )
    else:
        block_user(
            BlockUserParams(blocking_user_id=user_id, blocked_by_user_id=usr.id),
            session,
        )

    session.commit()
    return {"success": True}


@router.post("/message/{user_id}")
async def send_message_user_route(
    user_id: int,
    body: MessageUserRequest,
    usr: UserAuth = Depends(get_token_data),
    session: Session = Depends(db.get_db),
):
    user = (await find_users(FindUsersParams(id=user_id), session)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    query = select(UserBlocking).where(
        or_(
            and_(
                UserBlocking.blocking_user_id == user_id,
                UserBlocking.blocked_by_user_id == usr.id,
            ),
            and_(
                UserBlocking.blocking_user_id == usr.id,
                UserBlocking.blocked_by_user_id == user_id,
            ),
        )
    )
    is_blocked = session.scalars(query).first()
    if is_blocked is not None:
        raise HTTPException(
            status_code=400, detail="Cannot send message to blocked user"
        )

    dm = DirectMessage(
        sender_user_id=usr.id, receiver_user_id=user_id, content=body.content
    )
    session.add(dm)
    session.commit()
    return {"success": True}


@router.get("/messages", response_model=List[MessageListResponse])
async def get_message_user_route(
    usr: UserAuth = Depends(get_token_data), session: Session = Depends(db.get_db)
):
    query = select(DirectMessage).where(DirectMessage.receiver_user_id == usr.id)
    messages = session.scalars(query).all()
    return messages
