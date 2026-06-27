"""note parent_id (nested pages)

Revision ID: b5c6d7e8f9a0
Revises: a4b5c6d7e8f9
Create Date: 2026-06-19 02:50:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b5c6d7e8f9a0"
down_revision: str | None = "a4b5c6d7e8f9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("notes", sa.Column("parent_id", sa.Uuid(), nullable=True))
    op.create_index(op.f("ix_notes_parent_id"), "notes", ["parent_id"], unique=False)
    op.create_foreign_key(
        op.f("fk_notes_parent_id_notes"),
        "notes",
        "notes",
        ["parent_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_notes_parent_id_notes"), "notes", type_="foreignkey")
    op.drop_index(op.f("ix_notes_parent_id"), table_name="notes")
    op.drop_column("notes", "parent_id")
