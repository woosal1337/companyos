"""notification_preferences (per-trigger email toggles)

Revision ID: b1c2d3e4f5a7
Revises: a0b1c2d3e4f6
Create Date: 2026-06-20 21:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b1c2d3e4f5a7"
down_revision: str | None = "a0b1c2d3e4f6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "notification_preferences",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("email_property_change", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("email_state_change", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("email_completed", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("email_comments", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("email_mentions", sa.Boolean(), server_default=sa.true(), nullable=False),
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
            name=op.f("fk_notification_preferences_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_notification_preferences_user_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_notification_preferences_project_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_notification_preferences")),
        sa.UniqueConstraint("org_id", "user_id", "project_id", name="uq_notif_pref_scope"),
    )
    op.create_index("ix_notification_preferences_org_id", "notification_preferences", ["org_id"])
    op.create_index("ix_notification_preferences_user_id", "notification_preferences", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_notification_preferences_user_id", table_name="notification_preferences")
    op.drop_index("ix_notification_preferences_org_id", table_name="notification_preferences")
    op.drop_table("notification_preferences")
