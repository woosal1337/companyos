"""activity notify trigger

Revision ID: c1d2e3f4a5b6
Revises: b7f3a9c21d04
Create Date: 2026-06-15 06:05:00.000000

"""

from collections.abc import Sequence

from alembic import op

revision: str = "c1d2e3f4a5b6"
down_revision: str | None = "b7f3a9c21d04"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION companyos_notify_activity() RETURNS trigger AS $func$
BEGIN
  PERFORM pg_notify('companyos_activity', json_build_object(
    'id', NEW.id,
    'org_id', NEW.org_id,
    'project_id', NEW.project_id,
    'actor_id', NEW.actor_id,
    'entity_type', NEW.entity_type,
    'entity_id', NEW.entity_id,
    'event_type', NEW.event_type
  )::text);
  RETURN NEW;
END;
$func$ LANGUAGE plpgsql;
"""

_TRIGGER_SQL = (
    "CREATE OR REPLACE TRIGGER trg_activity_events_notify "
    "AFTER INSERT ON activity_events "
    "FOR EACH ROW EXECUTE FUNCTION companyos_notify_activity();"
)


def upgrade() -> None:
    op.execute(_FUNCTION_SQL)
    op.execute(_TRIGGER_SQL)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_activity_events_notify ON activity_events;")
    op.execute("DROP FUNCTION IF EXISTS companyos_notify_activity();")
