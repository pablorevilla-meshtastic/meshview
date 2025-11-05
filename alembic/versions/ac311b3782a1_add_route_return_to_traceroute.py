"""add route_return to traceroute

Revision ID: ac311b3782a1
Revises: 1717fa5c6545
Create Date: 2025-11-04 20:28:33.174137

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ac311b3782a1'
down_revision: str | None = '1717fa5c6545'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Add route_return column to traceroute table
    with op.batch_alter_table('traceroute', schema=None) as batch_op:
        batch_op.add_column(sa.Column('route_return', sa.LargeBinary(), nullable=True))


def downgrade() -> None:
    # Remove route_return column from traceroute table
    with op.batch_alter_table('traceroute', schema=None) as batch_op:
        batch_op.drop_column('route_return')
