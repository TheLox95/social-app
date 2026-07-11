"""seed 1

Revision ID: 55c8a10d2dd9
Revises: a7b158255bb8
Create Date: 2026-07-10 20:29:22.540869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import column, table


# revision identifiers, used by Alembic.
revision: str = '55c8a10d2dd9'
down_revision: Union[str, Sequence[str], None] = 'a7b158255bb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    users = [
        {
            "fullname": "Joe Doe",
            "password": "$argon2id$v=19$m=65536,t=3,p=4$wFBCoZUQcRxZSw4WOdXt4A$ubCqS8YRZ0I/c2S72rcD9jdrD9hcxkXkRs4yX7FeTIU",
            "email": "mail10@mail.com",
            "username": "joe10",
        }
    ]
    table_obj = table(
        "users",
        column("fullname"),
        column("password"),
        column("email"),
        column("username"),
    )

    op.bulk_insert(table_obj, users)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
