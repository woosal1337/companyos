"""notes.public_token + public_page_comments (COS-124)

Revision ID: d1b5f8c4a296
Revises: c9a4e7b2f185
Create Date: 2026-06-22 09:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d1b5f8c4a296"
down_revision: str | None = "c9a4e7b2f185"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("notes", sa.Column("public_token", sa.String(length=64), nullable=True))
    op.create_index("ix_notes_public_token", "notes", ["public_token"], unique=True)
    op.create_table(
        "public_page_comments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("note_id", sa.Uuid(), nullable=False),
        sa.Column("author_name", sa.String(length=120), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("reported", sa.Boolean(), server_default=sa.false(), nullable=False),
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
            ["note_id"],
            ["notes.id"],
            name=op.f("fk_public_page_comments_note_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_public_page_comments")),
    )
    op.create_index("ix_public_page_comments_note_id", "public_page_comments", ["note_id"])


def downgrade() -> None:
    op.drop_table("public_page_comments")
    op.drop_index("ix_notes_public_token", table_name="notes")
    op.drop_column("notes", "public_token")
