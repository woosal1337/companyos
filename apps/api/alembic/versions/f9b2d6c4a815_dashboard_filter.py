"""dashboards.filter (3-level PQL filter layering) (COS-104)

Revision ID: f9b2d6c4a815
Revises: e8c4a2f9b310
Create Date: 2026-06-22 13:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f9b2d6c4a815"
down_revision: str | None = "e8c4a2f9b310"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("dashboards", sa.Column("filter", sa.String(length=2000), nullable=True))


def downgrade() -> None:
    op.drop_column("dashboards", "filter")
