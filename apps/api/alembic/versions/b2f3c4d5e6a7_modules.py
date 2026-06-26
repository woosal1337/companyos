"""modules (workstream grouping) + tasks.module_id

Revision ID: b2f3c4d5e6a7
Revises: a1c2e3f4b5d6
Create Date: 2026-06-20 11:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b2f3c4d5e6a7"
down_revision: str | None = "a1c2e3f4b5d6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "modules",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("lead_id", sa.Uuid(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("target_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
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
        sa.ForeignKeyConstraint(["org_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["lead_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_modules_org_id", "modules", ["org_id"])
    op.create_index("ix_modules_project_id", "modules", ["project_id"])

    op.add_column("tasks", sa.Column("module_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        op.f("fk_tasks_module_id_modules"),
        "tasks",
        "modules",
        ["module_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_tasks_module_id", "tasks", ["module_id"])


def downgrade() -> None:
    op.drop_index("ix_tasks_module_id", table_name="tasks")
    op.drop_constraint(op.f("fk_tasks_module_id_modules"), "tasks", type_="foreignkey")
    op.drop_column("tasks", "module_id")
    op.drop_index("ix_modules_project_id", table_name="modules")
    op.drop_index("ix_modules_org_id", table_name="modules")
    op.drop_table("modules")
