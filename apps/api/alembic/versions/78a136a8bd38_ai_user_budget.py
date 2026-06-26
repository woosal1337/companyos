"""ai user budget

Revision ID: 78a136a8bd38
Revises: 8ea888da7919
Create Date: 2026-06-15 12:05:15.448413

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "78a136a8bd38"
down_revision: str | None = "8ea888da7919"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("ai_users", sa.Column("budget_monthly_cents", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("ai_users", "budget_monthly_cents")
