"""task note links

Revision ID: b1c2d3e4f5a6
Revises: a0b1c2d3e4f5
Create Date: 2026-06-19 06:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b1c2d3e4f5a6"
down_revision: str | None = "a0b1c2d3e4f5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "task_note_links",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("task_id", sa.Uuid(), nullable=False),
        sa.Column("note_id", sa.Uuid(), nullable=False),
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
            ["note_id"],
            ["notes.id"],
            name=op.f("fk_task_note_links_note_id_notes"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_task_note_links_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            name=op.f("fk_task_note_links_task_id_tasks"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_task_note_links")),
        sa.UniqueConstraint("task_id", "note_id", name="uq_task_note_links_task_id_note_id"),
    )
    op.create_index(
        op.f("ix_task_note_links_note_id"), "task_note_links", ["note_id"], unique=False
    )
    op.create_index(op.f("ix_task_note_links_org_id"), "task_note_links", ["org_id"], unique=False)
    op.create_index(
        op.f("ix_task_note_links_task_id"), "task_note_links", ["task_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_task_note_links_task_id"), table_name="task_note_links")
    op.drop_index(op.f("ix_task_note_links_org_id"), table_name="task_note_links")
    op.drop_index(op.f("ix_task_note_links_note_id"), table_name="task_note_links")
    op.drop_table("task_note_links")
