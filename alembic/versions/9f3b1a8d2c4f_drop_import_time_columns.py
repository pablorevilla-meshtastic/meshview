"""Drop import_time columns.

Revision ID: 9f3b1a8d2c4f
Revises: 2b5a61bb2b75
Create Date: 2026-01-09 09:55:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9f3b1a8d2c4f"
down_revision: str | None = "2b5a61bb2b75"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    packet_indexes = {idx["name"] for idx in inspector.get_indexes("packet")}
    packet_columns = {col["name"] for col in inspector.get_columns("packet")}

    with op.batch_alter_table("packet", schema=None) as batch_op:
        if "idx_packet_import_time" in packet_indexes:
            batch_op.drop_index("idx_packet_import_time")
        if "idx_packet_from_node_time" in packet_indexes:
            batch_op.drop_index("idx_packet_from_node_time")
        if "import_time" in packet_columns:
            batch_op.drop_column("import_time")

    packet_seen_columns = {col["name"] for col in inspector.get_columns("packet_seen")}
    with op.batch_alter_table("packet_seen", schema=None) as batch_op:
        if "import_time" in packet_seen_columns:
            batch_op.drop_column("import_time")

    traceroute_indexes = {idx["name"] for idx in inspector.get_indexes("traceroute")}
    traceroute_columns = {col["name"] for col in inspector.get_columns("traceroute")}
    with op.batch_alter_table("traceroute", schema=None) as batch_op:
        if "idx_traceroute_import_time" in traceroute_indexes:
            batch_op.drop_index("idx_traceroute_import_time")
        if "import_time" in traceroute_columns:
            batch_op.drop_column("import_time")


def downgrade() -> None:
    with op.batch_alter_table("traceroute", schema=None) as batch_op:
        batch_op.add_column(sa.Column("import_time", sa.DateTime(), nullable=True))
        batch_op.create_index("idx_traceroute_import_time", ["import_time"], unique=False)

    with op.batch_alter_table("packet_seen", schema=None) as batch_op:
        batch_op.add_column(sa.Column("import_time", sa.DateTime(), nullable=True))

    with op.batch_alter_table("packet", schema=None) as batch_op:
        batch_op.add_column(sa.Column("import_time", sa.DateTime(), nullable=True))
        batch_op.create_index("idx_packet_import_time", [sa.text("import_time DESC")], unique=False)
        batch_op.create_index(
            "idx_packet_from_node_time",
            ["from_node_id", sa.text("import_time DESC")],
            unique=False,
        )
