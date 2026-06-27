"""workflow transitions (allowed-transition guardrails)

Revision ID: c9d0e1f2a3b4
Revises: b8c9d0e1f2a3
Create Date: 2026-06-20 14:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c9d0e1f2a3b4"
down_revision: str | None = "b8c9d0e1f2a3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "workflow_transitions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("from_status_id", sa.Uuid(), nullable=False),
        sa.Column("to_status_id", sa.Uuid(), nullable=False),
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
        sa.ForeignKeyConstraint(["from_status_id"], ["workflow_statuses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["to_status_id"], ["workflow_statuses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("org_id", "from_status_id", "to_status_id"),
    )
    op.create_index("ix_workflow_transitions_org_id", "workflow_transitions", ["org_id"])
    op.create_index(
        "ix_workflow_transitions_from_status_id", "workflow_transitions", ["from_status_id"]
    )
    op.create_index(
        "ix_workflow_transitions_to_status_id", "workflow_transitions", ["to_status_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_workflow_transitions_to_status_id", table_name="workflow_transitions")
    op.drop_index("ix_workflow_transitions_from_status_id", table_name="workflow_transitions")
    op.drop_index("ix_workflow_transitions_org_id", table_name="workflow_transitions")
    op.drop_table("workflow_transitions")
