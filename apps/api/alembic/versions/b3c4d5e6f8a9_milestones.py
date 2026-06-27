"""milestones + task.milestone_id

Revision ID: b3c4d5e6f8a9
Revises: a2b3c4d5e6f8
Create Date: 2026-06-19 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b3c4d5e6f8a9"
down_revision: str | None = "a2b3c4d5e6f8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "milestones",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("target_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_milestones_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_milestones_project_id_projects"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_milestones")),
    )
    op.create_index(op.f("ix_milestones_org_id"), "milestones", ["org_id"], unique=False)
    op.create_index(op.f("ix_milestones_project_id"), "milestones", ["project_id"], unique=False)
    op.add_column("tasks", sa.Column("milestone_id", sa.Uuid(), nullable=True))
    op.create_index(op.f("ix_tasks_milestone_id"), "tasks", ["milestone_id"], unique=False)
    op.create_foreign_key(
        op.f("fk_tasks_milestone_id_milestones"),
        "tasks",
        "milestones",
        ["milestone_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_tasks_milestone_id_milestones"), "tasks", type_="foreignkey")
    op.drop_index(op.f("ix_tasks_milestone_id"), table_name="tasks")
    op.drop_column("tasks", "milestone_id")
    op.drop_index(op.f("ix_milestones_project_id"), table_name="milestones")
    op.drop_index(op.f("ix_milestones_org_id"), table_name="milestones")
    op.drop_table("milestones")
