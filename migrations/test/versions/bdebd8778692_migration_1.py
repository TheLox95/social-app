"""migration 1

Revision ID: bdebd8778692
Revises: 2c9b3771ea10
Create Date: 2026-07-10 20:27:09.820059

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdebd8778692'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


create_refresh_updated_at_func = """
    CREATE FUNCTION {schema}.refresh_updated_at()
    RETURNS TRIGGER
    LANGUAGE plpgsql AS
    $func$
    BEGIN
       NEW.updated_at := now();
       RETURN NEW;
    END
    $func$;
    """

create_trigger = """
    CREATE TRIGGER trig_{table}_updated BEFORE UPDATE ON {schema}.{table}
    FOR EACH ROW EXECUTE PROCEDURE {schema}.refresh_updated_at();
    """


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("fullname", sa.String(length=35), nullable=False),
        sa.Column("password", sa.String(length=256), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )

    op.execute(sa.text(create_refresh_updated_at_func.format(schema="public")))
    op.execute(sa.text(create_trigger.format(table="users", schema="public")))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
