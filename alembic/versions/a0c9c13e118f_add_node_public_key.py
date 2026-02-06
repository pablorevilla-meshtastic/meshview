"""Add node_public_key table

Revision ID: a0c9c13e118f
Revises: d4d7b0c2e1a4
Create Date: 2026-02-06 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a0c9c13e118f"
down_revision: str | None = "d4d7b0c2e1a4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "node_public_key",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("node_id", sa.BigInteger(), nullable=False),
        sa.Column("public_key", sa.String(), nullable=False),
        sa.Column("first_seen_us", sa.BigInteger(), nullable=True),
        sa.Column("last_seen_us", sa.BigInteger(), nullable=True),
    )
    op.create_index("idx_node_public_key_node_id", "node_public_key", ["node_id"], unique=False)
    op.create_index(
        "idx_node_public_key_public_key",
        "node_public_key",
        ["public_key"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("idx_node_public_key_public_key", table_name="node_public_key")
    op.drop_index("idx_node_public_key_node_id", table_name="node_public_key")
    op.drop_table("node_public_key")
