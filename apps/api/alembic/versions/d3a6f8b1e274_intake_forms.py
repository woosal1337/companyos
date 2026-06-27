"""intake_forms (custom intake forms)

Revision ID: d3a6f8b1e274
Revises: c2f5e7a0d163
Create Date: 2026-06-21 06:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "d3a6f8b1e274"
down_revision: str | None = "c2f5e7a0d163"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "intake_forms",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("token", sa.String(length=64), nullable=False),
        sa.Column("enabled", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column(
            "fields", postgresql.JSONB(), server_default=sa.text("'[]'::jsonb"), nullable=False
        ),
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
            name=op.f("fk_intake_forms_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_intake_forms_project_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_intake_forms")),
    )
    op.create_index("ix_intake_forms_org_id", "intake_forms", ["org_id"])
    op.create_index("ix_intake_forms_project_id", "intake_forms", ["project_id"])
    op.create_index("ix_intake_forms_token", "intake_forms", ["token"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_intake_forms_token", table_name="intake_forms")
    op.drop_index("ix_intake_forms_project_id", table_name="intake_forms")
    op.drop_index("ix_intake_forms_org_id", table_name="intake_forms")
    op.drop_table("intake_forms")
