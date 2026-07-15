from sqlalchemy import ScalarResult, delete, insert, select
from sqlalchemy.orm import Session

from models.user import User
from models.user_blocking import UserBlocking
from models.user_following import UserFollowing


class FindUsersParams:
    def __init__(
        self,
        username: str | None = None,
        email: str | None = None,
        id: int | None = None,
    ):
        self.username = username
        self.email = email
        self.id = id


async def find_users(params: FindUsersParams, session: Session) -> ScalarResult:
    query = select(User)

    if params.username is not None:
        query = query.where(User.username == params.username)

    if params.email is not None:
        query = query.where(User.email == params.email)

    if params.id is not None:
        query = query.where(User.id == params.id)

    return session.scalars(query)


class FollowUserParams:
    def __init__(self, following_id: int, follower_id: int):
        self.following_id = following_id
        self.follower_id = follower_id


def follow_user(params: FollowUserParams, session: Session):
    query = insert(UserFollowing).values(
        following_user_id=params.following_id, follower_user_id=params.follower_id
    )

    return session.execute(query)


def delete_follow_user(params: FollowUserParams, session: Session):
    query = (
        delete(UserFollowing)
        .where(UserFollowing.following_user_id == params.following_id)
        .where(UserFollowing.follower_user_id == params.follower_id)
    )

    return session.execute(query)


class BlockUserParams:
    def __init__(self, blocking_user_id: int, blocked_by_user_id: int):
        self.blocking_user_id = blocking_user_id
        self.blocked_by_user_id = blocked_by_user_id


def block_user(params: BlockUserParams, session: Session):
    query = insert(UserBlocking).values(
        blocking_user_id=params.blocking_user_id,
        blocked_by_user_id=params.blocked_by_user_id,
    )

    return session.execute(query)


def delete_block_user(params: BlockUserParams, session: Session):
    query = (
        delete(UserBlocking)
        .where(UserBlocking.blocking_user_id == params.blocking_user_id)
        .where(UserBlocking.blocked_by_user_id == params.blocked_by_user_id)
    )

    return session.execute(query)
