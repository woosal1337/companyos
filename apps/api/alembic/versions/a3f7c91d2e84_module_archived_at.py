"""module archived_at (archive/restore)

Revision ID: a3f7c91d2e84
Revises: e0f1a2b3c4d6
Create Date: 2026-06-21 01:45:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a3f7c91d2e84"
down_revision: str | None = "e0f1a2b3c4d6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("modules", sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("modules", "archived_at")
