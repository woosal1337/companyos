"""task_schedule_links (scheduling dependencies) (COS-68)

Revision ID: f9c4e2b7a358
Revises: e8b3d6f9a247
Create Date: 2026-06-21 14:20:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f9c4e2b7a358"
down_revision: str | None = "e8b3d6f9a247"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "task_schedule_links",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("predecessor_id", sa.Uuid(), nullable=False),
        sa.Column("successor_id", sa.Uuid(), nullable=False),
        sa.Column("dependency_type", sa.String(length=20), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=True),
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
            name=op.f("fk_task_schedule_links_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["predecessor_id"],
            ["tasks.id"],
            name=op.f("fk_task_schedule_links_predecessor_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["successor_id"],
            ["tasks.id"],
            name=op.f("fk_task_schedule_links_successor_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            name=op.f("fk_task_schedule_links_created_by"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_task_schedule_links")),
        sa.UniqueConstraint(
            "predecessor_id",
            "successor_id",
            "dependency_type",
            name=op.f("uq_task_schedule_links_pair"),
        ),
    )
    op.create_index("ix_task_schedule_links_org_id", "task_schedule_links", ["org_id"])
    op.create_index(
        "ix_task_schedule_links_predecessor_id", "task_schedule_links", ["predecessor_id"]
    )
    op.create_index("ix_task_schedule_links_successor_id", "task_schedule_links", ["successor_id"])


def downgrade() -> None:
    op.drop_table("task_schedule_links")
