"""workflow statuses

Revision ID: a58ad0c1c190
Revises: 2fe7f6560b46
Create Date: 2026-06-14 11:16:03.693611

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a58ad0c1c190"
down_revision: str | None = "2fe7f6560b46"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "workflow_statuses",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("team_id", sa.Uuid(), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column(
            "category",
            sa.Enum(
                "BACKLOG",
                "UNSTARTED",
                "STARTED",
                "COMPLETED",
                "CANCELLED",
                name="statuscategory",
                native_enum=False,
                length=20,
            ),
            nullable=False,
        ),
        sa.Column("color", sa.String(length=40), nullable=False),
        sa.Column("position", sa.Float(), nullable=False),
        sa.Column("is_default", sa.Boolean(), server_default=sa.text("false"), nullable=False),
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
            name=op.f("fk_workflow_statuses_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
            name=op.f("fk_workflow_statuses_team_id_teams"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_workflow_statuses")),
        sa.UniqueConstraint(
            "org_id", "team_id", "name", name=op.f("uq_workflow_statuses_org_id_team_id_name")
        ),
    )
    op.create_index(
        op.f("ix_workflow_statuses_org_id"), "workflow_statuses", ["org_id"], unique=False
    )
    op.create_index(
        op.f("ix_workflow_statuses_team_id"), "workflow_statuses", ["team_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_workflow_statuses_team_id"), table_name="workflow_statuses")
    op.drop_index(op.f("ix_workflow_statuses_org_id"), table_name="workflow_statuses")
    op.drop_table("workflow_statuses")
