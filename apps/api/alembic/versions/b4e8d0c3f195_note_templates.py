"""note_templates (page templates)

Revision ID: b4e8d0c3f195
Revises: a3f7c91d2e84
Create Date: 2026-06-21 02:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b4e8d0c3f195"
down_revision: str | None = "a3f7c91d2e84"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "note_templates",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
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
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_note_templates_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_note_templates_project_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            name=op.f("fk_note_templates_created_by"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_note_templates")),
        sa.UniqueConstraint("org_id", "name", name=op.f("uq_note_templates_org_name")),
    )
    op.create_index("ix_note_templates_org_id", "note_templates", ["org_id"])
    op.create_index("ix_note_templates_project_id", "note_templates", ["project_id"])


def downgrade() -> None:
    op.drop_index("ix_note_templates_project_id", table_name="note_templates")
    op.drop_index("ix_note_templates_org_id", table_name="note_templates")
    op.drop_table("note_templates")
