"""migration 2

Revision ID: a7b158255bb8
Revises: bdebd8778692
Create Date: 2026-07-10 20:28:14.494463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7b158255bb8'
down_revision: Union[str, Sequence[str], None] = 'bdebd8778692'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

create_trigger = """
    CREATE TRIGGER trig_{table}_updated BEFORE UPDATE ON {schema}.{table}
    FOR EACH ROW EXECUTE PROCEDURE {schema}.refresh_updated_at();
    """

def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "posts",
        sa.Column("id", sa.UUID(), server_default=sa.text("uuidv7()"), nullable=False),
        sa.Column("content", sa.VARCHAR(length=500), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="cascade"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_posts_user_id"), "posts", ["user_id"], unique=False)
    op.execute(sa.text(create_trigger.format(table="posts", schema="public")))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
