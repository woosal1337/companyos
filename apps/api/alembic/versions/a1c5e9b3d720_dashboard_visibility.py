"""dashboards.visibility (private/workspace sharing) (COS-134)

Revision ID: a1c5e9b3d720
Revises: f9b2d6c4a815
Create Date: 2026-06-22 13:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a1c5e9b3d720"
down_revision: str | None = "f9b2d6c4a815"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "dashboards",
        sa.Column("visibility", sa.String(length=20), server_default="PRIVATE", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("dashboards", "visibility")
