"""seed 2

Revision ID: 008c1dee1516
Revises: 55c8a10d2dd9
Create Date: 2026-07-10 20:30:06.321273

"""

import os
from typing import Sequence, Union

from alembic import context, op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from models.user import User
from models.user_blocking import UserBlocking
from models.post import Post
from models.post_comment import PostComment
from models.post_like import PostLike

# revision identifiers, used by Alembic.
revision: str = "008c1dee1516"
down_revision: Union[str, Sequence[str], None] = "55c8a10d2dd9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

db_url = "postgresql://{}:{}@{}:{}/{}".format(
    os.getenv("DB_USER"),
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_HOST"),
    os.getenv("DB_PORT"),
    os.getenv("DB_NAME"),
)


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_context().connection
    context.configure(connection=conn)

    session = sessionmaker(bind=context.get_bind())()
    user = User(
        email="poster1@mail.com",
        password="$argon2id$v=19$m=65536,t=3,p=4$wFBCoZUQcRxZSw4WOdXt4A$ubCqS8YRZ0I/c2S72rcD9jdrD9hcxkXkRs4yX7FeTIU",
        fullname="joe doe",
        username="poster1",
    )
    session.add(user)

    edit_user = User(
        email="poster3@mail.com",
        password="$argon2id$v=19$m=65536,t=3,p=4$wFBCoZUQcRxZSw4WOdXt4A$ubCqS8YRZ0I/c2S72rcD9jdrD9hcxkXkRs4yX7FeTIU",
        fullname="joe doe",
        username="poster3",
    )

    del_user = User(
        email="poster4@mail.com",
        password="$argon2id$v=19$m=65536,t=3,p=4$wFBCoZUQcRxZSw4WOdXt4A$ubCqS8YRZ0I/c2S72rcD9jdrD9hcxkXkRs4yX7FeTIU",
        fullname="joe doe",
        username="poster4",
    )
    like_user = User(
        id=118,
        email="like1@mail.com",
        password="$argon2id$v=19$m=65536,t=3,p=4$wFBCoZUQcRxZSw4WOdXt4A$ubCqS8YRZ0I/c2S72rcD9jdrD9hcxkXkRs4yX7FeTIU",
        fullname="joe doe",
        username="like1",
    )
    liked_user = User(
        id=120,
        email="liked1@mail.com",
        password="$argon2id$v=19$m=65536,t=3,p=4$wFBCoZUQcRxZSw4WOdXt4A$ubCqS8YRZ0I/c2S72rcD9jdrD9hcxkXkRs4yX7FeTIU",
        fullname="joe doe",
        username="liked1",
    )
    commented_user = User(
        id=130,
        email="commented1@mail.com",
        password="$argon2id$v=19$m=65536,t=3,p=4$wFBCoZUQcRxZSw4WOdXt4A$ubCqS8YRZ0I/c2S72rcD9jdrD9hcxkXkRs4yX7FeTIU",
        fullname="joe doe",
        username="commented1",
    )
    commenter_user = User(
        id=132,
        email="commenter1@mail.com",
        password="$argon2id$v=19$m=65536,t=3,p=4$wFBCoZUQcRxZSw4WOdXt4A$ubCqS8YRZ0I/c2S72rcD9jdrD9hcxkXkRs4yX7FeTIU",
        fullname="joe doe",
        username="commenter",
    )
    followed_user = User(
        id=100,
        email="followed_user1@mail.com",
        password="$argon2id$v=19$m=65536,t=3,p=4$wFBCoZUQcRxZSw4WOdXt4A$ubCqS8YRZ0I/c2S72rcD9jdrD9hcxkXkRs4yX7FeTIU",
        fullname="joe doe",
        username="followed_user1",
    )
    follower_user = User(
        id=140,
        email="follower_user1@mail.com",
        password="$argon2id$v=19$m=65536,t=3,p=4$wFBCoZUQcRxZSw4WOdXt4A$ubCqS8YRZ0I/c2S72rcD9jdrD9hcxkXkRs4yX7FeTIU",
        fullname="joe doe",
        username="follower_user1",
    )

    session.add_all(
        [
            user,
            edit_user,
            del_user,
            like_user,
            liked_user,
            commented_user,
            commenter_user,
            followed_user,
            follower_user,
        ]
    )
    session.flush()

    posts = [
        Post(
            content="long text long text long text long text long text long text",
            user_id=user.id,
        ),
        Post(
            content="long text 2 long text 2 long text 2 long text 2 long text 2 long text 2",
            user_id=user.id,
        ),
        Post(
            content="long text 3 long text 3 long text 3 long text 3 long text 3 long text 3",
            user_id=user.id,
        ),
        Post(
            id="019f4d45-18c8-7776-99ca-3591a962435c",
            content="this text should not be here. should be updated from pytest",
            user_id=edit_user.id,
        ),
        Post(
            id="019f4d5b-ca42-75e4-90e7-01a8d06e7acd",
            content="this post should not exits. it was delete from pytest",
            user_id=del_user.id,
        ),
        Post(
            id="019f52f8-905e-7e34-9456-071da4df492b",
            content="this post should have a like at the end of the test",
            user_id=liked_user.id,
        ),
        Post(
            id="019f53c8-44a6-7910-a289-548a53ee444e",
            content="this post should have a comment at the end of the test",
            user_id=commented_user.id,
        ),
    ]
    session.add_all(posts)

    users = [
        User(
            email="poster2@mail.com",
            password="$argon2id$v=19$m=65536,t=3,p=4$wFBCoZUQcRxZSw4WOdXt4A$ubCqS8YRZ0I/c2S72rcD9jdrD9hcxkXkRs4yX7FeTIU",
            fullname="joe doe",
            username="poster2",
        ),
    ]
    session.add_all(users)
    session.commit()
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
