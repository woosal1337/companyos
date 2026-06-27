"""retrospectives (post-mortems anchored to cycle)

Revision ID: a7d2c5f8b146
Revises: f5c8a1b3e927
Create Date: 2026-06-21 08:20:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a7d2c5f8b146"
down_revision: str | None = "f5c8a1b3e927"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "retrospectives",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("cycle_id", sa.Uuid(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("went_well", sa.Text(), nullable=True),
        sa.Column("to_improve", sa.Text(), nullable=True),
        sa.Column("action_items", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Uuid(), nullable=True),
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
            name=op.f("fk_retrospectives_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_retrospectives_project_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["cycle_id"],
            ["cycles.id"],
            name=op.f("fk_retrospectives_cycle_id"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            name=op.f("fk_retrospectives_created_by"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_retrospectives")),
    )
    op.create_index("ix_retrospectives_org_id", "retrospectives", ["org_id"])
    op.create_index("ix_retrospectives_project_id", "retrospectives", ["project_id"])
    op.create_index("ix_retrospectives_cycle_id", "retrospectives", ["cycle_id"])


def downgrade() -> None:
    op.drop_index("ix_retrospectives_cycle_id", table_name="retrospectives")
    op.drop_index("ix_retrospectives_project_id", table_name="retrospectives")
    op.drop_index("ix_retrospectives_org_id", table_name="retrospectives")
    op.drop_table("retrospectives")
