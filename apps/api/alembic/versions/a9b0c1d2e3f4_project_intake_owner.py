"""project intake_owner_id

Revision ID: a9b0c1d2e3f4
Revises: f8a9b0c1d2e3
Create Date: 2026-06-20 08:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a9b0c1d2e3f4"
down_revision: str | None = "f8a9b0c1d2e3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("projects", sa.Column("intake_owner_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        op.f("fk_projects_intake_owner_id_users"),
        "projects",
        "users",
        ["intake_owner_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_projects_intake_owner_id_users"), "projects", type_="foreignkey")
    op.drop_column("projects", "intake_owner_id")
