"""seed users

Revision ID: 54a1ed1f517f
Revises: 52284bde47f4
Create Date: 2026-07-09 11:00:07.032072

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision: str = "54a1ed1f517f"
down_revision: Union[str, Sequence[str], None] = "52284bde47f4"
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


def downgrade() -> None:
    """Downgrade schema."""
    pass
