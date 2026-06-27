"""organizations compliance + residency fields (COS-233)

Revision ID: d4f8b2e6c153
Revises: c3e7a9b5d042
Create Date: 2026-06-22 15:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "d4f8b2e6c153"
down_revision: str | None = "c3e7a9b5d042"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "organizations", sa.Column("residency_region", sa.String(length=20), nullable=True)
    )
    op.add_column(
        "organizations",
        sa.Column(
            "compliance_frameworks",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
    )
    op.add_column(
        "organizations", sa.Column("data_controller", sa.String(length=255), nullable=True)
    )
    op.add_column("organizations", sa.Column("dpo_contact", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("organizations", "dpo_contact")
    op.drop_column("organizations", "data_controller")
    op.drop_column("organizations", "compliance_frameworks")
    op.drop_column("organizations", "residency_region")
