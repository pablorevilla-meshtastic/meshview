"""Drop last_update_us from node.

Revision ID: d4d7b0c2e1a4
Revises: b7c3c2e3a1f0
Create Date: 2026-01-12 10:20:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d4d7b0c2e1a4"
down_revision: str | None = "b7c3c2e3a1f0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    conn = op.get_bind()
    if conn.dialect.name == "sqlite":
        with op.batch_alter_table("node", schema=None) as batch_op:
            batch_op.drop_index("idx_node_last_update_us")
            batch_op.drop_column("last_update_us")
    else:
        op.drop_index("idx_node_last_update_us", table_name="node")
        op.drop_column("node", "last_update_us")


def downgrade() -> None:
    op.add_column("node", sa.Column("last_update_us", sa.BigInteger(), nullable=True))
    op.create_index("idx_node_last_update_us", "node", ["last_update_us"], unique=False)
