"""group_role_mappings + ProjectMember.source + SSOConnection sync flags (COS-181)

Revision ID: a7c1e5b9d480
Revises: f6b0d4a8c375
Create Date: 2026-06-22 16:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a7c1e5b9d480"
down_revision: str | None = "f6b0d4a8c375"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "project_members",
        sa.Column("source", sa.String(length=20), server_default="manual", nullable=False),
    )
    op.add_column(
        "sso_connections",
        sa.Column(
            "group_attribute_key", sa.String(length=100), server_default="groups", nullable=False
        ),
    )
    op.add_column(
        "sso_connections",
        sa.Column("sync_on_login", sa.Boolean(), server_default=sa.true(), nullable=False),
    )
    op.add_column(
        "sso_connections",
        sa.Column("auto_remove", sa.Boolean(), server_default=sa.false(), nullable=False),
    )
    op.create_table(
        "group_role_mappings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("idp_group", sa.String(length=255), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
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
            name=op.f("fk_group_role_mappings_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_group_role_mappings_project_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_group_role_mappings")),
        sa.UniqueConstraint(
            "org_id",
            "idp_group",
            "project_id",
            name=op.f("uq_group_role_mappings_org_id_idp_group_project_id"),
        ),
    )
    op.create_index("ix_group_role_mappings_org_id", "group_role_mappings", ["org_id"])
    op.create_index("ix_group_role_mappings_project_id", "group_role_mappings", ["project_id"])


def downgrade() -> None:
    op.drop_table("group_role_mappings")
    op.drop_column("sso_connections", "auto_remove")
    op.drop_column("sso_connections", "sync_on_login")
    op.drop_column("sso_connections", "group_attribute_key")
    op.drop_column("project_members", "source")
