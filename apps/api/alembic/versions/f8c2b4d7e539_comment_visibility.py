"""comment visibility (internal/external)

Revision ID: f8c2b4d7e539
Revises: e7b1a3c6d428
Create Date: 2026-06-21 04:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f8c2b4d7e539"
down_revision: str | None = "e7b1a3c6d428"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "comments",
        sa.Column("visibility", sa.String(length=20), server_default="INTERNAL", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("comments", "visibility")
