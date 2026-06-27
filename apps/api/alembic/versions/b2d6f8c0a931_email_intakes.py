"""email_intakes (email-to-task intake) (COS-62)

Revision ID: b2d6f8c0a931
Revises: a1c5e9b3d720
Create Date: 2026-06-22 14:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b2d6f8c0a931"
down_revision: str | None = "a1c5e9b3d720"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "email_intakes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("token", sa.String(length=64), nullable=False),
        sa.Column("enabled", sa.Boolean(), server_default=sa.text("true"), nullable=False),
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
            name=op.f("fk_email_intakes_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_email_intakes_project_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_email_intakes")),
    )
    op.create_index("ix_email_intakes_org_id", "email_intakes", ["org_id"])
    op.create_index("ix_email_intakes_project_id", "email_intakes", ["project_id"])
    op.create_index("ix_email_intakes_token", "email_intakes", ["token"], unique=True)


def downgrade() -> None:
    op.drop_table("email_intakes")
