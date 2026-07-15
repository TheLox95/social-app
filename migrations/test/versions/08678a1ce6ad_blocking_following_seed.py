"""blocking following seed

Revision ID: 08678a1ce6ad
Revises: 185415d97d1d
Create Date: 2026-07-15 12:06:53.224752

"""

from typing import Sequence, Union

from alembic import context, op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from models.user import User
from models.user_blocking import UserBlocking


# revision identifiers, used by Alembic.
revision: str = "08678a1ce6ad"
down_revision: Union[str, Sequence[str], None] = "185415d97d1d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    conn = op.get_context().connection
    context.configure(connection=conn)
    session = sessionmaker(bind=context.get_bind())()
    dm_sender = User(
        id=150,
        email="dm_sender1@mail.com",
        password="$argon2id$v=19$m=65536,t=3,p=4$wFBCoZUQcRxZSw4WOdXt4A$ubCqS8YRZ0I/c2S72rcD9jdrD9hcxkXkRs4yX7FeTIU",
        fullname="joe doe",
        username="dm_sender1",
    )
    dm_receiver = User(
        id=152,
        email="dm_receiver1@mail.com",
        password="$argon2id$v=19$m=65536,t=3,p=4$wFBCoZUQcRxZSw4WOdXt4A$ubCqS8YRZ0I/c2S72rcD9jdrD9hcxkXkRs4yX7FeTIU",
        fullname="joe doe",
        username="dm_receiver1",
    )
    dm_receiver_blocked = User(
        id=154,
        email="dm_receiver_blocked1@mail.com",
        password="$argon2id$v=19$m=65536,t=3,p=4$wFBCoZUQcRxZSw4WOdXt4A$ubCqS8YRZ0I/c2S72rcD9jdrD9hcxkXkRs4yX7FeTIU",
        fullname="joe doe",
        username="dm_receiver_blocked1",
    )
    blocked_relation = UserBlocking(blocking_user_id=150, blocked_by_user_id=154)

    session.add_all([dm_sender, dm_receiver, dm_receiver_blocked, blocked_relation])

    session.commit()

    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
