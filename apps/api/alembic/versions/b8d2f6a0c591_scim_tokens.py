"""scim_tokens (SCIM provisioning) (COS-184)

Revision ID: b8d2f6a0c591
Revises: a7c1e5b9d480
Create Date: 2026-06-22 17:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b8d2f6a0c591"
down_revision: str | None = "a7c1e5b9d480"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "scim_tokens",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("prefix", sa.String(length=16), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
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
            ["org_id"], ["organizations.id"], name=op.f("fk_scim_tokens_org_id"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_scim_tokens")),
    )
    op.create_index("ix_scim_tokens_org_id", "scim_tokens", ["org_id"])
    op.create_index("ix_scim_tokens_token_hash", "scim_tokens", ["token_hash"], unique=True)


def downgrade() -> None:
    op.drop_table("scim_tokens")
