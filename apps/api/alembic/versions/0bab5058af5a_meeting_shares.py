"""meeting shares

Revision ID: 0bab5058af5a
Revises: 704d7fb13c31
Create Date: 2026-06-14 22:00:46.252961

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0bab5058af5a"
down_revision: str | None = "704d7fb13c31"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "meeting_shares",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("meeting_id", sa.Uuid(), nullable=False),
        sa.Column("token", sa.String(length=64), nullable=False),
        sa.Column(
            "include_transcript", sa.Boolean(), server_default=sa.text("false"), nullable=False
        ),
        sa.Column("revoked", sa.Boolean(), server_default=sa.text("false"), nullable=False),
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
            name=op.f("fk_meeting_shares_created_by_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["meeting_id"],
            ["meetings.id"],
            name=op.f("fk_meeting_shares_meeting_id_meetings"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_meeting_shares_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_meeting_shares")),
        sa.UniqueConstraint("meeting_id", name=op.f("uq_meeting_shares_meeting_id")),
    )
    op.create_index(
        op.f("ix_meeting_shares_meeting_id"), "meeting_shares", ["meeting_id"], unique=False
    )
    op.create_index(op.f("ix_meeting_shares_org_id"), "meeting_shares", ["org_id"], unique=False)
    op.create_index(op.f("ix_meeting_shares_token"), "meeting_shares", ["token"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_meeting_shares_token"), table_name="meeting_shares")
    op.drop_index(op.f("ix_meeting_shares_org_id"), table_name="meeting_shares")
    op.drop_index(op.f("ix_meeting_shares_meeting_id"), table_name="meeting_shares")
    op.drop_table("meeting_shares")
