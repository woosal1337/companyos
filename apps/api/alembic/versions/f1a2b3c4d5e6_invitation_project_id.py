"""invitation project_id

An invitation may target a specific project. Accepting such an invite joins the
user to the organization AND that project. The link is ON DELETE SET NULL so
deleting the project before the invite is accepted simply drops the project
association — the org invite still works.

Revision ID: f1a2b3c4d5e6
Revises: a1b2c3d4e5f6
Create Date: 2026-06-18

"""

import sqlalchemy as sa
from alembic import op

revision = "f1a2b3c4d5e6"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("invitations", sa.Column("project_id", sa.Uuid(), nullable=True))
    op.create_index("ix_invitations_project_id", "invitations", ["project_id"])
    op.create_foreign_key(
        "fk_invitations_project_id_projects",
        "invitations",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_invitations_project_id_projects", "invitations", type_="foreignkey")
    op.drop_index("ix_invitations_project_id", table_name="invitations")
    op.drop_column("invitations", "project_id")
