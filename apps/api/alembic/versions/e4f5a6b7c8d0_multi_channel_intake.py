"""multi-channel intake: task channel + project in-app toggle

Revision ID: e4f5a6b7c8d0
Revises: d3e4f5a6b7c9
Create Date: 2026-06-20 23:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e4f5a6b7c8d0"
down_revision: str | None = "d3e4f5a6b7c9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("tasks", sa.Column("intake_channel", sa.String(length=20), nullable=True))
    op.add_column(
        "projects",
        sa.Column("intake_inapp_enabled", sa.Boolean(), server_default=sa.false(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("projects", "intake_inapp_enabled")
    op.drop_column("tasks", "intake_channel")
