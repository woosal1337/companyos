"""task_description_versions (description edit history)

Revision ID: d9e0f1a2b3c5
Revises: c8d9e0f1a2b4
Create Date: 2026-06-21 01:05:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d9e0f1a2b3c5"
down_revision: str | None = "c8d9e0f1a2b4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "task_description_versions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("task_id", sa.Uuid(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("edited_by", sa.Uuid(), nullable=True),
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
            name=op.f("fk_task_description_versions_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            name=op.f("fk_task_description_versions_task_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["edited_by"],
            ["users.id"],
            name=op.f("fk_task_description_versions_edited_by"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_task_description_versions")),
    )
    op.create_index("ix_task_description_versions_org_id", "task_description_versions", ["org_id"])
    op.create_index(
        "ix_task_description_versions_task_id", "task_description_versions", ["task_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_task_description_versions_task_id", table_name="task_description_versions")
    op.drop_index("ix_task_description_versions_org_id", table_name="task_description_versions")
    op.drop_table("task_description_versions")
