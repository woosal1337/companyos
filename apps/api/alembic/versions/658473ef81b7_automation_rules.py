"""automation rules

Revision ID: 658473ef81b7
Revises: 08fb88b650b4
Create Date: 2026-06-14 22:48:56.096071

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "658473ef81b7"
down_revision: str | None = "08fb88b650b4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "automation_rules",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column(
            "trigger",
            sa.Enum(
                "ON_TRIAGE_ENTRY",
                "ON_STATUS_CHANGE",
                name="automationtrigger",
                native_enum=False,
                length=40,
            ),
            nullable=False,
        ),
        sa.Column("actions", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("is_skill", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("enabled", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=True),
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
            ["created_by"],
            ["users.id"],
            name=op.f("fk_automation_rules_created_by_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_automation_rules_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_automation_rules")),
    )
    op.create_index(
        op.f("ix_automation_rules_org_id"), "automation_rules", ["org_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_automation_rules_org_id"), table_name="automation_rules")
    op.drop_table("automation_rules")
