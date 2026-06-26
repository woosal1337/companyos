"""note lifecycle: visibility/locked/archived + note_shares

Revision ID: a0b1c2d3e4f6
Revises: f9a0b1c2d3e5
Create Date: 2026-06-20 21:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a0b1c2d3e4f6"
down_revision: str | None = "f9a0b1c2d3e5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "notes",
        sa.Column("visibility", sa.String(length=20), server_default="PUBLIC", nullable=False),
    )
    op.add_column(
        "notes",
        sa.Column("locked", sa.Boolean(), server_default=sa.false(), nullable=False),
    )
    op.add_column("notes", sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True))
    op.create_table(
        "note_shares",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("note_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("access", sa.String(length=20), server_default="VIEW", nullable=False),
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
            name=op.f("fk_note_shares_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["note_id"], ["notes.id"], name=op.f("fk_note_shares_note_id"), ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_note_shares_user_id"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_note_shares")),
        sa.UniqueConstraint("note_id", "user_id", name=op.f("uq_note_shares_note_user")),
    )
    op.create_index("ix_note_shares_org_id", "note_shares", ["org_id"])
    op.create_index("ix_note_shares_note_id", "note_shares", ["note_id"])


def downgrade() -> None:
    op.drop_index("ix_note_shares_note_id", table_name="note_shares")
    op.drop_index("ix_note_shares_org_id", table_name="note_shares")
    op.drop_table("note_shares")
    op.drop_column("notes", "archived_at")
    op.drop_column("notes", "locked")
    op.drop_column("notes", "visibility")
