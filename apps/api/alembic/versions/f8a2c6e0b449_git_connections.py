"""git_repo_connections (Git sync) (COS-256)

Revision ID: f8a2c6e0b449
Revises: e7c1b5a9f338
Create Date: 2026-06-22 19:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f8a2c6e0b449"
down_revision: str | None = "e7c1b5a9f338"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "git_repo_connections",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("provider", sa.String(length=20), nullable=False),
        sa.Column("owner", sa.String(length=255), nullable=False),
        sa.Column("repo", sa.String(length=255), nullable=False),
        sa.Column("token", sa.String(length=64), nullable=False),
        sa.Column("enabled", sa.Boolean(), server_default=sa.text("true"), nullable=False),
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
            name=op.f("fk_git_repo_connections_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_git_repo_connections_project_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_git_repo_connections")),
    )
    op.create_index("ix_git_repo_connections_org_id", "git_repo_connections", ["org_id"])
    op.create_index("ix_git_repo_connections_project_id", "git_repo_connections", ["project_id"])
    op.create_index("ix_git_repo_connections_token", "git_repo_connections", ["token"], unique=True)


def downgrade() -> None:
    op.drop_table("git_repo_connections")
