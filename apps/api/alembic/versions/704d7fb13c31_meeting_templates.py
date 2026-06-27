"""meeting templates

Revision ID: 704d7fb13c31
Revises: 1fa178a681a1
Create Date: 2026-06-14 11:47:04.401400

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "704d7fb13c31"
down_revision: str | None = "1fa178a681a1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "meeting_templates",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("sections", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("prompt_scaffold", sa.Text(), nullable=True),
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
            name=op.f("fk_meeting_templates_created_by_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_meeting_templates_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_meeting_templates")),
        sa.UniqueConstraint("org_id", "name", name=op.f("uq_meeting_templates_org_id_name")),
    )
    op.create_index(
        op.f("ix_meeting_templates_org_id"), "meeting_templates", ["org_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_meeting_templates_org_id"), table_name="meeting_templates")
    op.drop_table("meeting_templates")
