"""task external_source / external_id (import idempotency)

Revision ID: c8d9e0f1a2b4
Revises: b7c8d9e0f1a3
Create Date: 2026-06-21 00:45:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c8d9e0f1a2b4"
down_revision: str | None = "b7c8d9e0f1a3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("tasks", sa.Column("external_source", sa.String(length=50), nullable=True))
    op.add_column("tasks", sa.Column("external_id", sa.String(length=255), nullable=True))
    op.create_index(
        "uq_tasks_external_ref",
        "tasks",
        ["org_id", "external_source", "external_id"],
        unique=True,
        postgresql_where=sa.text("external_id IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("uq_tasks_external_ref", table_name="tasks")
    op.drop_column("tasks", "external_id")
    op.drop_column("tasks", "external_source")
