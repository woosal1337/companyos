"""transition_conditions (pre-validation hooks) (COS-220)

Revision ID: a4e8c1b7d293
Revises: f3c7b2e9a648
Create Date: 2026-06-21 11:25:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a4e8c1b7d293"
down_revision: str | None = "f3c7b2e9a648"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "transition_conditions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("from_status_id", sa.Uuid(), nullable=False),
        sa.Column("to_status_id", sa.Uuid(), nullable=False),
        sa.Column("condition", sa.String(length=40), nullable=False),
        sa.Column("position", sa.Float(), nullable=False, server_default="0"),
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
            name=op.f("fk_transition_conditions_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["from_status_id"],
            ["workflow_statuses.id"],
            name=op.f("fk_transition_conditions_from_status_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["to_status_id"],
            ["workflow_statuses.id"],
            name=op.f("fk_transition_conditions_to_status_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_transition_conditions")),
    )
    op.create_index("ix_transition_conditions_org_id", "transition_conditions", ["org_id"])
    op.create_index(
        "ix_transition_conditions_from_status_id", "transition_conditions", ["from_status_id"]
    )
    op.create_index(
        "ix_transition_conditions_to_status_id", "transition_conditions", ["to_status_id"]
    )


def downgrade() -> None:
    op.drop_table("transition_conditions")
