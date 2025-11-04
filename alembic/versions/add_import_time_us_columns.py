"""add import_time_us columns

Revision ID: add_time_us_cols
Revises: c88468b7ab0b
Create Date: 2025-11-03 14:10:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'add_time_us_cols'
down_revision: str | None = 'c88468b7ab0b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Check if columns already exist, add them if they don't
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # Add import_time_us to packet table
    packet_columns = [col['name'] for col in inspector.get_columns('packet')]
    if 'import_time_us' not in packet_columns:
        with op.batch_alter_table('packet', schema=None) as batch_op:
            batch_op.add_column(sa.Column('import_time_us', sa.BigInteger(), nullable=True))
        op.create_index(
            'idx_packet_import_time_us', 'packet', [sa.text('import_time_us DESC')], unique=False
        )
        op.create_index(
            'idx_packet_from_node_time_us',
            'packet',
            ['from_node_id', sa.text('import_time_us DESC')],
            unique=False,
        )

    # Add import_time_us to packet_seen table
    packet_seen_columns = [col['name'] for col in inspector.get_columns('packet_seen')]
    if 'import_time_us' not in packet_seen_columns:
        with op.batch_alter_table('packet_seen', schema=None) as batch_op:
            batch_op.add_column(sa.Column('import_time_us', sa.BigInteger(), nullable=True))
        op.create_index(
            'idx_packet_seen_import_time_us', 'packet_seen', ['import_time_us'], unique=False
        )

    # Add import_time_us to traceroute table
    traceroute_columns = [col['name'] for col in inspector.get_columns('traceroute')]
    if 'import_time_us' not in traceroute_columns:
        with op.batch_alter_table('traceroute', schema=None) as batch_op:
            batch_op.add_column(sa.Column('import_time_us', sa.BigInteger(), nullable=True))
        op.create_index(
            'idx_traceroute_import_time_us', 'traceroute', ['import_time_us'], unique=False
        )


def downgrade() -> None:
    # Drop indexes and columns
    op.drop_index('idx_traceroute_import_time_us', table_name='traceroute')
    with op.batch_alter_table('traceroute', schema=None) as batch_op:
        batch_op.drop_column('import_time_us')

    op.drop_index('idx_packet_seen_import_time_us', table_name='packet_seen')
    with op.batch_alter_table('packet_seen', schema=None) as batch_op:
        batch_op.drop_column('import_time_us')

    op.drop_index('idx_packet_from_node_time_us', table_name='packet')
    op.drop_index('idx_packet_import_time_us', table_name='packet')
    with op.batch_alter_table('packet', schema=None) as batch_op:
        batch_op.drop_column('import_time_us')
