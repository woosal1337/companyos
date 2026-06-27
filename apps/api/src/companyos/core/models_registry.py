"""Imports every model so Base.metadata is fully populated."""

from companyos.core.models_base import Base
from companyos.modules.activity.models import ActivityEvent
from companyos.modules.ai.models import (
    AIChatMessage,
    AIConversation,
    AIProviderKey,
    AIRun,
    AIUser,
)
from companyos.modules.approvals.models import TaskApproval
from companyos.modules.auth_providers.models import AuthProviderConfig
from companyos.modules.automation.models import AutomationRule
from companyos.modules.comments.models import Comment, CommentReaction, CommentVersion
from companyos.modules.customers.models import Customer, CustomerRequest
from companyos.modules.cycles.models import Cycle
from companyos.modules.dashboards.models import Dashboard, DashboardWidget
from companyos.modules.domains.models import OrgDomain
from companyos.modules.embeds.models import NoteEmbed
from companyos.modules.events.models import Event
from companyos.modules.favorites.models import Favorite
from companyos.modules.idp_sync.models import GroupRoleMapping
from companyos.modules.initiatives.models import Initiative, InitiativeUpdate
from companyos.modules.instance.models import InstanceLicense, InstanceSettings
from companyos.modules.intake.models import IntakeForm
from companyos.modules.integrations.git_models import GitRepoConnection
from companyos.modules.integrations.models import (
    EmailIntake,
    SentryIntake,
    SlackConnection,
)
from companyos.modules.ldap.models import LDAPConnection
from companyos.modules.mcp_auth.models import (
    OAuthAccessToken,
    OAuthAuthorizationCode,
    OAuthClient,
    OAuthGrant,
    OAuthRefreshToken,
    OAuthSigningKey,
)
from companyos.modules.mcp_connectors.models import McpConnector
from companyos.modules.mcp_server.models import McpIdempotencyKey
from companyos.modules.meeting_templates.models import MeetingRecipe, MeetingTemplate
from companyos.modules.meetings.models import (
    Meeting,
    MeetingShare,
    MeetingSummary,
    TranscriptSegment,
)
from companyos.modules.milestones.models import Milestone
from companyos.modules.modules.models import Module
from companyos.modules.notes.models import (
    Note,
    NoteShare,
    NoteTemplate,
    NoteVersion,
    PublicPageComment,
)
from companyos.modules.notifications.models import (
    DeviceToken,
    Notification,
    NotificationPreference,
)
from companyos.modules.orgs.models import (
    CustomRole,
    Invitation,
    Organization,
    OrganizationMember,
)
from companyos.modules.outbox.models import EventOutbox, WebhookEndpoint
from companyos.modules.projects.models import (
    Project,
    ProjectArtifact,
    ProjectMember,
    ProjectState,
    ProjectSubscription,
    ProjectTemplate,
    ProjectUpdate,
)
from companyos.modules.properties.models import CustomProperty, PropertyTemplate
from companyos.modules.rbac_audit.models import RbacAuditEvent
from companyos.modules.recurring.models import RecurringTaskRule
from companyos.modules.register.models import RegisterEntry
from companyos.modules.releases.models import ChangelogEntry, Release
from companyos.modules.retrospectives.models import Retrospective
from companyos.modules.runner.models import RunnerExecution, RunnerScript
from companyos.modules.scim.models import ScimToken
from companyos.modules.sso.models import SSOConnection
from companyos.modules.stickies.models import Sticky
from companyos.modules.storage.models import StoredObject
from companyos.modules.tasks.models import (
    Label,
    NotDuplicatePair,
    RelationTypeDef,
    Task,
    TaskDescriptionVersion,
    TaskLink,
    TaskNoteLink,
    TaskRelation,
    TaskScheduleLink,
    TaskSubscription,
    WorkItemTemplate,
    WorkItemTypeLevel,
    WorkItemUpdate,
)
from companyos.modules.teams.models import Team, TeamMember, TeamProjectLink
from companyos.modules.users.models import PersonalAccessToken, User
from companyos.modules.views.models import TaskView
from companyos.modules.vocabulary.models import VocabularyTerm
from companyos.modules.webhooks.models import ProjectWebhook
from companyos.modules.workflow.models import (
    TransitionCondition,
    WorkflowStatus,
    WorkflowTransition,
)
from companyos.modules.worklogs.models import Worklog

__all__ = [
    "AIChatMessage",
    "AIConversation",
    "AIProviderKey",
    "AIRun",
    "AIUser",
    "ActivityEvent",
    "AuthProviderConfig",
    "AutomationRule",
    "Base",
    "ChangelogEntry",
    "Comment",
    "CommentReaction",
    "CommentVersion",
    "CustomProperty",
    "CustomRole",
    "Customer",
    "CustomerRequest",
    "Cycle",
    "Dashboard",
    "DashboardWidget",
    "DeviceToken",
    "EmailIntake",
    "Event",
    "EventOutbox",
    "Favorite",
    "GitRepoConnection",
    "GroupRoleMapping",
    "Initiative",
    "InitiativeUpdate",
    "InstanceLicense",
    "InstanceSettings",
    "IntakeForm",
    "Invitation",
    "LDAPConnection",
    "Label",
    "McpConnector",
    "McpIdempotencyKey",
    "Meeting",
    "MeetingRecipe",
    "MeetingShare",
    "MeetingSummary",
    "MeetingTemplate",
    "Milestone",
    "Module",
    "NotDuplicatePair",
    "Note",
    "NoteEmbed",
    "NoteShare",
    "NoteTemplate",
    "NoteVersion",
    "Notification",
    "NotificationPreference",
    "OAuthAccessToken",
    "OAuthAuthorizationCode",
    "OAuthClient",
    "OAuthGrant",
    "OAuthRefreshToken",
    "OAuthSigningKey",
    "OrgDomain",
    "Organization",
    "OrganizationMember",
    "PersonalAccessToken",
    "Project",
    "ProjectArtifact",
    "ProjectMember",
    "ProjectState",
    "ProjectSubscription",
    "ProjectTemplate",
    "ProjectUpdate",
    "ProjectWebhook",
    "PropertyTemplate",
    "PublicPageComment",
    "RbacAuditEvent",
    "RecurringTaskRule",
    "RegisterEntry",
    "RelationTypeDef",
    "Release",
    "Retrospective",
    "RunnerExecution",
    "RunnerScript",
    "SSOConnection",
    "ScimToken",
    "SentryIntake",
    "SlackConnection",
    "Sticky",
    "StoredObject",
    "Task",
    "TaskApproval",
    "TaskDescriptionVersion",
    "TaskLink",
    "TaskNoteLink",
    "TaskRelation",
    "TaskScheduleLink",
    "TaskSubscription",
    "TaskView",
    "Team",
    "TeamMember",
    "TeamProjectLink",
    "TranscriptSegment",
    "TransitionCondition",
    "User",
    "VocabularyTerm",
    "WebhookEndpoint",
    "WorkItemTemplate",
    "WorkItemTypeLevel",
    "WorkItemUpdate",
    "WorkflowStatus",
    "WorkflowTransition",
    "Worklog",
]
