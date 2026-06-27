"""project default_assignee_id

Revision ID: c2d3e4f5a6b7
Revises: b1c2d3e4f5a6
Create Date: 2026-06-19 06:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c2d3e4f5a6b7"
down_revision: str | None = "b1c2d3e4f5a6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("projects", sa.Column("default_assignee_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        op.f("fk_projects_default_assignee_id_users"),
        "projects",
        "users",
        ["default_assignee_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_projects_default_assignee_id_users"), "projects", type_="foreignkey"
    )
    op.drop_column("projects", "default_assignee_id")
