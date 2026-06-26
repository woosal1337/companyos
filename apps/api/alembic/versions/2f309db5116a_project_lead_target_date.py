"""project lead target_date

Revision ID: 2f309db5116a
Revises: 658473ef81b7
Create Date: 2026-06-14 22:55:42.393974

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "2f309db5116a"
down_revision: str | None = "658473ef81b7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("projects", sa.Column("lead_id", sa.Uuid(), nullable=True))
    op.add_column("projects", sa.Column("target_date", sa.Date(), nullable=True))
    op.create_foreign_key(
        op.f("fk_projects_lead_id_users"),
        "projects",
        "users",
        ["lead_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_projects_lead_id_users"), "projects", type_="foreignkey")
    op.drop_column("projects", "target_date")
    op.drop_column("projects", "lead_id")
