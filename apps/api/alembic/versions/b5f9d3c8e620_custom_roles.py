"""custom_roles + organization_members.custom_role_id (COS-176)

Revision ID: b5f9d3c8e620
Revises: a4e8c2d7f539
Create Date: 2026-06-22 11:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "b5f9d3c8e620"
down_revision: str | None = "a4e8c2d7f539"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "custom_roles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column(
            "permissions",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
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
            name=op.f("fk_custom_roles_org_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_custom_roles")),
        sa.UniqueConstraint("org_id", "name", name=op.f("uq_custom_roles_org_id_name")),
    )
    op.create_index("ix_custom_roles_org_id", "custom_roles", ["org_id"])
    op.add_column("organization_members", sa.Column("custom_role_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        op.f("fk_organization_members_custom_role_id"),
        "organization_members",
        "custom_roles",
        ["custom_role_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_organization_members_custom_role_id"), "organization_members", type_="foreignkey"
    )
    op.drop_column("organization_members", "custom_role_id")
    op.drop_table("custom_roles")
