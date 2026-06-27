"""ai chat pinned + message feedback (COS-231)

Revision ID: e5b9d2c7f413
Revises: d4a8c1f6b592
Create Date: 2026-06-21 17:20:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e5b9d2c7f413"
down_revision: str | None = "d4a8c1f6b592"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "ai_conversations",
        sa.Column("pinned", sa.Boolean(), server_default=sa.false(), nullable=False),
    )
    op.add_column(
        "ai_chat_messages",
        sa.Column("feedback", sa.SmallInteger(), server_default="0", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("ai_chat_messages", "feedback")
    op.drop_column("ai_conversations", "pinned")
