"""task_views.public_token (publish to public link) (COS-167)

Revision ID: a1d5f8c3e269
Revises: f9c4e2b7a358
Create Date: 2026-06-21 14:55:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a1d5f8c3e269"
down_revision: str | None = "f9c4e2b7a358"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("task_views", sa.Column("public_token", sa.String(length=64), nullable=True))
    op.create_index("ix_task_views_public_token", "task_views", ["public_token"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_task_views_public_token", table_name="task_views")
    op.drop_column("task_views", "public_token")
