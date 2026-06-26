"""org_domains (domain verification) (COS-193)

Revision ID: b2e6f9c4d370
Revises: a1d5f8c3e269
Create Date: 2026-06-21 15:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b2e6f9c4d370"
down_revision: str | None = "a1d5f8c3e269"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "org_domains",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("domain", sa.String(length=255), nullable=False),
        sa.Column("txt_token", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="PENDING", nullable=False),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
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
            name=op.f("fk_org_domains_org_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_org_domains")),
    )
    op.create_index("ix_org_domains_org_id", "org_domains", ["org_id"])
    op.create_index("ix_org_domains_domain", "org_domains", ["domain"])
    op.create_index(
        "uq_org_domains_verified",
        "org_domains",
        ["domain"],
        unique=True,
        postgresql_where=sa.text("status = 'VERIFIED'"),
    )


def downgrade() -> None:
    op.drop_index("uq_org_domains_verified", table_name="org_domains")
    op.drop_index("ix_org_domains_domain", table_name="org_domains")
    op.drop_index("ix_org_domains_org_id", table_name="org_domains")
    op.drop_table("org_domains")
