"""task workflow_status_id (status<->workflow wiring)

Revision ID: b8c9d0e1f2a3
Revises: a7b8c9d0e1f2
Create Date: 2026-06-20 14:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b8c9d0e1f2a3"
down_revision: str | None = "a7b8c9d0e1f2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_BACKFILL = {
    "BACKLOG": "Backlog",
    "TODO": "Todo",
    "IN_PROGRESS": "In Progress",
    "IN_REVIEW": "In Review",
    "DONE": "Done",
    "CANCELLED": "Cancelled",
    "DUPLICATE": "Cancelled",
}


def upgrade() -> None:
    op.add_column("tasks", sa.Column("workflow_status_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        op.f("fk_tasks_workflow_status_id_workflow_statuses"),
        "tasks",
        "workflow_statuses",
        ["workflow_status_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_tasks_workflow_status_id", "tasks", ["workflow_status_id"])

    for status_name, workflow_name in _BACKFILL.items():
        op.execute(
            sa.text(
                "UPDATE tasks t SET workflow_status_id = ws.id "
                "FROM workflow_statuses ws "
                "WHERE ws.org_id = t.org_id AND ws.team_id IS NULL "
                "AND ws.name = :wname AND t.status = :sname "
                "AND t.workflow_status_id IS NULL"
            ).bindparams(wname=workflow_name, sname=status_name)
        )


def downgrade() -> None:
    op.drop_index("ix_tasks_workflow_status_id", table_name="tasks")
    op.drop_constraint(
        op.f("fk_tasks_workflow_status_id_workflow_statuses"), "tasks", type_="foreignkey"
    )
    op.drop_column("tasks", "workflow_status_id")
