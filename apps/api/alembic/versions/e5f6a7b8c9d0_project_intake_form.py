"""project public intake form (intake_enabled + intake_token)

Revision ID: e5f6a7b8c9d0
Revises: d4f5e6a7b8c9
Create Date: 2026-06-20 12:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e5f6a7b8c9d0"
down_revision: str | None = "d4f5e6a7b8c9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "projects",
        sa.Column("intake_enabled", sa.Boolean(), server_default=sa.false(), nullable=False),
    )
    op.add_column("projects", sa.Column("intake_token", sa.String(length=64), nullable=True))
    op.create_index("ix_projects_intake_token", "projects", ["intake_token"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_projects_intake_token", table_name="projects")
    op.drop_column("projects", "intake_token")
    op.drop_column("projects", "intake_enabled")
