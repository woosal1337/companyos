"""initiative updates (RAG health stream)

Revision ID: e6f8a9b0c1d2
Revises: d5e6f8a9b0c1
Create Date: 2026-06-19 13:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e6f8a9b0c1d2"
down_revision: str | None = "d5e6f8a9b0c1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "initiative_updates",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("initiative_id", sa.Uuid(), nullable=False),
        sa.Column("health", sa.String(length=20), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
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
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_initiative_updates_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["initiative_id"],
            ["initiatives.id"],
            name=op.f("fk_initiative_updates_initiative_id_initiatives"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            name=op.f("fk_initiative_updates_created_by_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_initiative_updates")),
    )
    op.create_index(
        op.f("ix_initiative_updates_org_id"), "initiative_updates", ["org_id"], unique=False
    )
    op.create_index(
        op.f("ix_initiative_updates_initiative_id"),
        "initiative_updates",
        ["initiative_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_initiative_updates_initiative_id"), table_name="initiative_updates")
    op.drop_index(op.f("ix_initiative_updates_org_id"), table_name="initiative_updates")
    op.drop_table("initiative_updates")
