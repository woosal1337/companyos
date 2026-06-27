"""recurring_task_rules (recurring work items)

Revision ID: f5c8a1b3e927
Revises: e4b7a9c2f385
Create Date: 2026-06-21 07:50:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f5c8a1b3e927"
down_revision: str | None = "e4b7a9c2f385"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "recurring_task_rules",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("priority", sa.String(length=20), nullable=False),
        sa.Column("kind", sa.String(length=20), nullable=False),
        sa.Column("assignee_id", sa.Uuid(), nullable=True),
        sa.Column("interval_days", sa.Integer(), nullable=False),
        sa.Column("next_run_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
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
            name=op.f("fk_recurring_task_rules_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_recurring_task_rules_project_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["assignee_id"],
            ["users.id"],
            name=op.f("fk_recurring_task_rules_assignee_id"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_recurring_task_rules")),
    )
    op.create_index("ix_recurring_task_rules_org_id", "recurring_task_rules", ["org_id"])
    op.create_index("ix_recurring_task_rules_project_id", "recurring_task_rules", ["project_id"])
    op.create_index("ix_recurring_task_rules_next_run_at", "recurring_task_rules", ["next_run_at"])


def downgrade() -> None:
    op.drop_index("ix_recurring_task_rules_next_run_at", table_name="recurring_task_rules")
    op.drop_index("ix_recurring_task_rules_project_id", table_name="recurring_task_rules")
    op.drop_index("ix_recurring_task_rules_org_id", table_name="recurring_task_rules")
    op.drop_table("recurring_task_rules")
