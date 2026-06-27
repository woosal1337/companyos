"""cycle lifecycle (status + start/complete timestamps)

Revision ID: a2b3c4d5e6f8
Revises: f1a2b3c4d5e7
Create Date: 2026-06-19 11:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a2b3c4d5e6f8"
down_revision: str | None = "f1a2b3c4d5e7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "cycles",
        sa.Column(
            "status",
            sa.String(length=20),
            server_default="upcoming",
            nullable=False,
        ),
    )
    op.add_column("cycles", sa.Column("started_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("cycles", sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("cycles", "completed_at")
    op.drop_column("cycles", "started_at")
    op.drop_column("cycles", "status")
