"""tasks.start_date (timeline/Gantt) (COS-115)

Revision ID: c9a4e7b2f185
Revises: b8f3d1c6e074
Create Date: 2026-06-21 21:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c9a4e7b2f185"
down_revision: str | None = "b8f3d1c6e074"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("tasks", sa.Column("start_date", sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column("tasks", "start_date")
