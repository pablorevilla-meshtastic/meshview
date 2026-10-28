"""add last altitude to node

Revision ID: 44612e74a798
Revises: 4d2a7c9e1b30
Create Date: 2026-10-28 10:37:11.340792

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '44612e74a798'
down_revision: str | None = '4d2a7c9e1b30'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("node") as batch_op:
        batch_op.add_column(sa.Column("last_altitude", sa.BigInteger(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("node") as batch_op:
        batch_op.drop_column("last_altitude")
