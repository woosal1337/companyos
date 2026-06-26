"""releases (versioned deliverables) + tasks.release_id

Revision ID: d4f5e6a7b8c9
Revises: c3f4d5e6a7b8
Create Date: 2026-06-20 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d4f5e6a7b8c9"
down_revision: str | None = "c3f4d5e6a7b8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "releases",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("version", sa.String(length=60), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("released_at", sa.Date(), nullable=True),
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
        sa.ForeignKeyConstraint(["org_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_releases_org_id", "releases", ["org_id"])

    op.add_column("tasks", sa.Column("release_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        op.f("fk_tasks_release_id_releases"),
        "tasks",
        "releases",
        ["release_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_tasks_release_id", "tasks", ["release_id"])


def downgrade() -> None:
    op.drop_index("ix_tasks_release_id", table_name="tasks")
    op.drop_constraint(op.f("fk_tasks_release_id_releases"), "tasks", type_="foreignkey")
    op.drop_column("tasks", "release_id")
    op.drop_index("ix_releases_org_id", table_name="releases")
    op.drop_table("releases")
