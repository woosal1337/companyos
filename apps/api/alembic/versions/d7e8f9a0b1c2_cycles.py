"""cycles + tasks.cycle_id

Revision ID: d7e8f9a0b1c2
Revises: c6d7e8f9a0b1
Create Date: 2026-06-19 03:40:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d7e8f9a0b1c2"
down_revision: str | None = "c6d7e8f9a0b1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "cycles",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
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
            name=op.f("fk_cycles_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_cycles_project_id_projects"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cycles")),
    )
    op.create_index(op.f("ix_cycles_org_id"), "cycles", ["org_id"], unique=False)
    op.create_index(op.f("ix_cycles_project_id"), "cycles", ["project_id"], unique=False)

    op.add_column("tasks", sa.Column("cycle_id", sa.Uuid(), nullable=True))
    op.create_index(op.f("ix_tasks_cycle_id"), "tasks", ["cycle_id"], unique=False)
    op.create_foreign_key(
        op.f("fk_tasks_cycle_id_cycles"),
        "tasks",
        "cycles",
        ["cycle_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_tasks_cycle_id_cycles"), "tasks", type_="foreignkey")
    op.drop_index(op.f("ix_tasks_cycle_id"), table_name="tasks")
    op.drop_column("tasks", "cycle_id")
    op.drop_index(op.f("ix_cycles_project_id"), table_name="cycles")
    op.drop_index(op.f("ix_cycles_org_id"), table_name="cycles")
    op.drop_table("cycles")
