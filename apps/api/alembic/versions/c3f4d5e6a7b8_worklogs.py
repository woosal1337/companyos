"""worklogs (time tracking)

Revision ID: c3f4d5e6a7b8
Revises: b2f3c4d5e6a7
Create Date: 2026-06-20 11:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c3f4d5e6a7b8"
down_revision: str | None = "b2f3c4d5e6a7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "worklogs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("task_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("minutes", sa.Integer(), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("logged_at", sa.Date(), nullable=False),
        sa.Column("user_name", sa.String(length=255), nullable=True),
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
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_worklogs_org_id", "worklogs", ["org_id"])
    op.create_index("ix_worklogs_project_id", "worklogs", ["project_id"])
    op.create_index("ix_worklogs_task_id", "worklogs", ["task_id"])


def downgrade() -> None:
    op.drop_index("ix_worklogs_task_id", table_name="worklogs")
    op.drop_index("ix_worklogs_project_id", table_name="worklogs")
    op.drop_index("ix_worklogs_org_id", table_name="worklogs")
    op.drop_table("worklogs")
