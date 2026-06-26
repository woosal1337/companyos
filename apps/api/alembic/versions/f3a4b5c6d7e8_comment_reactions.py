"""comment reactions

Revision ID: f3a4b5c6d7e8
Revises: e2f3a4b5c6d7
Create Date: 2026-06-19 01:55:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f3a4b5c6d7e8"
down_revision: str | None = "e2f3a4b5c6d7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "comment_reactions",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("comment_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("emoji", sa.String(length=32), nullable=False),
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
            ["comment_id"],
            ["comments.id"],
            name=op.f("fk_comment_reactions_comment_id_comments"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_comment_reactions_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_comment_reactions_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_comment_reactions")),
        sa.UniqueConstraint(
            "comment_id",
            "user_id",
            "emoji",
            name="uq_comment_reactions_comment_id_user_id_emoji",
        ),
    )
    op.create_index(
        op.f("ix_comment_reactions_comment_id"), "comment_reactions", ["comment_id"], unique=False
    )
    op.create_index(
        op.f("ix_comment_reactions_org_id"), "comment_reactions", ["org_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_comment_reactions_org_id"), table_name="comment_reactions")
    op.drop_index(op.f("ix_comment_reactions_comment_id"), table_name="comment_reactions")
    op.drop_table("comment_reactions")
