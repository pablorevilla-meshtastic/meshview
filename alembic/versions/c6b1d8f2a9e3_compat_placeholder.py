"""Compatibility placeholder for removed revision c6b1d8f2a9e3.

Revision ID: c6b1d8f2a9e3
Revises: 4f1d2a9c8b71
Create Date: 2026-03-05 00:00:00.000000
"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "c6b1d8f2a9e3"
down_revision: str | None = "4f1d2a9c8b71"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
