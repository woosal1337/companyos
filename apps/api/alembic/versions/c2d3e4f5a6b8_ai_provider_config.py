"""ai provider config: base_url/region/models (BYO-LLM)

Revision ID: c2d3e4f5a6b8
Revises: b1c2d3e4f5a7
Create Date: 2026-06-20 22:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c2d3e4f5a6b8"
down_revision: str | None = "b1c2d3e4f5a7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("ai_provider_keys", sa.Column("base_url", sa.String(length=500), nullable=True))
    op.add_column("ai_provider_keys", sa.Column("region", sa.String(length=50), nullable=True))
    op.add_column("ai_provider_keys", sa.Column("chat_model", sa.String(length=100), nullable=True))
    op.add_column(
        "ai_provider_keys", sa.Column("embedding_model", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "ai_provider_keys", sa.Column("embedding_dimensions", sa.Integer(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("ai_provider_keys", "embedding_dimensions")
    op.drop_column("ai_provider_keys", "embedding_model")
    op.drop_column("ai_provider_keys", "chat_model")
    op.drop_column("ai_provider_keys", "region")
    op.drop_column("ai_provider_keys", "base_url")
