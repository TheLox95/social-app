"""blocking following direct_message

Revision ID: fe935a922d30
Revises: 4b2be440ac05
Create Date: 2026-07-15 12:20:14.354304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe935a922d30'
down_revision: Union[str, Sequence[str], None] = '4b2be440ac05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

create_trigger = """
    CREATE TRIGGER trig_{table}_updated BEFORE UPDATE ON {schema}.{table}
    FOR EACH ROW EXECUTE PROCEDURE {schema}.refresh_updated_at();
    """

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users_blocked",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("blocking_user_id", sa.Integer(), nullable=False),
        sa.Column("blocked_by_user_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(["blocked_by_user_id"], ["users.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["blocking_user_id"], ["users.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "uix_blocking_blocked_users",
        "users_blocked",
        ["blocking_user_id", "blocked_by_user_id"],
        unique=True,
    )
    op.execute(sa.text(create_trigger.format(table="users_blocked", schema="public")))
    op.create_table(
        "users_following",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("following_user_id", sa.Integer(), nullable=False),
        sa.Column("follower_user_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(["follower_user_id"], ["users.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(
            ["following_user_id"], ["users.id"], ondelete="cascade"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "uix_following_follower_users",
        "users_following",
        ["following_user_id", "follower_user_id"],
        unique=True,
    )
    op.execute(sa.text(create_trigger.format(table="users_following", schema="public")))
    op.create_table(
        "direct_message",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sender_user_id", sa.Integer(), nullable=False),
        sa.Column("receiver_user_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.VARCHAR(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(["receiver_user_id"], ["users.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["sender_user_id"], ["users.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute(sa.text(create_trigger.format(table="direct_message", schema="public")))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
