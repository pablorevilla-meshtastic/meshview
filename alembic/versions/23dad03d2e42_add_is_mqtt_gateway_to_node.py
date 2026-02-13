"""Add is_mqtt_gateway to node

Revision ID: 23dad03d2e42
Revises: a0c9c13e118f
Create Date: 2026-02-13 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "23dad03d2e42"
down_revision: str | None = "a0c9c13e118f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("node", sa.Column("is_mqtt_gateway", sa.Boolean(), nullable=True))


def downgrade() -> None:
    op.drop_column("node", "is_mqtt_gateway")
