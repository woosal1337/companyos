"""comment parent_id (threaded replies)

Revision ID: d1e2f3a4b5c6
Revises: c3d4e5f6a7b8
Create Date: 2026-06-19 01:20:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d1e2f3a4b5c6"
down_revision: str | None = "c3d4e5f6a7b8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("comments", sa.Column("parent_id", sa.Uuid(), nullable=True))
    op.create_index(op.f("ix_comments_parent_id"), "comments", ["parent_id"], unique=False)
    op.create_foreign_key(
        op.f("fk_comments_parent_id_comments"),
        "comments",
        "comments",
        ["parent_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_comments_parent_id_comments"), "comments", type_="foreignkey")
    op.drop_index(op.f("ix_comments_parent_id"), table_name="comments")
    op.drop_column("comments", "parent_id")
