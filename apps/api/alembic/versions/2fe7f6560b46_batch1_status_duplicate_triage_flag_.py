"""batch1 status duplicate triage flag slack connection

Revision ID: 2fe7f6560b46
Revises: 8fe22f2b47d3
Create Date: 2026-06-14 00:23:08.367881

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "2fe7f6560b46"
down_revision: str | None = "8fe22f2b47d3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "slack_connections",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("team_id", sa.String(length=100), nullable=False),
        sa.Column("team_name", sa.String(length=255), nullable=False),
        sa.Column("encrypted_token", sa.LargeBinary(), nullable=False),
        sa.Column("nonce", sa.LargeBinary(), nullable=False),
        sa.Column("installed_by", sa.Uuid(), nullable=True),
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
            ["installed_by"],
            ["users.id"],
            name=op.f("fk_slack_connections_installed_by_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_slack_connections_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_slack_connections")),
        sa.UniqueConstraint("org_id", name=op.f("uq_slack_connections_org_id")),
    )
    op.create_index(
        op.f("ix_slack_connections_org_id"), "slack_connections", ["org_id"], unique=False
    )
    op.add_column(
        "tasks",
        sa.Column("is_triage", sa.Boolean(), server_default=sa.text("false"), nullable=False),
    )
    op.create_index(op.f("ix_tasks_is_triage"), "tasks", ["is_triage"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_tasks_is_triage"), table_name="tasks")
    op.drop_column("tasks", "is_triage")
    op.drop_index(op.f("ix_slack_connections_org_id"), table_name="slack_connections")
    op.drop_table("slack_connections")
