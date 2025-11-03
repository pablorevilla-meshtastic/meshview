"""add_microsecond_timestamp_columns

Adds import_time_us INTEGER columns to packet, packet_seen, and traceroute tables.
This implements the changes described in GitHub issue #55:
- Adds import_time_us INTEGER columns to track microsecond-precision timestamps
- Populates new columns from existing import_time datetime values
- Creates indexes on the new columns for performance

Revision ID: fb5781f0c470
Revises: 1717fa5c6545
Create Date: 2025-11-03 12:59:03.202458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb5781f0c470'
down_revision: Union[str, None] = '1717fa5c6545'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add import_time_us columns and populate them from existing data."""

    # Add import_time_us column to packet table
    with op.batch_alter_table('packet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('import_time_us', sa.Integer(), nullable=True))

    # Add import_time_us column to packet_seen table
    with op.batch_alter_table('packet_seen', schema=None) as batch_op:
        batch_op.add_column(sa.Column('import_time_us', sa.Integer(), nullable=True))

    # Add import_time_us column to traceroute table
    with op.batch_alter_table('traceroute', schema=None) as batch_op:
        batch_op.add_column(sa.Column('import_time_us', sa.Integer(), nullable=True))

    # Populate packet.import_time_us from existing import_time data
    # Note: import_time is stored as local time text, but we convert to UTC timestamp
    # strftime('%s', ...) interprets the datetime as UTC
    op.execute("""
        UPDATE packet
        SET import_time_us =
            CAST((strftime('%s', import_time) || substr(import_time, 21, 6)) AS INTEGER)
        WHERE import_time IS NOT NULL
    """)

    # Populate packet_seen.import_time_us
    op.execute("""
        UPDATE packet_seen
        SET import_time_us =
            CAST((strftime('%s', import_time) || substr(import_time, 21, 6)) AS INTEGER)
        WHERE import_time IS NOT NULL
    """)

    # Populate traceroute.import_time_us
    op.execute("""
        UPDATE traceroute
        SET import_time_us =
            CAST((strftime('%s', import_time) || substr(import_time, 21, 6)) AS INTEGER)
        WHERE import_time IS NOT NULL
    """)

    # Create indexes on the new columns
    op.create_index('idx_packet_import_time_us', 'packet', [sa.text('import_time_us DESC')])
    op.create_index('idx_packet_from_node_time_us', 'packet', ['from_node_id', sa.text('import_time_us DESC')])
    op.create_index('idx_packet_seen_import_time_us', 'packet_seen', ['import_time_us'])
    op.create_index('idx_traceroute_import_time_us', 'traceroute', ['import_time_us'])


def downgrade() -> None:
    """Remove import_time_us columns and their indexes."""

    # Drop indexes
    op.drop_index('idx_traceroute_import_time_us', table_name='traceroute')
    op.drop_index('idx_packet_seen_import_time_us', table_name='packet_seen')
    op.drop_index('idx_packet_from_node_time_us', table_name='packet')
    op.drop_index('idx_packet_import_time_us', table_name='packet')

    # Drop columns
    with op.batch_alter_table('traceroute', schema=None) as batch_op:
        batch_op.drop_column('import_time_us')

    with op.batch_alter_table('packet_seen', schema=None) as batch_op:
        batch_op.drop_column('import_time_us')

    with op.batch_alter_table('packet', schema=None) as batch_op:
        batch_op.drop_column('import_time_us')
