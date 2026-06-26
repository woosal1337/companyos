"""project lifecycle timers (auto-archive / auto-close)

Revision ID: d3e4f5a6b7c9
Revises: c2d3e4f5a6b8
Create Date: 2026-06-20 22:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d3e4f5a6b7c9"
down_revision: str | None = "c2d3e4f5a6b8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("projects", sa.Column("auto_archive_days", sa.Integer(), nullable=True))
    op.add_column("projects", sa.Column("auto_close_days", sa.Integer(), nullable=True))
    op.add_column("projects", sa.Column("auto_close_status", sa.String(length=20), nullable=True))


def downgrade() -> None:
    op.drop_column("projects", "auto_close_status")
    op.drop_column("projects", "auto_close_days")
    op.drop_column("projects", "auto_archive_days")
