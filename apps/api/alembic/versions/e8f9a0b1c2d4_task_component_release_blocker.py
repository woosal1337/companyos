"""task component + release_blocker (severity-vs-priority extras)

Revision ID: e8f9a0b1c2d4
Revises: d7e8f9a0b1c3
Create Date: 2026-06-20 20:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e8f9a0b1c2d4"
down_revision: str | None = "d7e8f9a0b1c3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("tasks", sa.Column("component", sa.String(length=100), nullable=True))
    op.add_column(
        "tasks",
        sa.Column("release_blocker", sa.Boolean(), server_default=sa.false(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("tasks", "release_blocker")
    op.drop_column("tasks", "component")
