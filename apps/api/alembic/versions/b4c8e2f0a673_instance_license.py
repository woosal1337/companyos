"""instance_licenses (offline license keys) (COS-230)

Revision ID: b4c8e2f0a673
Revises: a3f7c1e9b562
Create Date: 2026-06-22 20:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b4c8e2f0a673"
down_revision: str | None = "a3f7c1e9b562"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "instance_licenses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("plan", sa.String(length=20), nullable=False),
        sa.Column("seats", sa.Integer(), nullable=False),
        sa.Column("licensee", sa.String(length=255), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("token", sa.Text(), nullable=False),
        sa.Column("active", sa.Boolean(), server_default=sa.true(), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_instance_licenses")),
    )


def downgrade() -> None:
    op.drop_table("instance_licenses")
