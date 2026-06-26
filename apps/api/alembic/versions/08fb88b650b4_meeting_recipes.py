"""meeting recipes

Revision ID: 08fb88b650b4
Revises: 0bab5058af5a
Create Date: 2026-06-14 22:07:10.107934

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "08fb88b650b4"
down_revision: str | None = "0bab5058af5a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "meeting_recipes",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=True),
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
            ["created_by"],
            ["users.id"],
            name=op.f("fk_meeting_recipes_created_by_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_meeting_recipes_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_meeting_recipes")),
        sa.UniqueConstraint("org_id", "name", name=op.f("uq_meeting_recipes_org_id_name")),
    )
    op.create_index(op.f("ix_meeting_recipes_org_id"), "meeting_recipes", ["org_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_meeting_recipes_org_id"), table_name="meeting_recipes")
    op.drop_table("meeting_recipes")
