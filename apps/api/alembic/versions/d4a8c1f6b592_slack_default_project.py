"""slack_connections.default_project_id (COS-266)

Revision ID: d4a8c1f6b592
Revises: c3f7a0d5e481
Create Date: 2026-06-21 16:45:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d4a8c1f6b592"
down_revision: str | None = "c3f7a0d5e481"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("slack_connections", sa.Column("default_project_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        op.f("fk_slack_connections_default_project_id"),
        "slack_connections",
        "projects",
        ["default_project_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_slack_connections_default_project_id"), "slack_connections", type_="foreignkey"
    )
    op.drop_column("slack_connections", "default_project_id")
