"""stickies

Revision ID: d5e6f8a9b0c1
Revises: c4d5e6f8a9b0
Create Date: 2026-06-19 13:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d5e6f8a9b0c1"
down_revision: str | None = "c4d5e6f8a9b0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "stickies",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("color", sa.String(length=20), nullable=False),
        sa.Column("position", sa.Float(), nullable=False),
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
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_stickies_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_stickies_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_stickies")),
    )
    op.create_index(op.f("ix_stickies_org_id"), "stickies", ["org_id"], unique=False)
    op.create_index(op.f("ix_stickies_user_id"), "stickies", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_stickies_user_id"), table_name="stickies")
    op.drop_index(op.f("ix_stickies_org_id"), table_name="stickies")
    op.drop_table("stickies")
