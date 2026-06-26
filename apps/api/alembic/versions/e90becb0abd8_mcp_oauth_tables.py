"""mcp oauth tables

Revision ID: e90becb0abd8
Revises: c1d2e3f4a5b6
Create Date: 2026-06-15 07:15:20.624521

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "e90becb0abd8"
down_revision: str | None = "c1d2e3f4a5b6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "oauth_clients",
        sa.Column("client_id", sa.String(length=512), nullable=False),
        sa.Column(
            "registration_type",
            sa.Enum(
                "DCR",
                "CIMD",
                "PREREGISTERED",
                name="clientregistrationtype",
                native_enum=False,
                length=20,
            ),
            nullable=False,
        ),
        sa.Column("client_name", sa.String(length=255), nullable=False),
        sa.Column("client_uri", sa.String(length=2000), nullable=True),
        sa.Column("logo_uri", sa.String(length=2000), nullable=True),
        sa.Column("redirect_uris", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("grant_types", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("token_endpoint_auth_method", sa.String(length=40), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_oauth_clients")),
    )
    op.create_index(op.f("ix_oauth_clients_client_id"), "oauth_clients", ["client_id"], unique=True)
    op.create_table(
        "oauth_signing_keys",
        sa.Column("kid", sa.String(length=64), nullable=False),
        sa.Column("algorithm", sa.String(length=10), nullable=False),
        sa.Column("public_jwk", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("encrypted_private_key", sa.LargeBinary(), nullable=False),
        sa.Column("nonce", sa.LargeBinary(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "ACTIVE", "NEXT", "RETIRED", name="signingkeystatus", native_enum=False, length=20
            ),
            nullable=False,
        ),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_oauth_signing_keys")),
    )
    op.create_index(op.f("ix_oauth_signing_keys_kid"), "oauth_signing_keys", ["kid"], unique=True)
    op.create_table(
        "oauth_authorization_codes",
        sa.Column("code_hash", sa.String(length=64), nullable=False),
        sa.Column("client_id", sa.String(length=512), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("scopes", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("redirect_uri", sa.String(length=2000), nullable=False),
        sa.Column("code_challenge", sa.String(length=128), nullable=False),
        sa.Column("code_challenge_method", sa.String(length=10), nullable=False),
        sa.Column("resource", sa.String(length=512), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True),
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
            name=op.f("fk_oauth_authorization_codes_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_oauth_authorization_codes_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_oauth_authorization_codes")),
    )
    op.create_index(
        op.f("ix_oauth_authorization_codes_code_hash"),
        "oauth_authorization_codes",
        ["code_hash"],
        unique=True,
    )
    op.create_table(
        "oauth_grants",
        sa.Column("client_id", sa.String(length=512), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("scopes", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "status",
            sa.Enum("ACTIVE", "REVOKED", name="grantstatus", native_enum=False, length=20),
            nullable=False,
        ),
        sa.Column("granted_by", sa.String(length=40), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_reason", sa.String(length=40), nullable=True),
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
            name=op.f("fk_oauth_grants_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_oauth_grants_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_oauth_grants")),
        sa.UniqueConstraint(
            "client_id", "user_id", "org_id", name=op.f("uq_oauth_grants_client_id_user_id_org_id")
        ),
    )
    op.create_index(op.f("ix_oauth_grants_client_id"), "oauth_grants", ["client_id"], unique=False)
    op.create_index(op.f("ix_oauth_grants_org_id"), "oauth_grants", ["org_id"], unique=False)
    op.create_index("ix_oauth_grants_user_org", "oauth_grants", ["user_id", "org_id"], unique=False)
    op.create_table(
        "oauth_access_tokens",
        sa.Column("jti", sa.Uuid(), nullable=False),
        sa.Column("grant_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("client_id", sa.String(length=512), nullable=False),
        sa.Column("scopes", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("resource", sa.String(length=512), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
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
            ["grant_id"],
            ["oauth_grants.id"],
            name=op.f("fk_oauth_access_tokens_grant_id_oauth_grants"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_oauth_access_tokens_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_oauth_access_tokens_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_oauth_access_tokens")),
    )
    op.create_index(
        "ix_oauth_access_tokens_grant", "oauth_access_tokens", ["grant_id"], unique=False
    )
    op.create_index(op.f("ix_oauth_access_tokens_jti"), "oauth_access_tokens", ["jti"], unique=True)
    op.create_table(
        "oauth_refresh_tokens",
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("grant_id", sa.Uuid(), nullable=False),
        sa.Column("family_id", sa.Uuid(), nullable=False),
        sa.Column("replaced_by", sa.Uuid(), nullable=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("client_id", sa.String(length=512), nullable=False),
        sa.Column("scopes", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
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
            ["grant_id"],
            ["oauth_grants.id"],
            name=op.f("fk_oauth_refresh_tokens_grant_id_oauth_grants"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_oauth_refresh_tokens_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_oauth_refresh_tokens_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_oauth_refresh_tokens")),
    )
    op.create_index(
        "ix_oauth_refresh_tokens_family", "oauth_refresh_tokens", ["family_id"], unique=False
    )
    op.create_index(
        op.f("ix_oauth_refresh_tokens_token_hash"),
        "oauth_refresh_tokens",
        ["token_hash"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_oauth_refresh_tokens_token_hash"), table_name="oauth_refresh_tokens")
    op.drop_index("ix_oauth_refresh_tokens_family", table_name="oauth_refresh_tokens")
    op.drop_table("oauth_refresh_tokens")
    op.drop_index(op.f("ix_oauth_access_tokens_jti"), table_name="oauth_access_tokens")
    op.drop_index("ix_oauth_access_tokens_grant", table_name="oauth_access_tokens")
    op.drop_table("oauth_access_tokens")
    op.drop_index("ix_oauth_grants_user_org", table_name="oauth_grants")
    op.drop_index(op.f("ix_oauth_grants_org_id"), table_name="oauth_grants")
    op.drop_index(op.f("ix_oauth_grants_client_id"), table_name="oauth_grants")
    op.drop_table("oauth_grants")
    op.drop_index(
        op.f("ix_oauth_authorization_codes_code_hash"), table_name="oauth_authorization_codes"
    )
    op.drop_table("oauth_authorization_codes")
    op.drop_index(op.f("ix_oauth_signing_keys_kid"), table_name="oauth_signing_keys")
    op.drop_table("oauth_signing_keys")
    op.drop_index(op.f("ix_oauth_clients_client_id"), table_name="oauth_clients")
    op.drop_table("oauth_clients")
