"""Add example table

Revision ID: 1717fa5c6545
Revises: c88468b7ab0b
Create Date: 2025-10-26 20:59:04.347066

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1717fa5c6545'
down_revision: str | None = 'add_time_us_cols'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create example table with sample columns."""
    op.create_table(
        'example',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('value', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column(
            'created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')
        ),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create an index on the name column for faster lookups
    op.create_index('idx_example_name', 'example', ['name'])


def downgrade() -> None:
    """Remove example table."""
    op.drop_index('idx_example_name', table_name='example')
    op.drop_table('example')
