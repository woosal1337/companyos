"""worklog approvals + project policy flag

Revision ID: d6a0f2e5b317
Revises: c5f9e1d4a206
Create Date: 2026-06-21 03:25:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d6a0f2e5b317"
down_revision: str | None = "c5f9e1d4a206"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "projects",
        sa.Column(
            "worklog_approval_required",
            sa.Boolean(),
            server_default=sa.false(),
            nullable=False,
        ),
    )
    op.add_column(
        "worklogs",
        sa.Column(
            "approval_status",
            sa.String(length=20),
            server_default="APPROVED",
            nullable=False,
        ),
    )
    op.add_column("worklogs", sa.Column("approver_id", sa.Uuid(), nullable=True))
    op.add_column("worklogs", sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("worklogs", sa.Column("decision_note", sa.Text(), nullable=True))
    op.create_foreign_key(
        op.f("fk_worklogs_approver_id"),
        "worklogs",
        "users",
        ["approver_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_worklogs_approver_id"), "worklogs", type_="foreignkey")
    op.drop_column("worklogs", "decision_note")
    op.drop_column("worklogs", "decided_at")
    op.drop_column("worklogs", "approver_id")
    op.drop_column("worklogs", "approval_status")
    op.drop_column("projects", "worklog_approval_required")
