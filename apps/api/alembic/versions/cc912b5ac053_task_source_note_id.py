"""task source_note_id

Revision ID: cc912b5ac053
Revises: ea0727f5ba49
Create Date: 2026-06-14 23:30:42.983711

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "cc912b5ac053"
down_revision: str | None = "ea0727f5ba49"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("tasks", sa.Column("source_note_id", sa.Uuid(), nullable=True))
    op.create_index(op.f("ix_tasks_source_note_id"), "tasks", ["source_note_id"], unique=False)
    op.create_foreign_key(
        op.f("fk_tasks_source_note_id_notes"),
        "tasks",
        "notes",
        ["source_note_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_tasks_source_note_id_notes"), "tasks", type_="foreignkey")
    op.drop_index(op.f("ix_tasks_source_note_id"), table_name="tasks")
    op.drop_column("tasks", "source_note_id")
