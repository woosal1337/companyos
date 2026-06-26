"""project network (visibility)

Revision ID: f0a1b2c3d4e5
Revises: b0c1d2e3f4a5
Create Date: 2026-06-20 10:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f0a1b2c3d4e5"
down_revision: str | None = "b0c1d2e3f4a5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "projects",
        sa.Column(
            "network",
            sa.String(length=20),
            server_default="PRIVATE",
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("projects", "network")
