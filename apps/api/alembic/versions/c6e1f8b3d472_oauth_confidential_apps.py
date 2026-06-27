"""oauth confidential apps (owner + secret) (COS-198)

Revision ID: c6e1f8b3d472
Revises: b5d9e2a4c761
Create Date: 2026-06-21 12:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c6e1f8b3d472"
down_revision: str | None = "b5d9e2a4c761"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("oauth_clients", sa.Column("owner_user_id", sa.Uuid(), nullable=True))
    op.add_column(
        "oauth_clients", sa.Column("client_secret_hash", sa.String(length=64), nullable=True)
    )
    op.create_index("ix_oauth_clients_owner_user_id", "oauth_clients", ["owner_user_id"])
    op.create_foreign_key(
        op.f("fk_oauth_clients_owner_user_id"),
        "oauth_clients",
        "users",
        ["owner_user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_oauth_clients_owner_user_id"), "oauth_clients", type_="foreignkey")
    op.drop_index("ix_oauth_clients_owner_user_id", table_name="oauth_clients")
    op.drop_column("oauth_clients", "client_secret_hash")
    op.drop_column("oauth_clients", "owner_user_id")
