"""notification email_sent_at

Revision ID: 62a14e0f61ff
Revises: 18430ba19baf
Create Date: 2026-06-14 23:41:56.809267

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "62a14e0f61ff"
down_revision: str | None = "18430ba19baf"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "notifications", sa.Column("email_sent_at", sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("notifications", "email_sent_at")
