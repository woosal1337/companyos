"""sentry_intakes (inbound alerts) (COS-260)

Revision ID: e8b3d6f9a247
Revises: d7f2b9e4c815
Create Date: 2026-06-21 13:50:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e8b3d6f9a247"
down_revision: str | None = "d7f2b9e4c815"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "sentry_intakes",
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
            name=op.f("fk_sentry_intakes_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_sentry_intakes_project_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sentry_intakes")),
    )
    op.create_index("ix_sentry_intakes_org_id", "sentry_intakes", ["org_id"])
    op.create_index("ix_sentry_intakes_project_id", "sentry_intakes", ["project_id"])
    op.create_index("ix_sentry_intakes_token", "sentry_intakes", ["token"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_sentry_intakes_token", table_name="sentry_intakes")
    op.drop_index("ix_sentry_intakes_project_id", table_name="sentry_intakes")
    op.drop_index("ix_sentry_intakes_org_id", table_name="sentry_intakes")
    op.drop_table("sentry_intakes")
