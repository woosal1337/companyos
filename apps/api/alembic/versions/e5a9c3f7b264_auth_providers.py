"""auth_provider_configs (sign-in provider matrix) (COS-209)

Revision ID: e5a9c3f7b264
Revises: d4f8b2e6c153
Create Date: 2026-06-22 15:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e5a9c3f7b264"
down_revision: str | None = "d4f8b2e6c153"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "auth_provider_configs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("magic_code_enabled", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("password_enabled", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("google_enabled", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("github_enabled", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("allow_self_signup", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column(
            "restrict_oauth_to_verified_domains",
            sa.Boolean(),
            server_default=sa.false(),
            nullable=False,
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
            name=op.f("fk_auth_provider_configs_org_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_auth_provider_configs")),
        sa.UniqueConstraint("org_id", name=op.f("uq_auth_provider_configs_org_id")),
    )
    op.create_index("ix_auth_provider_configs_org_id", "auth_provider_configs", ["org_id"])


def downgrade() -> None:
    op.drop_table("auth_provider_configs")
