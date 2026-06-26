"""note_versions (page version history)

Revision ID: f9a0b1c2d3e5
Revises: e8f9a0b1c2d4
Create Date: 2026-06-20 20:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f9a0b1c2d3e5"
down_revision: str | None = "e8f9a0b1c2d4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "note_versions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("note_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("edited_by", sa.Uuid(), nullable=True),
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
            name=op.f("fk_note_versions_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["note_id"], ["notes.id"], name=op.f("fk_note_versions_note_id"), ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["edited_by"],
            ["users.id"],
            name=op.f("fk_note_versions_edited_by"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_note_versions")),
    )
    op.create_index("ix_note_versions_org_id", "note_versions", ["org_id"])
    op.create_index("ix_note_versions_note_id", "note_versions", ["note_id"])


def downgrade() -> None:
    op.drop_index("ix_note_versions_note_id", table_name="note_versions")
    op.drop_index("ix_note_versions_org_id", table_name="note_versions")
    op.drop_table("note_versions")
