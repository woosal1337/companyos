"""personal_access_tokens.description (COS-275)

Revision ID: a7e2c5d9b613
Revises: f6d1a9c4e528
Create Date: 2026-06-21 19:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a7e2c5d9b613"
down_revision: str | None = "f6d1a9c4e528"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "personal_access_tokens",
        sa.Column("description", sa.String(length=500), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("personal_access_tokens", "description")
