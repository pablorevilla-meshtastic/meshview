"""Add relay_node column to packet_seen

Revision ID: c6b1d8f2a9e3
Revises: 4f1d2a9c8b71
Create Date: 2026-03-05 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c6b1d8f2a9e3"
down_revision: str | None = "4f1d2a9c8b71"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    packet_seen_columns = {col["name"] for col in inspector.get_columns("packet_seen")}

    if "relay_node" not in packet_seen_columns:
        with op.batch_alter_table("packet_seen", schema=None) as batch_op:
            batch_op.add_column(sa.Column("relay_node", sa.BigInteger(), nullable=True))


def downgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    packet_seen_columns = {col["name"] for col in inspector.get_columns("packet_seen")}

    if "relay_node" in packet_seen_columns:
        with op.batch_alter_table("packet_seen", schema=None) as batch_op:
            batch_op.drop_column("relay_node")
