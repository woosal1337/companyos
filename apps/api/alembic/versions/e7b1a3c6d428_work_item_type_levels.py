"""work_item_type_levels (type hierarchy)

Revision ID: e7b1a3c6d428
Revises: d6a0f2e5b317
Create Date: 2026-06-21 04:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e7b1a3c6d428"
down_revision: str | None = "d6a0f2e5b317"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "work_item_type_levels",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("kind", sa.String(length=20), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
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
            name=op.f("fk_work_item_type_levels_org_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_work_item_type_levels")),
        sa.UniqueConstraint("org_id", "kind", name=op.f("uq_work_item_type_levels_org_kind")),
    )
    op.create_index("ix_work_item_type_levels_org_id", "work_item_type_levels", ["org_id"])


def downgrade() -> None:
    op.drop_index("ix_work_item_type_levels_org_id", table_name="work_item_type_levels")
    op.drop_table("work_item_type_levels")
