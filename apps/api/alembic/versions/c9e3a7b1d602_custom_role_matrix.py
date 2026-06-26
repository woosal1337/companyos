"""custom_roles.matrix (per-resource permission matrix) (COS-182)

Revision ID: c9e3a7b1d602
Revises: b8d2f6a0c591
Create Date: 2026-06-22 17:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "c9e3a7b1d602"
down_revision: str | None = "b8d2f6a0c591"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "custom_roles",
        sa.Column(
            "matrix",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("custom_roles", "matrix")
