"""milestone grouping: cycles.milestone_id + modules.milestone_id

Revision ID: e4b7a9c2f385
Revises: d3a6f8b1e274
Create Date: 2026-06-21 07:10:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e4b7a9c2f385"
down_revision: str | None = "d3a6f8b1e274"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("cycles", sa.Column("milestone_id", sa.Uuid(), nullable=True))
    op.create_index("ix_cycles_milestone_id", "cycles", ["milestone_id"])
    op.create_foreign_key(
        op.f("fk_cycles_milestone_id"),
        "cycles",
        "milestones",
        ["milestone_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.add_column("modules", sa.Column("milestone_id", sa.Uuid(), nullable=True))
    op.create_index("ix_modules_milestone_id", "modules", ["milestone_id"])
    op.create_foreign_key(
        op.f("fk_modules_milestone_id"),
        "modules",
        "milestones",
        ["milestone_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_modules_milestone_id"), "modules", type_="foreignkey")
    op.drop_index("ix_modules_milestone_id", table_name="modules")
    op.drop_column("modules", "milestone_id")
    op.drop_constraint(op.f("fk_cycles_milestone_id"), "cycles", type_="foreignkey")
    op.drop_index("ix_cycles_milestone_id", table_name="cycles")
    op.drop_column("cycles", "milestone_id")
