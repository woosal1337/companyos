"""initiatives + initiative_projects

Revision ID: c4d5e6f8a9b0
Revises: b3c4d5e6f8a9
Create Date: 2026-06-19 12:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c4d5e6f8a9b0"
down_revision: str | None = "b3c4d5e6f8a9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "initiatives",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("target_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
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
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_initiatives_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            name=op.f("fk_initiatives_created_by_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_initiatives")),
    )
    op.create_index(op.f("ix_initiatives_org_id"), "initiatives", ["org_id"], unique=False)
    op.create_table(
        "initiative_projects",
        sa.Column("initiative_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["initiative_id"],
            ["initiatives.id"],
            name=op.f("fk_initiative_projects_initiative_id_initiatives"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_initiative_projects_project_id_projects"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("initiative_id", "project_id", name=op.f("pk_initiative_projects")),
    )


def downgrade() -> None:
    op.drop_table("initiative_projects")
    op.drop_index(op.f("ix_initiatives_org_id"), table_name="initiatives")
    op.drop_table("initiatives")
