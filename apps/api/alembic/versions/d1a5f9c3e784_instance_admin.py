"""instance_settings + users.is_instance_admin/suspended_at (COS-223)

Revision ID: d1a5f9c3e784
Revises: c9e3a7b1d602
Create Date: 2026-06-22 18:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d1a5f9c3e784"
down_revision: str | None = "c9e3a7b1d602"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_instance_admin", sa.Boolean(), server_default=sa.false(), nullable=False),
    )
    op.add_column("users", sa.Column("suspended_at", sa.DateTime(timezone=True), nullable=True))
    op.create_table(
        "instance_settings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("instance_name", sa.String(length=200), nullable=False),
        sa.Column("telemetry_enabled", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column(
            "allow_workspace_creation", sa.Boolean(), server_default=sa.true(), nullable=False
        ),
        sa.Column("email_from", sa.String(length=255), nullable=True),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_instance_settings")),
    )


def downgrade() -> None:
    op.drop_table("instance_settings")
    op.drop_column("users", "suspended_at")
    op.drop_column("users", "is_instance_admin")
