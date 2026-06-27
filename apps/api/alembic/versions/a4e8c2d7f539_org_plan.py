"""organizations.plan (editions) (COS-197)

Revision ID: a4e8c2d7f539
Revises: f3d7b2c9e418
Create Date: 2026-06-22 10:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a4e8c2d7f539"
down_revision: str | None = "f3d7b2c9e418"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "organizations",
        sa.Column("plan", sa.String(length=20), server_default="free", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("organizations", "plan")
