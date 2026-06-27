"""fix project.network to store enum names (PRIVATE/PUBLIC)

The initial network migration defaulted to the lowercase value "private", but
non-native enums store the member NAME, so the API could not read those rows.
This normalizes any lowercase values and resets the column default.

Revision ID: a1c2e3f4b5d6
Revises: f0a1b2c3d4e5
Create Date: 2026-06-20 10:30:00.000000

"""

from collections.abc import Sequence

from alembic import op

revision: str = "a1c2e3f4b5d6"
down_revision: str | None = "f0a1b2c3d4e5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("UPDATE projects SET network = 'PRIVATE' WHERE network = 'private'")
    op.execute("UPDATE projects SET network = 'PUBLIC' WHERE network = 'public'")
    op.execute("ALTER TABLE projects ALTER COLUMN network SET DEFAULT 'PRIVATE'")


def downgrade() -> None:
    op.execute("ALTER TABLE projects ALTER COLUMN network SET DEFAULT 'private'")
