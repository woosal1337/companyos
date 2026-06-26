"""customers (CRM-lite accounts)

Revision ID: c9f4e7b2a361
Revises: b8e3d6a1f257
Create Date: 2026-06-21 09:20:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c9f4e7b2a361"
down_revision: str | None = "b8e3d6a1f257"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("email", sa.String(length=320), nullable=True),
        sa.Column("website_url", sa.String(length=500), nullable=True),
        sa.Column("employees", sa.Integer(), nullable=True),
        sa.Column("industry", sa.String(length=120), nullable=True),
        sa.Column("stage", sa.String(length=120), nullable=True),
        sa.Column("contract_status", sa.String(length=20), nullable=True),
        sa.Column("revenue", sa.Numeric(precision=14, scale=2), nullable=True),
        sa.Column("created_by", sa.Uuid(), nullable=True),
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
            ["org_id"], ["organizations.id"], name=op.f("fk_customers_org_id"), ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["created_by"], ["users.id"], name=op.f("fk_customers_created_by"), ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_customers")),
    )
    op.create_index("ix_customers_org_id", "customers", ["org_id"])


def downgrade() -> None:
    op.drop_index("ix_customers_org_id", table_name="customers")
    op.drop_table("customers")
