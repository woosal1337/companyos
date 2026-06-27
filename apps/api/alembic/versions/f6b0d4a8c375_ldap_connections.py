"""ldap_connections (LDAP/AD auth) (COS-173)

Revision ID: f6b0d4a8c375
Revises: e5a9c3f7b264
Create Date: 2026-06-22 16:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f6b0d4a8c375"
down_revision: str | None = "e5a9c3f7b264"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ldap_connections",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("server_uri", sa.String(length=500), nullable=False),
        sa.Column("use_tls", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("bind_dn", sa.String(length=500), nullable=False),
        sa.Column("encrypted_bind_pw", sa.LargeBinary(), nullable=False),
        sa.Column("nonce", sa.LargeBinary(), nullable=False),
        sa.Column("search_base", sa.String(length=500), nullable=False),
        sa.Column("search_filter", sa.String(length=500), nullable=False),
        sa.Column("attr_email", sa.String(length=100), nullable=False),
        sa.Column("attr_first", sa.String(length=100), nullable=False),
        sa.Column("attr_last", sa.String(length=100), nullable=False),
        sa.Column("enabled", sa.Boolean(), server_default=sa.false(), nullable=False),
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
            name=op.f("fk_ldap_connections_org_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_ldap_connections")),
        sa.UniqueConstraint("org_id", name=op.f("uq_ldap_connections_org_id")),
    )
    op.create_index("ix_ldap_connections_org_id", "ldap_connections", ["org_id"])


def downgrade() -> None:
    op.drop_table("ldap_connections")
