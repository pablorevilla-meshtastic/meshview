"""Add daily_snapshot table

Revision ID: 4f1d2a9c8b71
Revises: 23dad03d2e42
Create Date: 2026-03-05 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4f1d2a9c8b71"
down_revision: str | None = "23dad03d2e42"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "daily_snapshot",
        sa.Column("snapshot_date", sa.Date(), nullable=False),
        sa.Column("node_count", sa.BigInteger(), nullable=False),
        sa.Column("packet_count", sa.BigInteger(), nullable=False),
        sa.Column("gateway_count", sa.BigInteger(), nullable=False),
        sa.Column("captured_at_us", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("snapshot_date"),
    )


def downgrade() -> None:
    op.drop_table("daily_snapshot")
