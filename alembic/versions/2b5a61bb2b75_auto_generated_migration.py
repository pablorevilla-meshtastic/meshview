"""Add first_seen_us and last_seen_us to node table

Revision ID: 2b5a61bb2b75
Revises: ac311b3782a1
Create Date: 2025-11-05 15:19:13.446724

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2b5a61bb2b75'
down_revision: str | None = 'ac311b3782a1'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Add microsecond epoch timestamp columns for first and last seen times
    op.add_column('node', sa.Column('first_seen_us', sa.BigInteger(), nullable=True))
    op.add_column('node', sa.Column('last_seen_us', sa.BigInteger(), nullable=True))
    op.create_index('idx_node_first_seen_us', 'node', ['first_seen_us'], unique=False)
    op.create_index('idx_node_last_seen_us', 'node', ['last_seen_us'], unique=False)


def downgrade() -> None:
    # Remove the microsecond epoch timestamp columns and their indexes
    op.drop_index('idx_node_last_seen_us', table_name='node')
    op.drop_index('idx_node_first_seen_us', table_name='node')
    op.drop_column('node', 'last_seen_us')
    op.drop_column('node', 'first_seen_us')
