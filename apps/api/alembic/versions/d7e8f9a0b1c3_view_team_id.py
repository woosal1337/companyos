"""task_views.team_id (teamspace-scoped views)

Revision ID: d7e8f9a0b1c3
Revises: f1a2b3c4d5e8
Create Date: 2026-06-20 19:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d7e8f9a0b1c3"
down_revision: str | None = "f1a2b3c4d5e8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("task_views", sa.Column("team_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        op.f("fk_task_views_team_id"),
        "task_views",
        "teams",
        ["team_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index("ix_task_views_team_id", "task_views", ["team_id"])


def downgrade() -> None:
    op.drop_index("ix_task_views_team_id", table_name="task_views")
    op.drop_constraint(op.f("fk_task_views_team_id"), "task_views", type_="foreignkey")
    op.drop_column("task_views", "team_id")
