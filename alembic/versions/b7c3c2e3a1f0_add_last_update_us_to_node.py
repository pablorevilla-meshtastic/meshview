"""Add last_update_us to node and migrate data.

Revision ID: b7c3c2e3a1f0
Revises: 9f3b1a8d2c4f
Create Date: 2026-01-12 10:12:00.000000
"""

from collections.abc import Sequence
from datetime import UTC, datetime

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b7c3c2e3a1f0"
down_revision: str | None = "9f3b1a8d2c4f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _parse_datetime(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, str):
        text = value.replace("Z", "+00:00")
        try:
            dt = datetime.fromisoformat(text)
        except ValueError:
            return None
    else:
        return None

    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def upgrade() -> None:
    conn = op.get_bind()
    op.add_column("node", sa.Column("last_update_us", sa.BigInteger(), nullable=True))
    op.create_index("idx_node_last_update_us", "node", ["last_update_us"], unique=False)

    node = sa.table(
        "node",
        sa.column("id", sa.String()),
        sa.column("last_update", sa.DateTime()),
        sa.column("last_update_us", sa.BigInteger()),
    )

    rows = conn.execute(sa.select(node.c.id, node.c.last_update)).all()
    for node_id, last_update in rows:
        dt = _parse_datetime(last_update)
        if dt is None:
            continue
        last_update_us = int(dt.timestamp() * 1_000_000)
        conn.execute(
            sa.update(node).where(node.c.id == node_id).values(last_update_us=last_update_us)
        )

    if conn.dialect.name == "sqlite":
        with op.batch_alter_table("node", schema=None) as batch_op:
            batch_op.drop_column("last_update")
    else:
        op.drop_column("node", "last_update")


def downgrade() -> None:
    conn = op.get_bind()
    op.add_column("node", sa.Column("last_update", sa.DateTime(), nullable=True))

    node = sa.table(
        "node",
        sa.column("id", sa.String()),
        sa.column("last_update", sa.DateTime()),
        sa.column("last_update_us", sa.BigInteger()),
    )

    rows = conn.execute(sa.select(node.c.id, node.c.last_update_us)).all()
    for node_id, last_update_us in rows:
        if last_update_us is None:
            continue
        dt = datetime.fromtimestamp(last_update_us / 1_000_000, tz=UTC).replace(tzinfo=None)
        conn.execute(sa.update(node).where(node.c.id == node_id).values(last_update=dt))

    if conn.dialect.name == "sqlite":
        with op.batch_alter_table("node", schema=None) as batch_op:
            batch_op.drop_index("idx_node_last_update_us")
            batch_op.drop_column("last_update_us")
    else:
        op.drop_index("idx_node_last_update_us", table_name="node")
        op.drop_column("node", "last_update_us")
