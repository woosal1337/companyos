"""changelog_entries (release notes)

Revision ID: b8e3d6a1f257
Revises: a7d2c5f8b146
Create Date: 2026-06-21 08:50:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b8e3d6a1f257"
down_revision: str | None = "a7d2c5f8b146"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "changelog_entries",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("release_id", sa.Uuid(), nullable=False),
        sa.Column("category", sa.String(length=20), server_default="ADDED", nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("pr_url", sa.String(length=500), nullable=True),
        sa.Column("sort_order", sa.Float(), nullable=False, server_default="0"),
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
            name=op.f("fk_changelog_entries_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["release_id"],
            ["releases.id"],
            name=op.f("fk_changelog_entries_release_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_changelog_entries")),
    )
    op.create_index("ix_changelog_entries_org_id", "changelog_entries", ["org_id"])
    op.create_index("ix_changelog_entries_release_id", "changelog_entries", ["release_id"])


def downgrade() -> None:
    op.drop_index("ix_changelog_entries_release_id", table_name="changelog_entries")
    op.drop_index("ix_changelog_entries_org_id", table_name="changelog_entries")
    op.drop_table("changelog_entries")
