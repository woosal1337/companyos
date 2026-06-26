"""rbac audit events (role/permission compliance trail)

Revision ID: d6e7f8a9b0c1
Revises: c5d6e7f8a9b0
Create Date: 2026-06-20 18:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "d6e7f8a9b0c1"
down_revision: str | None = "c5d6e7f8a9b0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "rbac_audit_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=True),
        sa.Column("actor_type", sa.String(length=20), server_default="user", nullable=False),
        sa.Column("subject_user_id", sa.Uuid(), nullable=True),
        sa.Column("resource_scope", sa.String(length=20), nullable=False),
        sa.Column("resource_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("action", sa.String(length=30), nullable=False),
        sa.Column("role_before", sa.String(length=20), nullable=True),
        sa.Column("role_after", sa.String(length=20), nullable=True),
        sa.Column("detail", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
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
            name=op.f("fk_rbac_audit_events_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["actor_id"],
            ["users.id"],
            name=op.f("fk_rbac_audit_events_actor_id"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["subject_user_id"],
            ["users.id"],
            name=op.f("fk_rbac_audit_events_subject_user_id"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_rbac_audit_events_project_id"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_rbac_audit_events")),
    )
    op.create_index("ix_rbac_audit_events_org_id", "rbac_audit_events", ["org_id"])
    op.create_index("ix_rbac_audit_org_created", "rbac_audit_events", ["org_id", "created_at"])
    op.create_index("ix_rbac_audit_org_subject", "rbac_audit_events", ["org_id", "subject_user_id"])
    op.create_index("ix_rbac_audit_org_actor", "rbac_audit_events", ["org_id", "actor_id"])
    op.create_index(
        "ix_rbac_audit_org_resource",
        "rbac_audit_events",
        ["org_id", "resource_scope", "resource_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_rbac_audit_org_resource", table_name="rbac_audit_events")
    op.drop_index("ix_rbac_audit_org_actor", table_name="rbac_audit_events")
    op.drop_index("ix_rbac_audit_org_subject", table_name="rbac_audit_events")
    op.drop_index("ix_rbac_audit_org_created", table_name="rbac_audit_events")
    op.drop_index("ix_rbac_audit_events_org_id", table_name="rbac_audit_events")
    op.drop_table("rbac_audit_events")
