"""tasks.bot_assignee_id (agents as bot users) (COS-272)

Revision ID: d7b3f8a2c641
Revises: c6a1f9d4b730
Create Date: 2026-06-22 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d7b3f8a2c641"
down_revision: str | None = "c6a1f9d4b730"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("tasks", sa.Column("bot_assignee_id", sa.Uuid(), nullable=True))
    op.create_index("ix_tasks_bot_assignee_id", "tasks", ["bot_assignee_id"])
    op.create_foreign_key(
        op.f("fk_tasks_bot_assignee_id"),
        "tasks",
        "ai_users",
        ["bot_assignee_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_tasks_bot_assignee_id"), "tasks", type_="foreignkey")
    op.drop_index("ix_tasks_bot_assignee_id", table_name="tasks")
    op.drop_column("tasks", "bot_assignee_id")
