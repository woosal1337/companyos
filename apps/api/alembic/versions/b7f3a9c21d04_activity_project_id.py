"""activity event project_id

Revision ID: b7f3a9c21d04
Revises: 62a14e0f61ff
Create Date: 2026-06-15 00:55:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b7f3a9c21d04"
down_revision: str | None = "62a14e0f61ff"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("activity_events", sa.Column("project_id", sa.Uuid(), nullable=True))
    op.create_index(
        "ix_activity_events_org_project_created",
        "activity_events",
        ["org_id", "project_id", "created_at"],
        unique=False,
    )
    op.create_foreign_key(
        op.f("fk_activity_events_project_id_projects"),
        "activity_events",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_activity_events_project_id_projects"), "activity_events", type_="foreignkey"
    )
    op.drop_index("ix_activity_events_org_project_created", table_name="activity_events")
    op.drop_column("activity_events", "project_id")
