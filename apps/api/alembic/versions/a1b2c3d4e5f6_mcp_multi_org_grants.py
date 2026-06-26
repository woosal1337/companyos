"""mcp multi-org grants

Allow an OAuth grant/token to span every organization the user belongs to.
A multi-org grant has ``org_id = NULL`` and ``cross_org = TRUE``; the per-org
membership check still runs live on every MCP call. Single-org grants are
unchanged. The old unique constraint on (client_id, user_id, org_id) is replaced
by two partial unique indexes so both grant shapes coexist.

Revision ID: a1b2c3d4e5f6
Revises: 78a136a8bd38
Create Date: 2026-06-17

"""

import sqlalchemy as sa
from alembic import op

revision = "a1b2c3d4e5f6"
down_revision = "78a136a8bd38"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "oauth_grants",
        sa.Column("cross_org", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.alter_column("oauth_grants", "org_id", existing_type=sa.Uuid(), nullable=True)

    op.drop_constraint("uq_oauth_grants_client_id_user_id_org_id", "oauth_grants", type_="unique")
    op.create_index(
        "uq_oauth_grants_client_user_org",
        "oauth_grants",
        ["client_id", "user_id", "org_id"],
        unique=True,
        postgresql_where=sa.text("org_id IS NOT NULL"),
    )
    op.create_index(
        "uq_oauth_grants_client_user_cross",
        "oauth_grants",
        ["client_id", "user_id"],
        unique=True,
        postgresql_where=sa.text("cross_org"),
    )

    op.alter_column("oauth_authorization_codes", "org_id", existing_type=sa.Uuid(), nullable=True)
    op.alter_column("oauth_access_tokens", "org_id", existing_type=sa.Uuid(), nullable=True)
    op.alter_column("oauth_refresh_tokens", "org_id", existing_type=sa.Uuid(), nullable=True)


def downgrade() -> None:
    op.execute("DELETE FROM oauth_access_tokens WHERE org_id IS NULL")
    op.execute("DELETE FROM oauth_refresh_tokens WHERE org_id IS NULL")
    op.execute("DELETE FROM oauth_authorization_codes WHERE org_id IS NULL")
    op.execute("DELETE FROM oauth_grants WHERE org_id IS NULL")

    op.alter_column("oauth_refresh_tokens", "org_id", existing_type=sa.Uuid(), nullable=False)
    op.alter_column("oauth_access_tokens", "org_id", existing_type=sa.Uuid(), nullable=False)
    op.alter_column("oauth_authorization_codes", "org_id", existing_type=sa.Uuid(), nullable=False)

    op.drop_index("uq_oauth_grants_client_user_cross", table_name="oauth_grants")
    op.drop_index("uq_oauth_grants_client_user_org", table_name="oauth_grants")
    op.create_unique_constraint(
        "uq_oauth_grants_client_id_user_id_org_id",
        "oauth_grants",
        ["client_id", "user_id", "org_id"],
    )
    op.drop_column("oauth_grants", "cross_org")
