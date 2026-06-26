"""users.locale (i18n preference) (COS-146)

Revision ID: c3f7a0d5e481
Revises: b2e6f9c4d370
Create Date: 2026-06-21 16:10:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c3f7a0d5e481"
down_revision: str | None = "b2e6f9c4d370"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("locale", sa.String(length=10), server_default="en", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("users", "locale")
