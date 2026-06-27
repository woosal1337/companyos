"""teamspaces: team lead/charter/logo + team_project_links

Revision ID: f1a2b3c4d5e8
Revises: d6e7f8a9b0c1
Create Date: 2026-06-20 19:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "f1a2b3c4d5e8"
down_revision: str | None = "d6e7f8a9b0c1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("teams", sa.Column("lead_id", sa.Uuid(), nullable=True))
    op.add_column("teams", sa.Column("charter", sa.Text(), nullable=True))
    op.add_column(
        "teams",
        sa.Column(
            "logo_props",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
    )
    op.create_foreign_key(
        op.f("fk_teams_lead_id"), "teams", "users", ["lead_id"], ["id"], ondelete="SET NULL"
    )
    op.create_table(
        "team_project_links",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("team_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("role", sa.String(length=20), server_default="MEMBER", nullable=False),
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
            name=op.f("fk_team_project_links_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
            name=op.f("fk_team_project_links_team_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_team_project_links_project_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_team_project_links")),
        sa.UniqueConstraint(
            "team_id", "project_id", name=op.f("uq_team_project_links_team_project")
        ),
    )
    op.create_index("ix_team_project_links_org_id", "team_project_links", ["org_id"])


def downgrade() -> None:
    op.drop_index("ix_team_project_links_org_id", table_name="team_project_links")
    op.drop_table("team_project_links")
    op.drop_constraint(op.f("fk_teams_lead_id"), "teams", type_="foreignkey")
    op.drop_column("teams", "logo_props")
    op.drop_column("teams", "charter")
    op.drop_column("teams", "lead_id")
