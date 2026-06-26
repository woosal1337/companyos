"""mcp idempotency keys

Revision ID: 8ea888da7919
Revises: e90becb0abd8
Create Date: 2026-06-15 12:00:18.895341

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "8ea888da7919"
down_revision: str | None = "e90becb0abd8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "mcp_idempotency_keys",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("key", sa.String(length=255), nullable=False),
        sa.Column("tool", sa.String(length=100), nullable=False),
        sa.Column("result", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
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
            name=op.f("fk_mcp_idempotency_keys_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_mcp_idempotency_keys")),
        sa.UniqueConstraint("org_id", "key", name=op.f("uq_mcp_idempotency_keys_org_id_key")),
    )
    op.create_index(
        op.f("ix_mcp_idempotency_keys_org_id"), "mcp_idempotency_keys", ["org_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_mcp_idempotency_keys_org_id"), table_name="mcp_idempotency_keys")
    op.drop_table("mcp_idempotency_keys")
