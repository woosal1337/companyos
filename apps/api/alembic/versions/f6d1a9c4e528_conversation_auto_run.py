"""ai_conversations.auto_run (COS-221)

Revision ID: f6d1a9c4e528
Revises: e5b9d2c7f413
Create Date: 2026-06-21 18:10:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f6d1a9c4e528"
down_revision: str | None = "e5b9d2c7f413"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "ai_conversations",
        sa.Column("auto_run", sa.Boolean(), server_default=sa.false(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("ai_conversations", "auto_run")
