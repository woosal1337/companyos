"""project artifacts

Revision ID: 18430ba19baf
Revises: cc912b5ac053
Create Date: 2026-06-14 23:35:15.937016

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "18430ba19baf"
down_revision: str | None = "cc912b5ac053"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "project_artifacts",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("label", sa.String(length=200), nullable=False),
        sa.Column("url", sa.String(length=2000), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
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
            ["created_by"],
            ["users.id"],
            name=op.f("fk_project_artifacts_created_by_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_project_artifacts_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_project_artifacts_project_id_projects"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_project_artifacts")),
    )
    op.create_index(
        op.f("ix_project_artifacts_org_id"), "project_artifacts", ["org_id"], unique=False
    )
    op.create_index(
        op.f("ix_project_artifacts_project_id"), "project_artifacts", ["project_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_project_artifacts_project_id"), table_name="project_artifacts")
    op.drop_index(op.f("ix_project_artifacts_org_id"), table_name="project_artifacts")
    op.drop_table("project_artifacts")
