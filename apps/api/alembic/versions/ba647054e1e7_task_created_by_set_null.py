"""task created_by set null

Revision ID: ba647054e1e7
Revises: 981ab3b2a8a6
Create Date: 2026-06-11 21:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "ba647054e1e7"
down_revision: str | None = "981ab3b2a8a6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("tasks", "created_by", existing_type=sa.Uuid(), nullable=True)
    op.drop_constraint(op.f("fk_tasks_created_by_users"), "tasks", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_tasks_created_by_users"),
        "tasks",
        "users",
        ["created_by"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_tasks_created_by_users"), "tasks", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_tasks_created_by_users"),
        "tasks",
        "users",
        ["created_by"],
        ["id"],
        ondelete="CASCADE",
    )
    op.alter_column("tasks", "created_by", existing_type=sa.Uuid(), nullable=False)
