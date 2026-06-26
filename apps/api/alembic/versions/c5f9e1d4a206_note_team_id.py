"""note.team_id (team-scoped pages)

Revision ID: c5f9e1d4a206
Revises: b4e8d0c3f195
Create Date: 2026-06-21 02:55:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c5f9e1d4a206"
down_revision: str | None = "b4e8d0c3f195"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("notes", sa.Column("team_id", sa.Uuid(), nullable=True))
    op.create_index("ix_notes_team_id", "notes", ["team_id"])
    op.create_foreign_key(
        op.f("fk_notes_team_id"), "notes", "teams", ["team_id"], ["id"], ondelete="SET NULL"
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_notes_team_id"), "notes", type_="foreignkey")
    op.drop_index("ix_notes_team_id", table_name="notes")
    op.drop_column("notes", "team_id")
