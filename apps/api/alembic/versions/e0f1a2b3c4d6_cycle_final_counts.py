"""cycle final counts (completed-cycle lock)

Revision ID: e0f1a2b3c4d6
Revises: d9e0f1a2b3c5
Create Date: 2026-06-21 01:25:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e0f1a2b3c4d6"
down_revision: str | None = "d9e0f1a2b3c5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("cycles", sa.Column("final_total_count", sa.Integer(), nullable=True))
    op.add_column("cycles", sa.Column("final_completed_count", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("cycles", "final_completed_count")
    op.drop_column("cycles", "final_total_count")
