"""not_duplicate_pairs (duplicate suppression)

Revision ID: c2f5e7a0d163
Revises: b1e4d6f9c052
Create Date: 2026-06-21 06:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c2f5e7a0d163"
down_revision: str | None = "b1e4d6f9c052"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "not_duplicate_pairs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("task_a_id", sa.Uuid(), nullable=False),
        sa.Column("task_b_id", sa.Uuid(), nullable=False),
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
            name=op.f("fk_not_duplicate_pairs_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task_a_id"],
            ["tasks.id"],
            name=op.f("fk_not_duplicate_pairs_task_a_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task_b_id"],
            ["tasks.id"],
            name=op.f("fk_not_duplicate_pairs_task_b_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_not_duplicate_pairs")),
        sa.UniqueConstraint(
            "org_id", "task_a_id", "task_b_id", name=op.f("uq_not_duplicate_pairs_pair")
        ),
    )
    op.create_index("ix_not_duplicate_pairs_org_id", "not_duplicate_pairs", ["org_id"])


def downgrade() -> None:
    op.drop_index("ix_not_duplicate_pairs_org_id", table_name="not_duplicate_pairs")
    op.drop_table("not_duplicate_pairs")
