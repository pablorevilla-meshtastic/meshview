"""Add packet index on from_node_id, portnum and import_time_us

Revision ID: 4d2a7c9e1b30
Revises: e8f2c4b6d9a1
Create Date: 2026-10-26 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4d2a7c9e1b30"
down_revision: str | None = "e8f2c4b6d9a1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

INDEX_NAME = "idx_packet_from_node_portnum_time_us"


def upgrade() -> None:
    # Lets the node QR endpoint read a node's NODEINFO packets without scanning all its packets.
    inspector = sa.inspect(op.get_bind())
    if INDEX_NAME not in {index["name"] for index in inspector.get_indexes("packet")}:
        op.create_index(
            INDEX_NAME,
            "packet",
            ["from_node_id", "portnum", sa.text("import_time_us DESC")],
            unique=False,
        )


def downgrade() -> None:
    op.drop_index(INDEX_NAME, table_name="packet")
