"""project_states + projects.state_id (portfolio lifecycle)

Revision ID: a6b7c8d9e0f2
Revises: f5a6b7c8d9e1
Create Date: 2026-06-20 23:55:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a6b7c8d9e0f2"
down_revision: str | None = "f5a6b7c8d9e1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "project_states",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("color", sa.String(length=16), nullable=False),
        sa.Column("group", sa.String(length=20), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
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
            name=op.f("fk_project_states_org_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_project_states")),
        sa.UniqueConstraint("org_id", "name", name=op.f("uq_project_states_org_name")),
    )
    op.create_index("ix_project_states_org_id", "project_states", ["org_id"])
    op.add_column("projects", sa.Column("state_id", sa.Uuid(), nullable=True))
    op.create_index("ix_projects_state_id", "projects", ["state_id"])
    op.create_foreign_key(
        op.f("fk_projects_state_id"),
        "projects",
        "project_states",
        ["state_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_projects_state_id"), "projects", type_="foreignkey")
    op.drop_index("ix_projects_state_id", table_name="projects")
    op.drop_column("projects", "state_id")
    op.drop_index("ix_project_states_org_id", table_name="project_states")
    op.drop_table("project_states")
