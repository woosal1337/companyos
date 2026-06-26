import type { DocPage } from "./types";

export const DOC_PAGES: DocPage[] = [
  {
    "title": "Overview & Getting Started",
    "slug": "overview-getting-started",
    "description": "What CompanyOS is, the core concepts behind it, and how to sign up, create or join an organization, and find your way around the workspace.",
    "blocks": [
      {
        "type": "h2",
        "text": "What CompanyOS is"
      },
      {
        "type": "p",
        "text": "CompanyOS is the coordination layer for your company. Instead of scattering your work across a project tracker, a notes app, a meeting recorder, and a chat tool, CompanyOS puts your projects, tasks, notes, meetings, calendar, and a complete activity history in one connected system. Every item keeps its context, so when you open a task you can see the meeting it came from, the note that referenced it, and everything that happened to it since."
      },
      {
        "type": "p",
        "text": "It works the way a modern issue tracker does, with a fast board of Linear-style tasks, but it reaches further than tasks. Meetings get transcripts and AI summaries that capture what was decided and who owns it. A single activity feed threads tasks, meetings, and decisions into one timeline. And a company brain lets you ask questions across all of it."
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "The one rule that shapes everything",
        "text": "Every AI feature in CompanyOS runs on **your own model key**. You bring an OpenAI or Anthropic API key, store it once at the organization level, and all AI work, summaries, answers, agents, runs on that key. Your cost and your data stay where they belong, never in a shared pool. This is what BYOK (bring your own key) means throughout the product."
      },
      {
        "type": "h2",
        "text": "Core concepts"
      },
      {
        "type": "p",
        "text": "A handful of building blocks make up the whole system. Once these click, the rest of the product is just different views onto them."
      },
      {
        "type": "h3",
        "text": "Account"
      },
      {
        "type": "p",
        "text": "Your account is your personal login, identified by your email address and protected by a password. It carries your full name and email, and it is the identity that follows you across every organization you belong to. One account can be a member of many organizations at once."
      },
      {
        "type": "h3",
        "text": "Organization"
      },
      {
        "type": "p",
        "text": "An organization (or org) is a shared workspace for one company or team. It is the home for everything: your projects, tasks, notes, meetings, people, and your model key all live inside an organization. Each org has a name you choose and a short URL-friendly slug that CompanyOS generates from that name automatically. Your account can belong to several organizations, and you switch between them freely."
      },
      {
        "type": "p",
        "text": "Membership in an organization comes with a role that controls what you can do:"
      },
      {
        "type": "table",
        "headers": [
          "Role",
          "What it can do"
        ],
        "rows": [
          [
            "Owner",
            "Full control. The person who creates an organization becomes its owner. Owners can do everything an admin can, plus grant or change the owner role and manage other owners. An organization always keeps at least one owner."
          ],
          [
            "Admin",
            "Manages the organization: updates org details, invites and removes members, changes member roles, and configures the model key. Admins cannot grant the owner role."
          ],
          [
            "Member",
            "Works inside the organization: projects, tasks, notes, meetings, calendar, and activity. The default role for invited people."
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Project"
      },
      {
        "type": "p",
        "text": "A project is a container for related work inside an organization, the place where tasks live. Think of it as a workstream, a product area, or an initiative. When you create your very first organization, CompanyOS takes you straight to creating your first project, because a project is where day-to-day work actually happens."
      },
      {
        "type": "h3",
        "text": "Task"
      },
      {
        "type": "p",
        "text": "Tasks are the unit of work, in the Linear style: each has a title, a status, and can be assigned, prioritized, and dragged across a board. You reorder them across statuses and lanes with pointer-perfect drag-and-drop, and every task keeps a stable identifier so a conversation or a meeting summary can point straight back to it. Tasks assigned to you also gather in one personal place, My Tasks, so you never have to dig through every project to see your own plate."
      },
      {
        "type": "h3",
        "text": "Note"
      },
      {
        "type": "p",
        "text": "Notes are documents for the thinking that surrounds your work: specs, decisions, research, meeting prep, or anything you want written down. They live in the organization alongside projects and meetings, and because everything is connected, a note can reference a task or a meeting and that link is preserved."
      },
      {
        "type": "h3",
        "text": "Meeting"
      },
      {
        "type": "p",
        "text": "A meeting in CompanyOS is a recorded conversation that becomes searchable, structured knowledge. Each meeting can carry a transcript and an AI-generated summary tuned to surface what was decided and who owns it, rather than replaying the whole conversation back at you. You can ask questions of a meeting (\"ask the meeting\"), and that answer runs on your organization's own model key."
      },
      {
        "type": "h3",
        "text": "Activity feed"
      },
      {
        "type": "p",
        "text": "The activity feed is a single, live timeline of everything happening in your organization: tasks moving, meetings summarized, members added, decisions made. It is how context compounds. Because every meaningful change is recorded with who did it and when, you can open any item and the surrounding history is already there. The feed updates live as your team works."
      },
      {
        "type": "h3",
        "text": "Calendar"
      },
      {
        "type": "p",
        "text": "The calendar gives you a time-based view of your organization, so scheduled and dated work, including meetings, shows up where you expect it on a familiar grid."
      },
      {
        "type": "h3",
        "text": "The AI brain (company brain)"
      },
      {
        "type": "p",
        "text": "CompanyOS includes an AI layer that reads across your whole organization, projects, tasks, transcripts, notes, and people, so you can ask one question and get an answer drawn from every surface at once. This is also where AI agents (configurable AI members with their own model and instructions) and meeting summaries are powered. Everything the brain does executes on your organization's own provider key."
      },
      {
        "type": "h3",
        "text": "BYOK (bring your own key)"
      },
      {
        "type": "p",
        "text": "BYOK is how CompanyOS runs AI without ever touching a shared, pooled model account. An admin or owner stores an OpenAI or Anthropic API key once at the organization level. The key is kept securely and only ever shown to you masked (just the last four characters). You can mark one key as the default, and you can swap or rotate keys with no downtime, work that is already in flight finishes on the key it started on. From then on, every AI feature in your org runs on that key, so the cost lands on your provider bill and your data stays under your control."
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "Set up your key early",
        "text": "AI features (meeting summaries, asking the meeting, the company brain, AI agents) need a model key before they can run. If you are an owner or admin, add an OpenAI or Anthropic key in **Settings** soon after you create your organization so the AI surfaces are ready when your team needs them."
      },
      {
        "type": "h2",
        "text": "Getting started"
      },
      {
        "type": "p",
        "text": "Going from nothing to a working workspace takes three moves: create your account, get into an organization (create one or accept an invite), then learn the layout. Here is each one."
      },
      {
        "type": "h3",
        "text": "1. Create your account"
      },
      {
        "type": "p",
        "text": "Head to company.chele.bi and choose to start free, which opens the sign-up page."
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open sign-up",
            "text": "Go to https://company.chele.bi and select Start free, or go straight to the Create your account page."
          },
          {
            "title": "Enter your details",
            "text": "Provide your full name, your email address, and a password. Passwords must be at least 8 characters."
          },
          {
            "title": "Create the account",
            "text": "Select Create account. CompanyOS signs you in immediately and takes you to the workspace chooser to set up or pick an organization."
          }
        ]
      },
      {
        "type": "p",
        "text": "Already have an account? Use the Sign in link instead. On the login page you enter your email and password and select Sign in, which drops you back into your most recent workspace."
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "Staying signed in",
        "text": "CompanyOS keeps you logged in with a secure session, so you do not have to re-enter your password every visit. To sign out, open the user menu at the bottom-left of the workspace and choose Log out."
      },
      {
        "type": "h3",
        "text": "2a. Create an organization"
      },
      {
        "type": "p",
        "text": "If you are starting a new company workspace, you create the organization and automatically become its owner."
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open the workspace chooser",
            "text": "Right after sign-up you land on Choose a workspace. If you already have orgs, you can also create a new one from the org switcher at the top of the sidebar (the New organization option)."
          },
          {
            "title": "Start a new organization",
            "text": "Select New organization (or Create organization if this is your first one)."
          },
          {
            "title": "Name it",
            "text": "Enter a name like Acme Inc. CompanyOS creates a matching slug for you automatically, no need to set one."
          },
          {
            "title": "Create",
            "text": "Select Create. You become the owner, and CompanyOS takes you straight into creating your first project so you can start working immediately."
          }
        ]
      },
      {
        "type": "h3",
        "text": "2b. Join an organization by invite"
      },
      {
        "type": "p",
        "text": "If a teammate is adding you to an existing organization, an admin or owner sends you an invitation tied to your email address. You accept it through a one-time link."
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open the invite link",
            "text": "Click the invite link your admin shared. It opens the Accept your invite page."
          },
          {
            "title": "Sign in with the invited email",
            "text": "You must be signed in with the exact email address the invite was sent to. If you are on a different account, use Sign in or create one with the right email first."
          },
          {
            "title": "Accept the invite",
            "text": "Select Accept invite. You join the organization with the role your admin assigned (usually member), and CompanyOS drops you into the org's projects."
          }
        ]
      },
      {
        "type": "callout",
        "variant": "warning",
        "title": "Invites expire",
        "text": "An invitation is valid for 7 days and can only be used once, by the email it was issued to. If your link has expired or was sent to the wrong address, the accept page will tell you, ask your admin to send a fresh one."
      },
      {
        "type": "h3",
        "text": "3. The workspace layout"
      },
      {
        "type": "p",
        "text": "Once you are inside an organization, every page shares the same frame: a sidebar on the left, a top bar across the top, and your current view filling the rest of the screen."
      },
      {
        "type": "h3",
        "text": "The sidebar (navigation)"
      },
      {
        "type": "p",
        "text": "The left sidebar is how you move between sections. At the very top sits the organization switcher, showing your current org. Below it, navigation is grouped into two sections, Personal (what is on your plate) and Workspace (the shared surfaces of the org). At the very bottom is your user menu."
      },
      {
        "type": "table",
        "headers": [
          "Section",
          "Item",
          "What it opens"
        ],
        "rows": [
          [
            "Personal",
            "My Tasks",
            "Every task assigned to you across all projects, in one personal list."
          ],
          [
            "Personal",
            "Inbox",
            "Your personal inbox of things needing your attention."
          ],
          [
            "Personal",
            "Triage",
            "Incoming items and automations to sort and route."
          ],
          [
            "Personal",
            "Notes",
            "Your notes and documents."
          ],
          [
            "Workspace",
            "Projects",
            "All projects in the organization and their task boards. This is the default landing page."
          ],
          [
            "Workspace",
            "Meetings",
            "Recorded meetings with transcripts and AI summaries."
          ],
          [
            "Workspace",
            "Calendar",
            "A time-based view of the organization."
          ],
          [
            "Workspace",
            "Activity",
            "The live, organization-wide activity feed."
          ],
          [
            "Workspace",
            "Settings",
            "Organization settings, members and invites, and your model key."
          ]
        ]
      },
      {
        "type": "p",
        "text": "The sidebar is yours to arrange. Drag any item to reorder it, or right-click (or use its options menu) to Pin to top or move it to a collapsible More group at the bottom to keep your nav focused. Your layout is remembered on your device."
      },
      {
        "type": "h3",
        "text": "The top bar"
      },
      {
        "type": "p",
        "text": "The bar across the top of every page shows the name of the section you are in. On the right it has two tools you will use constantly:"
      },
      {
        "type": "ul",
        "items": [
          "**Search / command palette.** Select Search, or press ⌘K (Cmd-K on Mac, Ctrl-K on Windows), to jump anywhere or run quick actions without leaving the keyboard. One query spans projects, transcripts, and people.",
          "**Notification bell.** Shows alerts about things that need you, mentions, assignments, and updates from across the organization."
        ]
      },
      {
        "type": "h3",
        "text": "The user menu"
      },
      {
        "type": "p",
        "text": "At the bottom-left of the sidebar is your user menu, showing your name and email. Open it to jump to Org settings or to Log out of your account."
      },
      {
        "type": "h3",
        "text": "Switching organizations"
      },
      {
        "type": "p",
        "text": "If you belong to more than one organization, you move between them from the organization switcher at the top of the sidebar."
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open the switcher",
            "text": "Select the organization name and logo at the top of the sidebar."
          },
          {
            "title": "Pick another org",
            "text": "Choose any organization from the list. A checkmark marks the one you are currently in. CompanyOS switches you over and opens that org's projects."
          },
          {
            "title": "Or create a new one",
            "text": "Select New organization at the bottom of the switcher to spin up another workspace."
          }
        ]
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "CompanyOS remembers where you left off",
        "text": "Your most recently used organization is remembered, so the next time you open CompanyOS it takes you right back to it. If you belong to exactly one organization, you skip the chooser entirely and land straight in your workspace."
      },
      {
        "type": "h2",
        "text": "What's next"
      },
      {
        "type": "p",
        "text": "You now have an account, an organization, and a feel for how to get around. From here, dive into the section that matches what you want to do:"
      },
      {
        "type": "ul",
        "items": [
          "**Projects & Tasks**, create projects, run the Linear-style task board, assign and prioritize work, and use My Tasks.",
          "**Notes**, write and organize documents, and connect them to your work.",
          "**Meetings**, record meetings, read transcripts and AI summaries, and ask questions of a meeting.",
          "**Activity & Calendar**, follow the organization-wide timeline and the time-based view.",
          "**Triage & Automations**, sort incoming items and set up automations to route work.",
          "**AI & BYOK**, add your OpenAI or Anthropic key, set up AI agents, and use the company brain.",
          "**Settings & Members**, manage org details, invite and manage people, and assign roles.",
          "**Company-brain MCP**, the more technical guide to connecting CompanyOS to external tools."
        ]
      }
    ]
  },
  {
    "blocks": [
      {
        "type": "h2",
        "text": "Organizations, teams, and members"
      },
      {
        "type": "p",
        "text": "An **organization** (org) is the home for everything in CompanyOS: your projects, tasks, notes, meetings, the activity log, and your people. Every screen in the app lives inside one org, and every org is fully separate from every other one. People you invite see only the org they were invited to. This page covers how to create an org, configure it, invite people, manage roles, and group members into teams."
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "Where this all lives",
        "text": "Most of what follows happens under **Settings**, reachable at `/app/<your-org>/settings`. Settings is organized into tabs: **General**, **Members**, **Teams**, **AI**, **AI Access**, **Vocabulary**, **Templates**, **Workflow**, and **Automations**. This page focuses on General, Members, and Teams."
      },
      {
        "type": "h2",
        "text": "Creating an organization"
      },
      {
        "type": "p",
        "text": "When you first sign in, CompanyOS sends you to a workspace picker that lists every org you belong to. If you have exactly one org, it takes you straight in. If you have none, it prompts you to create your first one."
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open the workspace picker",
            "text": "Go to the app. If you are not auto-redirected into an org, you will land on the \"Choose a workspace\" screen that lists your organizations."
          },
          {
            "title": "Click \"New organization\"",
            "text": "Use the button in the header of the organizations card. If you have no orgs yet, the empty state shows a \"Create organization\" button instead with the same effect."
          },
          {
            "title": "Name it",
            "text": "Enter a name such as \"Acme Inc\". The name must be at least 2 characters. There is no separate description field at creation time; you can add a description later via the API, and rename anytime in Settings."
          },
          {
            "title": "Click \"Create\"",
            "text": "CompanyOS creates the org and drops you straight into your first project so you can start working immediately."
          }
        ]
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "You become the owner automatically",
        "text": "Whoever creates an org is made its **owner**. CompanyOS also seeds a default task workflow (the set of statuses your tasks move through) for the new org so you can start creating tasks right away."
      },
      {
        "type": "h3",
        "text": "About the slug"
      },
      {
        "type": "p",
        "text": "Every org gets a URL-friendly **slug** derived from its name (for example, \"Acme Inc\" becomes `acme-inc`). The slug is unique across all of CompanyOS. If your chosen name produces a slug that is already taken, a short random suffix is added automatically (for example, `acme-inc-4f9a2c`). The slug is stable: renaming your org does not change it."
      },
      {
        "type": "h2",
        "text": "Organization settings (General)"
      },
      {
        "type": "p",
        "text": "The **General** tab under Settings is where you manage the org's core identity. The main card lets you rename the organization."
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open Settings → General",
            "text": "Navigate to Settings and stay on the default General tab."
          },
          {
            "title": "Edit the name",
            "text": "Change the value in the Name field. The Slug field below it is shown but disabled, because the slug never changes after creation."
          },
          {
            "title": "Save changes",
            "text": "Click \"Save changes\". The button stays disabled until your new name is at least 2 characters and actually different from the current name."
          }
        ]
      },
      {
        "type": "p",
        "text": "The General tab also surfaces two related panels: **Deleted projects** (where you can review and restore projects that were removed) and **Project notifications** (where you tune which project events notify you). Renaming the org is recorded in the activity log."
      },
      {
        "type": "callout",
        "variant": "warning",
        "title": "Renaming is an admin action",
        "text": "Editing the organization requires **admin** or **owner** role. A plain member who opens General will be able to view it but the save will be rejected by the server."
      },
      {
        "type": "h2",
        "text": "Members and roles"
      },
      {
        "type": "p",
        "text": "Everyone with access to an org is a **member** of it, and every member holds exactly one of three roles. The roles are a strict hierarchy: an owner outranks an admin, who outranks a member."
      },
      {
        "type": "table",
        "headers": [
          "Role",
          "Rank",
          "In one line"
        ],
        "rows": [
          [
            "Owner",
            "Highest",
            "Full control, including managing other owners and the org's existence."
          ],
          [
            "Admin",
            "Middle",
            "Day-to-day management: people, teams, projects, invites, settings."
          ],
          [
            "Member",
            "Base",
            "Does the work: projects, tasks, notes, meetings. No management powers."
          ]
        ]
      },
      {
        "type": "h3",
        "text": "What each role can do"
      },
      {
        "type": "p",
        "text": "CompanyOS enforces roles on the server, so these limits hold no matter what the UI shows. The key dividing line is that managing the org (people, teams, invites, projects, org settings) requires **admin or higher**, while a few sensitive actions are reserved for **owners** only."
      },
      {
        "type": "table",
        "headers": [
          "Action",
          "Member",
          "Admin",
          "Owner"
        ],
        "rows": [
          [
            "Use the org: view and work on projects, tasks, notes, meetings",
            "Yes",
            "Yes",
            "Yes"
          ],
          [
            "See the members list and teams",
            "Yes",
            "Yes",
            "Yes"
          ],
          [
            "Rename the organization / edit settings",
            "No",
            "Yes",
            "Yes"
          ],
          [
            "Invite people (as member or admin)",
            "No",
            "Yes",
            "Yes"
          ],
          [
            "Revoke a pending invite",
            "No",
            "Yes",
            "Yes"
          ],
          [
            "Change a member's role (member ↔ admin)",
            "No",
            "Yes",
            "Yes"
          ],
          [
            "Remove a member",
            "No",
            "Yes",
            "Yes"
          ],
          [
            "Create, rename, and delete teams; manage team membership",
            "No",
            "Yes",
            "Yes"
          ],
          [
            "Create, archive, and manage projects",
            "No",
            "Yes",
            "Yes"
          ],
          [
            "Invite someone as owner, or grant/change an owner role",
            "No",
            "No",
            "Yes"
          ],
          [
            "Remove an existing owner",
            "No",
            "No",
            "Yes"
          ]
        ]
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "Owner is a superset of admin",
        "text": "Anything an admin can do, an owner can do too. The owner-only rows above are the extra powers that admins do not have: everything to do with creating or touching other owners."
      },
      {
        "type": "h3",
        "text": "Viewing the members list"
      },
      {
        "type": "p",
        "text": "Open Settings → **Members**. The Members card lists everyone in the org with their name, email, and role, in the order they joined. Your own row is marked with \"(you)\"."
      },
      {
        "type": "p",
        "text": "If you are an admin or owner, each row shows a role dropdown and a remove button so you can manage people inline. If you are a plain member, you see the same list but roles appear as read-only badges and there are no management controls."
      },
      {
        "type": "h3",
        "text": "Changing a member's role"
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open Settings → Members",
            "text": "You must be an admin or owner to see the role controls."
          },
          {
            "title": "Find the person",
            "text": "Locate their row in the Members list."
          },
          {
            "title": "Pick a new role",
            "text": "Use the role dropdown on their row and choose owner, admin, or member. The change saves immediately."
          }
        ]
      },
      {
        "type": "p",
        "text": "There are guardrails to keep the org safe:"
      },
      {
        "type": "ul",
        "items": [
          "**You cannot change your own role.** This prevents an admin from accidentally self-promoting and prevents an owner from self-demoting out of control.",
          "**Only an owner can grant, modify, or remove an owner role.** An admin can move people between member and admin, but cannot touch anyone who is (or is becoming) an owner.",
          "**The last owner cannot be demoted.** If there is only one owner left, the system refuses to lower their role, so an org always has at least one owner."
        ]
      },
      {
        "type": "h3",
        "text": "Removing a member"
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open Settings → Members",
            "text": "Admin or owner only."
          },
          {
            "title": "Click the remove (trash) button",
            "text": "It sits at the end of the person's row. Your own row's remove button is disabled, so you cannot remove yourself this way."
          },
          {
            "title": "Confirm",
            "text": "The member loses access to the org immediately."
          }
        ]
      },
      {
        "type": "callout",
        "variant": "warning",
        "title": "Removal also clears their team and project memberships",
        "text": "When you remove someone from the org, CompanyOS also strips them out of every team and every project they belonged to within that org, in the same step, so nothing is left pointing at a person who no longer has access. The same owner protections apply: only an owner can remove an owner, and the last owner cannot be removed."
      },
      {
        "type": "h2",
        "text": "Inviting people by email"
      },
      {
        "type": "p",
        "text": "You add people to an org by inviting them by email. They do not need a CompanyOS account yet. When they accept (after signing in or signing up with that same email), they become members."
      },
      {
        "type": "h3",
        "text": "Sending an invite"
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open Settings → Members",
            "text": "The \"Invite people\" card appears only if you are an admin or owner."
          },
          {
            "title": "Enter their email",
            "text": "Type the address you want to invite, for example teammate@company.com."
          },
          {
            "title": "Choose a role",
            "text": "Pick the role they will join as. The dropdown offers member or admin. To invite someone directly as an owner, you must be an owner yourself (see note below)."
          },
          {
            "title": "Click \"Invite\"",
            "text": "CompanyOS creates the invitation and shows you a copyable invite link."
          },
          {
            "title": "Share the link",
            "text": "Click the copy icon to grab the invite URL and send it to the person however you like. The link is the fastest way to get them in."
          }
        ]
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "The invite link is shown once",
        "text": "The one-time invite token is only returned at the moment you create the invite, which is why the copyable link appears right after you click Invite. The token itself is never stored in readable form, so if you lose the link, revoke the invite and send a fresh one rather than trying to recover it."
      },
      {
        "type": "p",
        "text": "A few rules apply when creating invites:"
      },
      {
        "type": "ul",
        "items": [
          "**Default role is member** if you do not pick one.",
          "**One pending invite per email per org.** If there is already an unaccepted invite for that address, you cannot create a second one. Revoke the first if you need to change the role.",
          "**No inviting existing members.** If the email already belongs to a member of this org, the invite is rejected.",
          "**Invites expire after 7 days.** After that the link no longer works and you will need to send a new one.",
          "**Owner invites are owner-only.** Only an owner can invite someone as an owner; an admin attempting it is blocked."
        ]
      },
      {
        "type": "h3",
        "text": "Pending invites and revoking"
      },
      {
        "type": "p",
        "text": "Below the invite form, the \"Invite people\" card lists every **pending** invite with its email and role. Each one has a trash button. Click it to revoke an invite you no longer want; the link immediately stops working. Only invites that are still pending can be revoked (an already-accepted or expired one cannot)."
      },
      {
        "type": "h2",
        "text": "Accepting an invite"
      },
      {
        "type": "p",
        "text": "When you receive an invite link, it points to a page that joins you to the organization. You must be signed in with the same email the invite was sent to."
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open the invite link",
            "text": "It takes you to an \"Accept your invite\" page."
          },
          {
            "title": "Sign in or sign up with the invited email",
            "text": "If you are not signed in, use the \"Sign in\" or \"create one\" links on that page. The account must use the exact email the invite was issued to, otherwise the server rejects it."
          },
          {
            "title": "Click \"Accept invite\"",
            "text": "CompanyOS adds you to the organization and takes you straight to its projects."
          }
        ]
      },
      {
        "type": "p",
        "text": "If acceptance fails, the page tells you the invite could not be accepted: it may have expired, already been used, or been issued to a different account. In that case, ask an admin or owner to send a new one. Common reasons an accept is refused:"
      },
      {
        "type": "ul",
        "items": [
          "**Wrong account.** The invite was issued to a different email than the one you are signed in with.",
          "**Expired.** More than 7 days have passed; the invite is marked expired on the spot.",
          "**Already used or revoked.** The invite is no longer pending.",
          "**Already a member.** You are already in that org, so there is nothing to accept."
        ]
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "Elevated invites are re-checked at accept time",
        "text": "If you were invited as an admin or owner, CompanyOS double-checks the inviter's standing at the moment you accept. If the person who invited you has since been demoted or removed and no longer holds that level of authority, the elevated grant is rejected as stale. This keeps demoted or departed staff from leaving behind invites that would hand out power they no longer have."
      },
      {
        "type": "h2",
        "text": "Teams"
      },
      {
        "type": "p",
        "text": "A **team** is a named group of members inside an org, used to organize ownership: teams own projects. Teams are lightweight: a team has a name and an optional description, and a set of members drawn from the org. The same person can be on more than one team."
      },
      {
        "type": "h3",
        "text": "Creating and editing teams"
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open Settings → Teams",
            "text": "The create form and the per-team controls appear only if you are an admin or owner. Members see the team list read-only."
          },
          {
            "title": "Create a team",
            "text": "Type a name (for example \"Platform\", at least 2 characters) in the \"New team name\" field and click \"Add team\". Team names must be unique within the org."
          },
          {
            "title": "Rename a team",
            "text": "Click the pencil icon on a team row, edit the name inline, and click the check to save (or the X to cancel)."
          },
          {
            "title": "Delete a team",
            "text": "Click the trash icon on the team row and confirm in the dialog."
          }
        ]
      },
      {
        "type": "callout",
        "variant": "warning",
        "title": "Deleting a team is permanent",
        "text": "Deleting a team cannot be undone. Any projects owned by that team lose their team assignment (the projects themselves are not deleted). The team's members simply stop being on that team; they keep their org membership."
      },
      {
        "type": "h3",
        "text": "Team membership"
      },
      {
        "type": "p",
        "text": "You can only add someone to a team if they are already a member of the org. CompanyOS rejects adding a non-member, and it will not add the same person to a team twice. Managing team membership (adding and removing people) is an admin-or-owner action, like the rest of team management. When you remove someone from the whole org, they are taken off all their teams automatically."
      },
      {
        "type": "h2",
        "text": "Quick reference: who can manage what"
      },
      {
        "type": "p",
        "text": "If you ever wonder why a button is missing or an action is refused, it comes down to your role. Management surfaces (invite people, change roles, remove members, create or edit teams, manage projects, edit org settings) require **admin or owner**. The handful of owner-only actions all concern other owners: inviting as owner, granting or changing an owner role, and removing an owner. Everything else, the actual work in projects, tasks, notes, and meetings, is open to every member."
      }
    ],
    "description": "User guide page covering CompanyOS organizations, teams, members, roles, and invitations",
    "slug": "organizations-teams-members",
    "title": "Organizations, Teams & Members"
  },
  {
    "blocks": [
      {
        "type": "h2",
        "text": "Projects and tasks: the core of CompanyOS"
      },
      {
        "type": "p",
        "text": "Projects are how you group a stream of work, and tasks are the individual pieces of that work. Together they are the spine that everything else in CompanyOS hangs off: meetings turn into tasks, notes spin off tasks, the activity log records every status change, and your notifications and inbox are driven by tasks you are assigned to or watching. If you have used Linear, the model will feel familiar. Every task gets a short, human identifier like `WEB-42`, moves through a small set of statuses, and lives on a board you can drag work across."
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "Where this lives",
        "text": "Projects live at **company.chele.bi → Projects**. Each project opens to its own workspace with tabs for Overview, Board, Tasks, Meetings, Notes, and Members. **My Tasks** in the sidebar collects everything assigned to you across every project."
      },
      {
        "type": "h2",
        "text": "Projects"
      },
      {
        "type": "h3",
        "text": "What a project is"
      },
      {
        "type": "p",
        "text": "A project is a named container for related work, scoped to your organization. It holds tasks, meetings, and notes, plus a living brief (the Overview) where you write the vision and pin links. Each project has a unique **key** (the short prefix in front of every task number), an **active** or **archived** status, an optional **lead** and **target date**, and a set of **members** who can see and work in it. Projects can also be attached to a team."
      },
      {
        "type": "h3",
        "text": "The project key"
      },
      {
        "type": "p",
        "text": "The key is the most important decision you make when creating a project, because it becomes permanent shorthand for every task inside it. A project keyed `WEB` produces tasks `WEB-1`, `WEB-2`, `WEB-3`, and so on. The key must be **2 to 6 uppercase letters** (`WEB`, `OPS`, `GROWTH`) and must be **unique within your organization** — two projects cannot share a key. Pick something short and obvious; it is what people will type and say out loud."
      },
      {
        "type": "callout",
        "variant": "warning",
        "title": "Choose the key carefully",
        "text": "The key is set at creation and is not editable afterward through the app. The name, description, lead, target date, team, and status can all be changed later, but task identifiers are built from the key, so changing it would rewrite every identifier. Get it right the first time."
      },
      {
        "type": "h3",
        "text": "Creating a project"
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open Projects and click New project",
            "text": "From the Projects page, click **New project**. If you have no projects yet, the empty state offers the same button plus a shortcut to import work from a meeting."
          },
          {
            "title": "Enter a name",
            "text": "Type a clear name like \"Website redesign\". The name must be at least 2 characters and can be up to 255."
          },
          {
            "title": "Set the key",
            "text": "Enter 2 to 6 uppercase letters, for example WEB. The field forces uppercase. If a project in your org already uses that key, creation is rejected and you will need a different one."
          },
          {
            "title": "Add a description (optional)",
            "text": "Describe what the project is about. You can flesh this out later in the Overview brief with rich formatting, mentions, and links."
          },
          {
            "title": "Create",
            "text": "Click Create project. You are now a member of it automatically, and you land in its workspace ready to add tasks."
          }
        ]
      },
      {
        "type": "p",
        "text": "When you create a project you become its first member. Behind the scenes the org also records a \"project created\" entry in the activity log, so the team can see it appear."
      },
      {
        "type": "h3",
        "text": "The Overview brief"
      },
      {
        "type": "p",
        "text": "The Overview tab is a living brief, not a static description. It is a full rich-text editor: type `/` for blocks (headings, lists, and more) and `@` to mention a teammate or link a task. It **autosaves** as you type, showing a \"Saving…\" / \"Saved\" indicator, and you can flip to a clean preview with the eye icon. A sidebar shows project metadata (key, status, member count, created date) and a **Linked artifacts** list where you paste Figma files, docs, PRs, or any URL with an optional label. Plain domains get `https://` added for you."
      },
      {
        "type": "h3",
        "text": "Project settings you can change"
      },
      {
        "type": "p",
        "text": "After creation you can update the project's name, description, status (active or archived), assigned team, lead, and target date. Archiving a project keeps it and its history intact but takes it out of active flow — archived projects show an \"Archived\" badge, and you cannot create or change tasks inside an archived project until you set it active again."
      },
      {
        "type": "table",
        "headers": [
          "Field",
          "Editable later",
          "Notes"
        ],
        "rows": [
          [
            "Name",
            "Yes",
            "1–255 characters."
          ],
          [
            "Key",
            "No",
            "2–6 uppercase letters, unique per org. Fixed at creation."
          ],
          [
            "Description / brief",
            "Yes",
            "Edited as rich text in the Overview tab, autosaved."
          ],
          [
            "Status",
            "Yes",
            "Active or Archived. Archiving freezes task editing."
          ],
          [
            "Team",
            "Yes",
            "Optional owning team."
          ],
          [
            "Lead",
            "Yes",
            "Optional person who owns the project."
          ],
          [
            "Target date",
            "Yes",
            "Optional ship date."
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Project members"
      },
      {
        "type": "p",
        "text": "Members are the people who can work in a project. Assignees must be members — you cannot assign a task to someone who is not on the project. Adding and removing members is an **admin** action, done from the Members tab. A few rules keep projects sane: a person must already belong to your organization before you can add them to a project, you cannot remove yourself, and a project must always keep at least one member, so the last member cannot be removed. When you are added to a project, you get a notification."
      },
      {
        "type": "h3",
        "text": ""
      },
      {
        "type": "p",
        "text": "Independently of membership, you can **subscribe** to a project to opt into its notification stream. Subscribing and unsubscribing is a personal toggle and does not affect your access or anyone else's."
      },
      {
        "type": "h3",
        "text": "Deleting and restoring a project"
      },
      {
        "type": "p",
        "text": "Deleting a project is an **admin** action and is a **soft delete** — the project disappears from the active list but is recoverable for **30 days**. Within that window an admin can view deleted projects and restore one back to active. After 30 days it falls out of the recovery window and can no longer be restored."
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "Archive vs delete",
        "text": "Archive when work is done but you want to keep the project visible and its history browsable. Delete only when you want it gone — and remember you have a 30-day grace period to undo it."
      },
      {
        "type": "h2",
        "text": "Tasks: the Linear-style system"
      },
      {
        "type": "h3",
        "text": ""
      },
      {
        "type": "p",
        "text": "Every task gets a stable identifier of the form `KEY-number`, for example `WEB-42`. The number is assigned **per project** and counts up from 1: the first task in the `WEB` project is `WEB-1`, the next is `WEB-2`, and so on. Numbering is allocated under a per-project lock, so even if several people create tasks at the same moment, no two tasks ever collide on a number and there are no gaps from race conditions. The identifier is what you reference in conversation, search, and links."
      },
      {
        "type": "h3",
        "text": "Statuses and the workflow"
      },
      {
        "type": "p",
        "text": "A task moves through a fixed set of statuses. Five of them appear as columns on the board, in this order:"
      },
      {
        "type": "table",
        "headers": [
          "Status",
          "What it means",
          "Category"
        ],
        "rows": [
          [
            "Backlog",
            "Captured but not committed to.",
            "Backlog"
          ],
          [
            "Todo",
            "Committed, not started.",
            "Unstarted"
          ],
          [
            "In Progress",
            "Actively being worked on.",
            "Started"
          ],
          [
            "In Review",
            "Work done, awaiting review.",
            "Started"
          ],
          [
            "Done",
            "Completed.",
            "Completed"
          ],
          [
            "Cancelled",
            "Dropped, will not be done.",
            "Cancelled"
          ]
        ]
      },
      {
        "type": "p",
        "text": "There is also a **Duplicate** status used when a task is folded into another; it is treated like Cancelled for progress and is not shown as its own board column. Each status maps to an immutable **category** — Backlog, Unstarted, Started, Completed, or Cancelled. Categories are the stable spine that progress math and focus ordering read, so the system understands \"this is started work\" regardless of the exact status label."
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "How progress is calculated",
        "text": "A project's progress bar and a parent task's sub-task pill both use category math. Cancelled and Duplicate tasks are **excluded from the total entirely** (they do not drag your percentage down), and only Completed counts toward done. So progress reflects real, in-flight work — not abandoned work."
      },
      {
        "type": "h3",
        "text": "Priorities"
      },
      {
        "type": "p",
        "text": "Priority orders attention. The levels, highest to lowest, are **Urgent**, **High**, **Medium**, **Low**, and **No priority** (the default). Priority drives the ordering in My Tasks and in priority swimlanes on the board. Marking a task **Urgent** when it has an assignee sends that person an urgent notification, so it is a real signal, not just a color."
      },
      {
        "type": "h3",
        "text": "Assignees"
      },
      {
        "type": "p",
        "text": "A task can have one assignee, and the assignee must be a **member of the project**. Assigning someone (other than yourself) notifies them and auto-subscribes them so they follow the task. You can clear an assignee to leave a task unassigned. The assignee dropdown only lists people who are on the project."
      },
      {
        "type": "h3",
        "text": "Labels"
      },
      {
        "type": "p",
        "text": "Labels are org-scoped tags with a name and a color, shared across all projects. You create them once for the organization (each name is unique) and then attach any number of them to a task. Labels are useful for cross-cutting themes like \"design\", \"infra\", or \"customer-request\". You can filter and you can delete a label org-wide when it is no longer needed."
      },
      {
        "type": "h3",
        "text": "Due dates"
      },
      {
        "type": "p",
        "text": "Any task can carry an optional due date. For **bugs**, if you do not set one, CompanyOS derives a due date automatically from the bug's severity as an SLA: Critical is due in 1 day, High in 3, Medium in 7, and Low in 30. (More on bugs below.)"
      },
      {
        "type": "h3",
        "text": "Tasks vs bugs"
      },
      {
        "type": "p",
        "text": "A task has a **kind**: an ordinary **Task**, or a **Bug**. A bug must always have a **severity** (Low, Medium, High, or Critical) — you cannot save a bug without one, and switching a bug back to a plain task clears the severity. Severity drives the SLA due date above and shows as a badge on the card. This supports a zero-bug practice where every bug carries an explicit severity and deadline."
      },
      {
        "type": "h2",
        "text": "Creating tasks"
      },
      {
        "type": "p",
        "text": "There are several ways to add a task, from fastest to most detailed."
      },
      {
        "type": "h3",
        "text": "Inline on the board (fastest)"
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open a project's Board tab",
            "text": "Each status column has an Add task affordance at the bottom (and a + in the column header). You can also press the c shortcut."
          },
          {
            "title": "Type a title and press Enter",
            "text": "The task is created instantly in that column's status. The composer stays open so you can keep adding tasks one after another."
          },
          {
            "title": "Switch to Bug if needed",
            "text": "A small Task / Bug toggle lets you create the row as a bug (severity defaults to Medium). For more fields, click Add details to open the full dialog with your title carried over."
          }
        ]
      },
      {
        "type": "h3",
        "text": "The full New task dialog"
      },
      {
        "type": "p",
        "text": "From the board's Add details, the Tasks tab's New task button, or the `c` shortcut, you get the full form. Here you set the **title** (required), a **description** (supports context, links, acceptance criteria), the **type** (Task or Bug, with **severity** when it is a bug), and the starting **status**, **priority**, and **assignee**. The assignee list is limited to project members."
      },
      {
        "type": "h3",
        "text": "From meetings and notes"
      },
      {
        "type": "p",
        "text": "Tasks can be created with provenance — a link back to the meeting or note they came from. You can batch-create several tasks at once from a list of text lines (for example, action items extracted from a meeting), all sharing the same source. When a meeting-derived task is later marked **Done**, CompanyOS records that back on the meeting and notifies the attendees, closing the loop."
      },
      {
        "type": "h3",
        "text": "Sub-tasks"
      },
      {
        "type": "p",
        "text": "A task can have sub-tasks, managed from the task detail panel. Sub-tasks live in the **same project** as their parent and are limited to **one level** — a sub-task cannot itself have sub-tasks. The parent shows a progress pill (for example 2/5) computed from its sub-tasks using category math, so cancelled sub-tasks do not count against it."
      },
      {
        "type": "h2",
        "text": "Updating, moving, and transitioning tasks"
      },
      {
        "type": "h3",
        "text": "Editing fields"
      },
      {
        "type": "p",
        "text": "Open any task to edit it. The title and description save when you click away (on blur). Status, priority, assignee, type, and severity each have their own picker in the detail panel and apply the moment you change them. You can also change labels and due date. There is a short **grace window** right after a task is created during which routine edits do not spam the activity log — useful while you are still filling a task in."
      },
      {
        "type": "h3",
        "text": "Moving a task between statuses"
      },
      {
        "type": "p",
        "text": "On the board, move a task by opening its card menu (the … on hover) and picking a new status under **Move to**, which lists every status except the current one. On the list view and detail panel you change status from the Status picker. Every transition is recorded in the activity log with the from/to statuses. Transitioning to Done on a meeting-sourced task fires the meeting loop-closing described above, and status changes can also trigger your triage automations."
      },
      {
        "type": "h3",
        "text": "Bulk actions"
      },
      {
        "type": "p",
        "text": "On the board and the list, you can select multiple tasks (click, Shift-click for a range, Cmd/Ctrl-click to toggle). A floating action bar then lets you set **Status**, **Priority**, or **Assignee** on all of them at once, or **Archive** the selection (which sets them to Cancelled). Press `X` to clear the selection."
      },
      {
        "type": "h3",
        "text": "Relations: blocks, blocked by, related"
      },
      {
        "type": "p",
        "text": "From a task's detail you can link it to another task as **blocks**, **blocked by**, or **related**. A task that is blocked by an open (not Done or Cancelled) task shows a **Blocked** badge on its card, so you can see at a glance what is stuck. \"Related\" is symmetric, and \"blocked by\" is just the inverse of \"blocks\" — the system stores one canonical direction and shows you the right label from each task's point of view."
      },
      {
        "type": "h3",
        "text": "Deleting a task"
      },
      {
        "type": "p",
        "text": "Deleting a task removes it permanently (it is recorded in the activity log by identifier). Unlike projects, task deletion is not a recoverable soft-delete, so delete only when you are sure. To drop a task without losing the record, set it to **Cancelled** instead."
      },
      {
        "type": "h2",
        "text": "The board view"
      },
      {
        "type": "p",
        "text": "The Board tab lays tasks out as Kanban columns, one per status, in workflow order. A **progress bar** at the top shows the project's completion percentage and completed/total count. Across the top you also get a **Filter** box (matches title or identifier), **status** and **assignee** filters, a **Group by** control, and **Display options**."
      },
      {
        "type": "h3",
        "text": "Swimlanes (Group by)"
      },
      {
        "type": "p",
        "text": "You can group the board into swimlanes by **Assignee** or **Priority** (or None for a flat board). With swimlanes on, each person or priority gets its own row of columns, with counts, and you can collapse and expand lanes (press `t` to collapse or expand all)."
      },
      {
        "type": "h3",
        "text": "Display options"
      },
      {
        "type": "p",
        "text": "Display options let you control what each card shows — identifier, priority, assignee, labels, due date, sub-task progress, blocked/severity badges — and whether to show empty status columns. These are per-surface preferences."
      },
      {
        "type": "h3",
        "text": "Keyboard and quick create"
      },
      {
        "type": "p",
        "text": "Press `c` to create a task, `f` to jump to the filter, `t` to toggle swimlanes, and `Cmd/Ctrl+B` to flip between board and list. Each board column also has an inline composer so you can add work without leaving the board."
      },
      {
        "type": "h2",
        "text": "The list (Tasks) view"
      },
      {
        "type": "p",
        "text": "The Tasks tab is a dense table of the same tasks, with sortable-feeling columns for Task, Status, Priority, Assignee, Labels, Due, Progress, and Updated. You choose which columns appear via Display options, and a **density** toggle switches between comfortable and compact rows. The same Filter, status, and assignee controls apply, and a counter shows \"X of Y\" when a filter is active. **Double-click a row** to open the task; single-click and Shift/Cmd-click select rows for bulk actions."
      },
      {
        "type": "h2",
        "text": "Saved views and filters"
      },
      {
        "type": "p",
        "text": "Once you have dialed in a useful combination of filter text, status filter, assignee filter, grouping, and density, you can **save it as a view** so you can return to it in one click. Saved views live per project and per surface (the board has its own set, the list has its own)."
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Set up the filters you want",
            "text": "Adjust the search, status, assignee, and grouping/density until the board or list shows exactly the slice you care about."
          },
          {
            "title": "Save the view",
            "text": "In the Views bar, click Save view (or Save current as view…), give it a name, and confirm. It appears as a pill you can click to re-apply."
          },
          {
            "title": "Make one your default",
            "text": "Pin a view as the default (the star) so it loads automatically when you open the project. You can clear the default at any time."
          },
          {
            "title": "Update, rename, or delete",
            "text": "When you tweak an active view, a dot marks it as having unsaved changes — choose Update to overwrite it. You can also rename or delete views from the Views menu."
          }
        ]
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "Where saved views are stored",
        "text": "These board and list views are saved in your browser, so they are personal to you on that device. A separate, org-level views capability also exists in the platform with personal-vs-team scopes and a shared default, where team views can be managed by admins."
      },
      {
        "type": "h2",
        "text": "Task detail"
      },
      {
        "type": "p",
        "text": "Opening a task brings up a full detail panel. The left side holds the **title** and **description** (rich, autosaving on blur); the right rail holds **Status**, **Priority**, **Assignee**, **Type**, and **Severity** (for bugs). At the top you can **subscribe / unsubscribe** with the bell to control whether the task feeds your inbox. Below the editor you get an **AI context** panel, a **sub-tasks** panel (for top-level tasks), a **relations** panel, and tabs for **Comments** and **Activity**."
      },
      {
        "type": "h3",
        "text": "Comments"
      },
      {
        "type": "p",
        "text": "The Comments tab is the discussion thread on a task. Write a comment and post it; it shows with the author and a relative timestamp. Commenting on a task notifies the assignee, and every comment is recorded in the activity log. You can edit or delete your own comments (admins can moderate others'). The board and list cards also surface the latest comment and a comment count, so active discussions are visible without opening the task."
      },
      {
        "type": "h3",
        "text": "Activity"
      },
      {
        "type": "p",
        "text": "The Activity tab is the full timeline for that task — creation, status changes, assignments, priority changes, comments, and more — so you always have an audit trail of how a task got to where it is."
      },
      {
        "type": "h2",
        "text": "My Tasks"
      },
      {
        "type": "p",
        "text": "My Tasks (in the sidebar) gathers everything **assigned to you across all your active projects** into one focused list, so you do not have to hop between projects to see your plate. Instead of grouping by raw status, it groups by **focus**, in this order:"
      },
      {
        "type": "ul",
        "items": [
          "**Urgent** — anything you have marked urgent, surfaced first.",
          "**Blocking** — work that is holding up other tasks.",
          "**In progress** — what you are actively working on.",
          "**Up next** — committed but not started.",
          "**Backlog** — captured, not yet committed.",
          "**Done** — completed and cancelled, at the bottom."
        ]
      },
      {
        "type": "p",
        "text": "Within each group, started work floats to the top, then higher priority, then most recently updated. Each row shows the status dot, priority, the `KEY-number` identifier, the title, a context line, the project key badge, and when it was last updated. A summary line tells you how many tasks are assigned across how many projects. Click any task to jump into its project. The platform also exposes related personal slices — tasks you **created**, tasks you are **subscribed to** (watching), and a **recent** activity feed — that power your broader my-work and inbox surfaces."
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "A good daily rhythm",
        "text": "Start in My Tasks to see your focus-ordered plate, work the Urgent and In progress groups first, then drop into each project's Board to move work across columns and unblock anything showing a Blocked badge."
      }
    ],
    "title": "Projects and Tasks",
    "slug": "projects-and-tasks",
    "description": "Create projects with permanent keys, then plan and ship work with Linear-style tasks: KEY-numbered identifiers, statuses and priorities, assignees, labels, due dates, the board and list views, My Tasks, comments, and saved views."
  },
  {
    "blocks": [
      {
        "type": "h2",
        "text": "Meetings"
      },
      {
        "type": "p",
        "text": "Meetings is where every conversation your company has becomes a searchable, source-anchored record. Bring in a transcript and CompanyOS writes the summary, links every line back to the exact moment it came from, turns action items into tasks, answers follow-up questions, and lets you share the result with people outside the workspace. Every AI step runs on your organization's own model key (your OpenAI or Anthropic key), so nothing leaves your control."
      },
      {
        "type": "p",
        "text": "Open **Meetings** from the left sidebar of your workspace. You will land on the meeting list, newest first, with three actions in the top-right: **Ask across meetings**, **New meeting**, and **Import meeting**."
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "What you can see",
        "text": "You see every meeting that is not filed under a specific project, plus meetings filed in projects you belong to. Org admins see all meetings. This keeps project-specific conversations visible only to the people on that project."
      },
      {
        "type": "h2",
        "text": "Getting a meeting into CompanyOS"
      },
      {
        "type": "p",
        "text": "There are two ways to create a meeting: **import** an existing transcript, or start a **blank meeting** and write notes by hand. A meeting can have a transcript, your own notes, or both."
      },
      {
        "type": "h3",
        "text": "Import a meeting (the main path)"
      },
      {
        "type": "p",
        "text": "Click **Import meeting** to open the importer. It has three tabs, so you can use whatever you already have on hand:"
      },
      {
        "type": "table",
        "headers": [
          "Source",
          "What it accepts",
          "What happens"
        ],
        "rows": [
          [
            "Paste transcript",
            "Plain text where lines look like `Alex: let us ship it`",
            "Each `Name: text` line becomes a speaker-attributed segment. Lines without a speaker are kept verbatim under an \"Unknown\" speaker. The whole paste is also saved as your notes."
          ],
          [
            "Folio JSON",
            "The raw export from the [Folio](https://folio.chele.bi) recorder",
            "The JSON is validated in the browser before upload. Title, start time, attendees, and timestamped segments are imported exactly as recorded."
          ],
          [
            "Upload file",
            "A `.txt`, `.md`, `.vtt`, or `.srt` transcript, or a `.json` Folio export",
            "Text files are parsed into speaker segments like a paste. A `.json` file is treated as a Folio export, and the title comes from the file."
          ]
        ]
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open the importer",
            "text": "Click Import meeting on the Meetings page (or from the empty state if you have no meetings yet)."
          },
          {
            "title": "Pick your source",
            "text": "Choose Paste transcript, Folio JSON, or Upload file depending on what you have."
          },
          {
            "title": "Add a title",
            "text": "For pasted or uploaded text transcripts, give the meeting a title such as \"Weekly sync\". Folio JSON carries its own title."
          },
          {
            "title": "Import",
            "text": "Click Import meeting. CompanyOS creates the meeting and its transcript segments together, then opens it."
          }
        ]
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "What \"recording\" means here",
        "text": "CompanyOS does not record audio itself. It is the home for transcripts produced by a recorder (like [Folio](https://folio.chele.bi)) or any tool that exports text. Record or transcribe wherever you normally do, then import the result. The Paste transcript tab is the fastest path when you already have text."
      },
      {
        "type": "h3",
        "text": "Start a blank meeting"
      },
      {
        "type": "p",
        "text": "Click **New meeting**, give it a title (\"Standup\", \"Customer call\", \"1:1\"), and press **Create meeting**. This opens an empty meeting with no transcript required. Use it for a live or ad-hoc session and type your own notes as you go. You can summarize and chat once there is something to work with (a transcript or your notes)."
      },
      {
        "type": "h2",
        "text": "The meeting detail page"
      },
      {
        "type": "p",
        "text": "Opening a meeting shows its title, source badge (Folio or Manual), date, and duration. From here you work in two views: the **Document** tab and the **Transcript** tab. There is also a **Split view** button that puts the document and transcript side by side, and an **Ask** panel that stays docked on the right."
      },
      {
        "type": "h3",
        "text": "Filing the meeting into a project"
      },
      {
        "type": "p",
        "text": "If a meeting is not filed under a project yet, a suggestion banner appears at the top. CompanyOS proposes the project it thinks the meeting belongs to, and you can file it with one click or pick a different active project. Filing matters: it controls who can see the meeting, and it is required before you can turn action items into tasks (tasks live inside projects). You can dismiss the banner if the meeting is meant to stay org-wide."
      },
      {
        "type": "h3",
        "text": "The Document tab: AI summary"
      },
      {
        "type": "p",
        "text": "The Document tab is the readable version of the meeting. Click **Summarize** (or pick a template first, then Summarize) and CompanyOS reads the transcript on your org's AI key and produces a structured summary. The result is grouped into sections, each with a clear label and count:"
      },
      {
        "type": "ul",
        "items": [
          "**Decisions** — what was decided.",
          "**Action items** — what someone needs to do, each carrying an \"Action item\" badge.",
          "**Open questions** — what was raised but not resolved.",
          "**Key points** — the rest of the highlights."
        ]
      },
      {
        "type": "p",
        "text": "Every AI line is shown in dimmed text so you can tell at a glance what the model wrote versus what you wrote. Each line carries a small source marker. Hover it and you see the speaker, the timestamp, and the exact transcript quote behind that line. Click it to jump straight to that moment in the Transcript tab. The header tells you how many lines are linked to the transcript (for example \"7 of 9 lines linked to transcript\"), and a line with no clear source shows a \"verify manually\" marker instead of a fake citation."
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "Why the source links matter",
        "text": "The summarizer is built so an AI line never points at a source that is not actually in the transcript. If the model cites a passage that does not exist, that citation is dropped. So a link you can click is a link you can trust, and an unlinked line is honestly flagged as something to check yourself."
      },
      {
        "type": "h3",
        "text": "Re-running and refining the summary"
      },
      {
        "type": "ul",
        "items": [
          "**Re-enhance** — regenerate the AI summary from the transcript, optionally under a different template. Your own edited notes are preserved.",
          "**Edit as your notes** — copy the AI summary down into your notes so you can edit it. Once you edit it, it reads as your own words, marked \"Edited by you\", and is no longer treated as raw AI output.",
          "**Your notes** — the bottom block is always yours to write. Click Edit to add or change notes. Notes are source material, not AI-generated, and a blank meeting can be built entirely from notes."
        ]
      },
      {
        "type": "h3",
        "text": "Turning action items into tasks"
      },
      {
        "type": "p",
        "text": "This is how a meeting stops being a document and starts driving work. Action items in the summary each get a **Task** button, and the section header has a **Create all tasks** button. Filing a single action item creates one task; Create all tasks creates one task per action item. Each task is created in the project's backlog with no priority, and it remembers which meeting it came from."
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Make sure the meeting has a project",
            "text": "Tasks live in projects. If the meeting is filed in a project, tasks go there automatically. If it is not, a \"File tasks in\" picker appears so you can choose a destination project for this session."
          },
          {
            "title": "Create one task, or all of them",
            "text": "Hover an action item and click Task to file just that one, or click Create all tasks in the Action items header to file every action item at once."
          },
          {
            "title": "Track it like any other task",
            "text": "The new tasks appear in that project's backlog, linked back to this meeting so you always know where the work came from."
          }
        ]
      },
      {
        "type": "callout",
        "variant": "warning",
        "title": "No project, no tasks",
        "text": "If the meeting has no project and you have not picked one, the Task buttons stay disabled with a tooltip telling you to set a project first. File the meeting (or pick a project in the \"File tasks in\" menu) to enable them."
      },
      {
        "type": "h3",
        "text": "The Transcript tab"
      },
      {
        "type": "p",
        "text": "The Transcript tab is the verbatim record: every segment with its speaker, timestamp, and text. This is the ground truth that AI summary lines and chat citations link into, so you can always check a claim against what was actually said. For longer meetings it loads in pages of 80 segments with a Show more button, and a left-hand **chapters** rail appears for longer transcripts: 2 to 8 auto-generated topic jump points, each labelled and timestamped, that you can click to jump down the transcript. The active chapter highlights as you scroll. When you click a source link from a summary line or a chat citation, the transcript scrolls to that exact segment and highlights it."
      },
      {
        "type": "h3",
        "text": "Split view"
      },
      {
        "type": "p",
        "text": "On a wide screen, click **Split view** to show the document and transcript at the same time, so you can read the summary on one side and verify against the raw transcript on the other without switching tabs."
      },
      {
        "type": "h2",
        "text": "Meeting templates"
      },
      {
        "type": "p",
        "text": "Templates shape how the AI organizes a summary. Pick a template from the dropdown next to the Summarize button before you generate, and the summary is structured around that template's sections, in order. There are built-in templates for the common meeting shapes, and admins can create custom ones."
      },
      {
        "type": "table",
        "headers": [
          "Built-in template",
          "Sections it organizes the summary into"
        ],
        "rows": [
          [
            "Freeform",
            "No fixed sections. The AI chooses the most natural structure (the default)."
          ],
          [
            "One-on-One",
            "Wins, Blockers, Feedback, Action items"
          ],
          [
            "Stand-up",
            "Yesterday, Today, Blockers"
          ],
          [
            "Customer Call",
            "Context, Pain points, Requests, Next steps"
          ],
          [
            "Decision Meeting",
            "Options considered, Decision, Rationale, Owners"
          ],
          [
            "Retrospective",
            "What went well, What didn't, Action items"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Custom templates (admins)"
      },
      {
        "type": "p",
        "text": "Org admins can create custom templates with their own named sections and an optional extra instruction (a \"prompt scaffold\") that gets passed to the AI on top of the section list. A custom template might define sections like \"Risks, Mitigations, Owners\" plus an instruction such as \"Flag anything that needs legal review.\" Once saved, a custom template appears in the same template dropdown for everyone in the org. Admins can rename, re-section, or delete custom templates; the built-in templates are always available and cannot be removed."
      },
      {
        "type": "h2",
        "text": "Ask about a meeting"
      },
      {
        "type": "p",
        "text": "Every meeting has an **Ask** panel docked to the right (focus it instantly with Cmd/Ctrl+J). Ask anything about what was discussed, decided, or assigned, and the AI answers strictly from the transcript, on your org's key. Answers are ephemeral, they are not saved into the meeting document, and they are designed to stay grounded."
      },
      {
        "type": "ul",
        "items": [
          "**Preset prompts** — one-click starters like \"What did I miss?\", \"Summarize the last 5 minutes\", \"List decisions made\", and \"Suggest questions for me to ask\".",
          "**Inline citations** — when an answer is grounded, it shows numbered source chips. Hover one to see the quote and timestamp, click it to jump to that segment in the transcript.",
          "**Honesty signal** — if the answer reads as low confidence (for example \"that was not discussed\"), it is flagged with a warning so you know to verify directly. Grounded answers carry a quieter \"check the transcript to verify\" note.",
          "**Action lines to tasks** — if the AI's answer lists an action item that matches one in the summary, a Task button appears on that line so you can file it on the spot."
        ]
      },
      {
        "type": "h3",
        "text": "Recipes: saved prompts you reuse"
      },
      {
        "type": "p",
        "text": "Type `/` in the Ask box to open the **recipes** menu. Recipes are saved instructions you run against a meeting in one click. CompanyOS ships several built-in recipes:"
      },
      {
        "type": "ul",
        "items": [
          "**Create tasks from action items** — extract every action item as a discrete task with an owner.",
          "**Draft Slack summary** — write a concise, Slack-ready recap with the key decisions.",
          "**Write follow-up email to attendees** — draft a recap email covering outcomes and next steps.",
          "**Extract decisions for the project log** — list every decision, one per line."
        ]
      },
      {
        "type": "p",
        "text": "To save your own recipe, type `/` followed by the instruction you want to keep, and choose \"Save … as a recipe\". It is then available from the `/` menu on every meeting in the org. Running a recipe is grounded in the transcript just like a normal question, so it will not invent facts the meeting does not contain."
      },
      {
        "type": "h2",
        "text": "Ask across all meetings"
      },
      {
        "type": "p",
        "text": "The single-meeting Ask panel answers about one conversation. **Ask across meetings** (top-right of the Meetings list) answers about the whole archive. Use it for questions like \"What did we decide about the API redesign this quarter?\" CompanyOS finds the most relevant meetings, pulls the best-matching passages, and answers from those excerpts only."
      },
      {
        "type": "ul",
        "items": [
          "**Citations** — every answer lists the meetings and moments it drew from, as links you can open.",
          "**Coverage** — it tells you how many meetings it consulted out of how many it scanned, so you know how broad the answer is.",
          "**Scope filters** — narrow the search to a single project, or to a date range (From / To), before you ask.",
          "**Respects visibility** — it only ever searches meetings you are allowed to see."
        ]
      },
      {
        "type": "h2",
        "text": "Shareable meeting links with tiered guest access"
      },
      {
        "type": "p",
        "text": "You can share a meeting with people who are not in your workspace, with no login required, and you control exactly how much they see. This is what \"tiered guest access\" means: guests always get the summary, but the raw transcript is a separate, opt-in tier."
      },
      {
        "type": "h3",
        "text": "What a guest sees"
      },
      {
        "type": "table",
        "headers": [
          "Tier",
          "Always shared",
          "Shared only if you opt in"
        ],
        "rows": [
          [
            "Summary tier (default)",
            "The AI summary, the action items, and the decisions",
            "—"
          ],
          [
            "Transcript tier (toggle on)",
            "Everything above",
            "The full verbatim transcript with speakers and timestamps"
          ]
        ]
      },
      {
        "type": "p",
        "text": "On top of that, guests get a built-in **Ask about this meeting** box on the shared page. They can ask the AI follow-up questions, and the answer runs on your organization's key. Crucially, a guest's AI access is scoped to what you shared: if you did not include the transcript, the guest's chat is grounded only on the summary, and the answer carries the same grounding signal you see internally. Guests can never reach beyond this one meeting."
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open the share dialog",
            "text": "On the meeting detail page, click Share. Only the meeting's creator or an org admin can create or change a share link."
          },
          {
            "title": "Choose the transcript tier",
            "text": "Decide whether to include the transcript. Leave it off to share only the summary, action items, and decisions. Turn it on to also let guests read the verbatim record."
          },
          {
            "title": "Create and copy the link",
            "text": "Click Create share link, then copy the generated URL and send it to anyone."
          },
          {
            "title": "Adjust or revoke later",
            "text": "Reopen the dialog any time to flip the Include transcript toggle, or click Revoke link to disable guest access. Revoking takes effect immediately and the link stops working."
          }
        ]
      },
      {
        "type": "callout",
        "variant": "warning",
        "title": "Revoke kills access instantly",
        "text": "A revoked link returns a clear \"this link is no longer available\" message to anyone who opens it, and the guest Ask box stops answering. Revoking does not delete the meeting, so you can re-share later if you change your mind."
      },
      {
        "type": "h2",
        "text": "Push a meeting summary to Slack with an embedded Ask link"
      },
      {
        "type": "p",
        "text": "Instead of copy-pasting a recap into Slack, post it directly from CompanyOS. Click **Send to Slack** on the meeting detail page, pick a channel, and CompanyOS posts a tidy message: the meeting title, the latest summary, the action items as a bulleted list, and a link your teammates can click to ask the AI about the meeting."
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Connect Slack once (admin)",
            "text": "Slack must be connected for your org. If it is not, the Send to Slack dialog shows a Connect Slack button that takes an admin to Settings to authorize the workspace. This is a one-time setup."
          },
          {
            "title": "Open Send to Slack",
            "text": "On the meeting, click Send to Slack. CompanyOS lists the channels the bot can post to."
          },
          {
            "title": "Pick a channel and post",
            "text": "Choose a channel and click Post summary. The message is delivered to that channel."
          }
        ]
      },
      {
        "type": "p",
        "text": "The **embedded Ask link** in the Slack message points to the meeting's share page, so teammates who click it land on a page where they can ask the AI about the meeting under the same tiered access you set up. The link is included only when the meeting has an active (non-revoked) share. So the recommended flow is: create the share link with the access tier you want, then push to Slack, and everyone in the channel gets a one-click way to dig into the meeting."
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "Put the Ask link to work",
        "text": "Because the Slack summary embeds the share link, you do not have to answer the inevitable \"wait, what did we decide about X?\" replies yourself. Point people at the link and let them ask the meeting directly, grounded in exactly the content you chose to share."
      },
      {
        "type": "h2",
        "text": "Everything is logged"
      },
      {
        "type": "p",
        "text": "Meeting actions are recorded in your org's activity log: created, imported, updated, summarized, recipe runs, shared, share revoked, and posted to Slack. So you always have a trail of how a meeting was used and who used it."
      }
    ],
    "description": "How to use Meetings in CompanyOS: import or record transcripts, AI summaries with source links, action items into tasks, templates, Ask, shareable links with tiered guest access, and Slack push",
    "slug": "meetings",
    "title": "Meetings"
  },
  {
    "blocks": [
      {
        "type": "h2",
        "text": "Notes, Activity, Calendar & Inbox"
      },
      {
        "type": "p",
        "text": "Four surfaces that keep the work and the context together. **Notes** are where you write things down: decisions, specs, plans, meeting follow-ups. The **Activity** feed is the live record of everything that changed across the org. The **Calendar** holds team and personal events, with an AI pre-meeting brief drawn from your own data. The **Inbox** is your triage queue: assignments, mentions, and closed loops that need you. They are designed to flow into one another, so you can drag a moment out of the activity feed straight into a note, or jump from a notification into the exact item that needs your attention."
      },
      {
        "type": "h2",
        "text": "Notes"
      },
      {
        "type": "p",
        "text": "Notes are shared, organization-wide writing. Every note belongs to the org, so the whole team can find it later, and any note can optionally be attached to a project. A note has a **title** and a **body**, and the body is full rich text. You reach notes from the **Notes** page in the sidebar."
      },
      {
        "type": "h3",
        "text": "What a note is"
      },
      {
        "type": "ul",
        "items": [
          "**Title** — up to 500 characters, required. This is what shows in lists and search.",
          "**Body** — rich-text content with no length limit. Written in a block editor and stored as Markdown under the hood, so it stays portable and diff-friendly.",
          "**Project** — optional. Link a note to a project to keep launch checklists, specs, and decisions grouped with the work they belong to. A project-scoped note shows up both on the Notes page and on that project.",
          "**Mentions** — you can name org members in a note. Each person you mention gets an in-app notification that they were named (you never notify yourself).",
          "**Authorship and timing** — every note tracks who created it, who last updated it, and when. The Notes list is always sorted by most recently updated, so the things you are actively working on float to the top."
        ]
      },
      {
        "type": "h3",
        "text": "Create a note"
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open Notes",
            "text": "Go to the Notes page from the sidebar. You will see every note in the org, newest-updated first, each with a one-line excerpt pulled from the first real line of the body."
          },
          {
            "title": "Click New note",
            "text": "A small dialog asks for a title (for example, \"Q3 launch checklist\"). The Create button stays disabled until you type something."
          },
          {
            "title": "Start writing",
            "text": "On create, you are taken straight into the note's editor with the title pre-filled and the cursor ready. There is nothing else to fill in first."
          }
        ]
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "Create a note inside a project",
        "text": "When you start a note from a project, it is automatically linked to that project. You do not have to set the project field yourself. The note then appears in the project's notes as well as on the main Notes page."
      },
      {
        "type": "h3",
        "text": "The rich-text editor"
      },
      {
        "type": "p",
        "text": "The note editor is a real block editor, not a plain text box. It supports headings (four levels), bold and italic, ordered and unordered lists, checklists, block quotes, inline code, code blocks, horizontal dividers, and links. You can write the way you would in any modern document tool, and everything is saved as clean Markdown."
      },
      {
        "type": "p",
        "text": "Two ways to format as you type:"
      },
      {
        "type": "ul",
        "items": [
          "**Markdown shortcuts** — type `## ` for a heading, `- ` for a bullet, `> ` for a quote, and so on. The editor converts them as you go. Pasting Markdown or links also works; URLs auto-link.",
          "**Slash menu** — type `/` on an empty line to open a block menu. Search by name (\"head\", \"todo\", \"code\") and pick from Text, Heading 1-3, Bullet list, Numbered list, Task list, Quote, Code block, and Divider. Arrow keys move the selection, Enter inserts, Escape closes."
        ]
      },
      {
        "type": "h3",
        "text": "Mentions"
      },
      {
        "type": "p",
        "text": "Type `@` to mention a person, or to reference a task by its key. A picker appears as you type; choose someone and they are inserted as a styled chip in the note. People you mention are notified that they were named in the note."
      },
      {
        "type": "h3",
        "text": "Turn writing into tasks"
      },
      {
        "type": "p",
        "text": "Notes are often where work gets discovered, so the editor lets you convert prose directly into tasks without leaving the page."
      },
      {
        "type": "ul",
        "items": [
          "**One line into a task** — type `/` and pick **Create task**. The current line becomes a task and is removed from the note.",
          "**A selection into many tasks** — highlight several lines, and a **Create task / Create N tasks** button appears at the top of the editor. Each non-empty line (list markers and checkbox brackets stripped) becomes its own task draft."
        ]
      },
      {
        "type": "h3",
        "text": "Saving, preview, and delete"
      },
      {
        "type": "p",
        "text": "There is no Save button. The editor **autosaves** about a second after you stop typing, and again if you navigate away with unsaved changes. A small dot at the top of the note tells you the state: amber and \"Saving…\" while a save is in flight, green and \"Saved <time ago>\" once it lands. An empty title is never saved, so a note always keeps a real title."
      },
      {
        "type": "ul",
        "items": [
          "**Preview** — toggle the eye icon to render the note as it will read, then the pencil icon to go back to editing.",
          "**Delete** — the trash icon removes the note and returns you to the Notes list. Deletion is recorded in the activity feed."
        ]
      },
      {
        "type": "h3",
        "text": "Find and organize notes"
      },
      {
        "type": "p",
        "text": "The Notes page lists everything in the org, sorted by most recently updated, each row showing the title, an auto-generated excerpt, and when it was last touched. You can narrow the list two ways:"
      },
      {
        "type": "ul",
        "items": [
          "**Search** — match against both title and body text. Useful for finding that one decision buried in a long note.",
          "**By project** — viewing notes inside a project shows only that project's notes."
        ]
      },
      {
        "type": "h2",
        "text": "Compose notes from the activity feed (drag and drop)"
      },
      {
        "type": "p",
        "text": "This is the bridge between Activity and Notes. When something happens in the feed — a meeting summary, a decision, a note, a task — you can drag that item straight into a note's editor and it lands as a clickable citation. It is the fastest way to assemble a recap, a decision log, or a follow-up doc from things that already happened."
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open the activity feed",
            "text": "Go to the Activity page (or any feed that shows activity rows). Each row representing a meeting, note, task, or decision is draggable."
          },
          {
            "title": "Open a note in another view",
            "text": "Have the target note open in its editor. You are dragging from the feed into the note body."
          },
          {
            "title": "Drag the activity item into the note",
            "text": "Grab the row and drop it where you want it in the note. CompanyOS carries a structured reference for that item, not just plain text."
          },
          {
            "title": "It lands as a linked citation",
            "text": "At the drop point, the editor inserts the item's title as a link back to the original (the meeting, the note, the task). Keep writing around it. The note now references the real source, so anyone reading later can click straight through."
          }
        ]
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "What carries over",
        "text": "Dragging carries the item's kind, id, title, and a link back to it. Meetings and notes resolve to a real in-app link; tasks and decisions drop in as a labeled reference. The citation is inserted exactly where you drop it, using the cursor position under your pointer."
      },
      {
        "type": "h2",
        "text": "Activity feed"
      },
      {
        "type": "p",
        "text": "The Activity feed is the org's running history — an append-only log of every meaningful change. Whenever someone creates or edits a note, moves a task, runs a meeting summary, adds a member, schedules an event, or records a decision, an activity event is written. The feed turns that raw stream into something readable and live."
      },
      {
        "type": "h3",
        "text": "What the feed shows"
      },
      {
        "type": "p",
        "text": "Each entry tells you who did what, to which item, and when. Events are grouped by day (Today, Yesterday, weekday names within the last week, then dated headers further back), newest first, with a count per day. Times are relative (\"5m\", \"2h\") with the exact timestamp on hover."
      },
      {
        "type": "p",
        "text": "The feed is opinionated about signal so it does not become noise:"
      },
      {
        "type": "ul",
        "items": [
          "**High-signal moments get room to breathe.** Decisions, blockers, approvals, comments, new notes, and new members render as richer cards with a headline and an excerpt, plus an \"Open\" link to jump to the source.",
          "**Routine churn collapses.** A run of three or more similar low-signal events (a flurry of edits, status changes) folds into a single expandable line — \"3 people updated 5 times\" — that you can open to see each one.",
          "**Everything is color-coded by type.** Created, Updated, Status, Assigned, Comment, Note, Decision, Action item, Blocker, Approval, Member, and more each have their own tag and icon, so you can scan the day at a glance."
        ]
      },
      {
        "type": "h3",
        "text": "Real-time updates"
      },
      {
        "type": "p",
        "text": "The feed is live. CompanyOS holds an open stream to the server, and the instant any activity is recorded anywhere in the org, the relevant views refresh on their own — no reload, no polling. Because the stream also knows what kind of thing changed, it refreshes the matching area too: a new note nudges your notes list, a task change nudges your tasks, and so on. You can leave the Activity page open as a true ambient view of the org."
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "\"Since your last visit\"",
        "text": "The feed remembers when you last looked. When you return, the page header tells you how many updates landed while you were away, and a \"Since your last visit\" divider marks exactly where the new activity begins. This is per-browser, so it tracks your own reading, not the team's."
      },
      {
        "type": "h3",
        "text": "Jumping from the feed"
      },
      {
        "type": "p",
        "text": "Activity rows for projects, notes, and meetings link straight to the item. Click the row, or the \"Open\" link on a richer card, to go to the source. And as covered above, draggable rows can be dropped into a note to compose from them."
      },
      {
        "type": "h2",
        "text": "Calendar and events"
      },
      {
        "type": "p",
        "text": "The Calendar puts team and personal events in one month grid so nothing slips through the week. You reach it from the sidebar. Move between months with the arrows, jump back with **Today**, and filter the view with the **All / Team / Personal** tabs."
      },
      {
        "type": "h3",
        "text": "Team events vs. personal events"
      },
      {
        "type": "table",
        "headers": [
          "",
          "Team event",
          "Personal event"
        ],
        "rows": [
          [
            "Who sees it",
            "Every member of the org",
            "Only you"
          ],
          [
            "Color",
            "Accent dot and tint",
            "Muted grey dot and tint"
          ],
          [
            "Who can edit it",
            "The creator, or an org admin",
            "Only you, the owner"
          ],
          [
            "Use it for",
            "Sprint reviews, all-hands, shared deadlines",
            "Focus blocks, reminders, anything private"
          ]
        ]
      },
      {
        "type": "p",
        "text": "Both kinds show in your calendar together, so your week is complete in one view. Other people's personal events are never visible to you — the Calendar simply does not return them."
      },
      {
        "type": "h3",
        "text": "Create and edit an event"
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Start a new event",
            "text": "Click New event in the header, or click the date number on any day cell to seed that date. A dialog opens."
          },
          {
            "title": "Fill in the details",
            "text": "Give it a title (required). Choose Team or Personal visibility. Pick a date. Set start and end times, or flip the All day switch to skip times. Optionally add a location (a room, or a link) and a description."
          },
          {
            "title": "Save",
            "text": "Create event adds it to the grid immediately. The form checks that the end is after the start before it lets you save."
          },
          {
            "title": "Edit or delete later",
            "text": "Click any event chip to reopen the dialog with its details filled in. Change anything and Save changes, or Delete to remove it. Editing a team event is limited to its creator or an admin; editing a personal event is limited to you."
          }
        ]
      },
      {
        "type": "h3",
        "text": "Reading the grid"
      },
      {
        "type": "ul",
        "items": [
          "**Today** is highlighted; weekends and days outside the current month are tinted so the month frame reads clearly.",
          "**Event chips** show the start time and title, color-coded by team or personal. Hover (or focus) a chip for a quick popover with the full time range, whether it is team or personal, and the location.",
          "**Busy days** cap at three visible chips; a \"+N\" opener reveals the rest for that day.",
          "**Linked meetings** — an event tied to a meeting shows a small document icon, and its popover offers an \"Open meeting\" link straight to the transcript and summary."
        ]
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "Coming up",
        "text": "Above the grid, a \"Coming up\" card always shows your single next upcoming event with a live countdown (\"in 2h 15m\") that ticks down on its own. Click it to open that event. When nothing is scheduled, it tells you so."
      },
      {
        "type": "h3",
        "text": "AI pre-meeting brief"
      },
      {
        "type": "p",
        "text": "Open a future event and CompanyOS generates a short **pre-meeting brief** — two to three bullets of real context pulled from your own CompanyOS data, each with a clickable source. It is deliberately honest: it only surfaces facts it can actually point to, and if there is nothing relevant, it says so rather than inventing filler."
      },
      {
        "type": "p",
        "text": "The brief draws from:"
      },
      {
        "type": "ul",
        "items": [
          "**Open tasks** assigned to the event's owner (a few of the most recently updated, still-open ones), each labeled with its task key.",
          "**Follow-ups from a linked meeting** — if the event is attached to a meeting, the action items from that meeting's latest summary.",
          "**A related note** — the note whose text most overlaps with the event's title and description."
        ]
      },
      {
        "type": "p",
        "text": "Each bullet links to its source, so you can click straight through to the task, meeting, or note. You can **pin** the brief to keep it visible, or **dismiss** it. When there is genuinely no prior context, the brief reads \"this looks like a fresh start\" instead of padding."
      },
      {
        "type": "h2",
        "text": "Inbox and notifications"
      },
      {
        "type": "p",
        "text": "The Inbox is your personal triage queue. It is scoped to you alone — only your notifications appear, never anyone else's. It collects the things that actually need your attention and is built to be cleared fast, from the keyboard."
      },
      {
        "type": "h3",
        "text": "What lands in your Inbox"
      },
      {
        "type": "table",
        "headers": [
          "Type",
          "When you get it"
        ],
        "rows": [
          [
            "Assigned",
            "A task is assigned to you"
          ],
          [
            "Mention",
            "Someone names you in a note (or other content)"
          ],
          [
            "Comment",
            "Someone comments on something you are following"
          ],
          [
            "Added",
            "You are added to an organization or a project"
          ],
          [
            "Closed the loop",
            "A meeting action item tied to you is completed"
          ],
          [
            "Update",
            "Other noteworthy events"
          ]
        ]
      },
      {
        "type": "p",
        "text": "You are never notified about your own actions. Each notification shows who triggered it, a title, an optional snippet, and a relative time. \"Closed the loop\" notifications are styled green to highlight that something finished, and show which meeting they came from."
      },
      {
        "type": "h3",
        "text": "Triage from the keyboard"
      },
      {
        "type": "p",
        "text": "The Inbox is filterable by **All / Unread / Archived** tabs, and is designed to be worked through without the mouse. Move with j and k, then act on the focused item:"
      },
      {
        "type": "table",
        "headers": [
          "Key",
          "Action"
        ],
        "rows": [
          [
            "j",
            "Move to the next notification"
          ],
          [
            "k",
            "Move to the previous notification"
          ],
          [
            "Enter (↵)",
            "Open the notification's source (and mark it read)"
          ],
          [
            "e",
            "Archive the focused notification"
          ],
          [
            "h",
            "Snooze the focused notification (hides it for about an hour)"
          ],
          [
            "Shift + e",
            "Mark everything read"
          ]
        ]
      },
      {
        "type": "ul",
        "items": [
          "**Open** — Enter, or clicking a row, marks it read and jumps you to the underlying item: the project, meeting, note, or the task in its project board.",
          "**Read vs. unread** — unread items carry a small accent dot and bolder text; the header shows your unread count. There is also a **Mark all read** button.",
          "**Archive** removes it from your active queue but keeps it under the Archived tab.",
          "**Snooze** tucks it away and brings it back later, so a notification you cannot deal with right now reappears when it is more relevant."
        ]
      },
      {
        "type": "h3",
        "text": "The notification bell"
      },
      {
        "type": "p",
        "text": "You do not have to be on the Inbox page to triage. The bell in the top bar shows your unread count (as a number, or \"9+\" when there are many) and opens a compact version of the Inbox in a popover. Every keyboard shortcut works there too, so you can clear a few items and get back to what you were doing. Press g then i anywhere to jump to the full Inbox."
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "Pick where the app opens",
        "text": "From the Inbox header, the \"Open on\" control sets which page CompanyOS lands you on when you enter the org — Projects, Inbox, My Tasks, or Activity. It is your personal preference, remembered in your browser. If triage is the first thing you do each morning, set it to Inbox."
      }
    ],
    "title": "Notes, Activity, Calendar & Inbox",
    "slug": "notes-activity-calendar-inbox",
    "description": "Write rich-text notes and compose them by dragging from the live activity feed, follow the real-time org activity stream, plan team and personal events with an AI pre-meeting brief, and triage your inbox from the keyboard."
  },
  {
    "title": "AI, Brain & Automations",
    "slug": "ai-brain-automations",
    "description": "Run every AI feature on your own model key, ask your company brain for answers, build AI agents with budgets, and automate triage with reusable skills.",
    "blocks": [
      {
        "type": "h2",
        "text": "What this page covers"
      },
      {
        "type": "p",
        "text": "CompanyOS is the coordination layer for your company, and a layer of AI runs through all of it. This page explains four things that fit together: **BYOK** (you connect your own OpenAI or Anthropic key, and every AI feature runs on it), the **Brain and Ask** features (catch-me-up, where-did-we-leave-off, semantic search across meetings, and your open threads), **AI agents** (named assistants that live inside your org with their own model and spending cap), and **triage automations and skills** (reusable rules that label, route, assign, and prioritize work for you)."
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "One rule ties it all together",
        "text": "There is no hidden CompanyOS model and no shared inference bill. Every summary, every answer, every agent runs on the provider key your org connected. You see exactly what was spent, on which model, for which purpose, in the run log."
      },
      {
        "type": "h2",
        "text": "BYOK: bring your own model key"
      },
      {
        "type": "p",
        "text": "Before any AI feature works, an admin connects at least one provider key under **Settings → AI**. CompanyOS supports two providers today: **OpenAI** and **Anthropic**. You paste a key, give it a name, and it becomes available to meeting summaries, the Ask features, and your AI agents."
      },
      {
        "type": "h3",
        "text": "Why BYOK matters"
      },
      {
        "type": "ul",
        "items": [
          "**Your data, your account.** AI calls go straight from CompanyOS to your provider on your key. The model relationship is yours, not resold through a middleman.",
          "**Your cost, fully visible.** You pay your provider directly at their rates. CompanyOS records the tokens of every call so you can see usage, not a bundled markup.",
          "**Your choice of model.** Because the key is yours, you pick the exact model id (for example a fast cheap model for triage and a stronger model for summaries). Agents and meeting tools each name their own model.",
          "**Stored encrypted.** A key is encrypted the moment it is saved. Only the last four characters are ever shown again. The raw secret is write-only and cannot be read back out of CompanyOS, not even by you."
        ]
      },
      {
        "type": "h3",
        "text": "Add a provider key"
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open AI settings",
            "text": "Go to Settings → AI. You will see a Provider keys card. Adding and managing keys is admin-only."
          },
          {
            "title": "Pick the provider",
            "text": "Choose OpenAI or Anthropic from the provider dropdown."
          },
          {
            "title": "Name the key",
            "text": "Give it a recognizable name like \"OpenAI – production\" or \"Anthropic – team\". Names must be unique within your org."
          },
          {
            "title": "Paste the secret",
            "text": "Paste the full API key (for example sk-…). It is masked as a password field and never echoed back."
          },
          {
            "title": "Save",
            "text": "Click Add key. CompanyOS encrypts it, stores only the last four digits for display, and logs the addition to your activity feed."
          }
        ]
      },
      {
        "type": "h3",
        "text": "Defaults, validation, and cleanup"
      },
      {
        "type": "ul",
        "items": [
          "**Default key.** Flip the Default switch on a key to make it the one AI features reach for automatically. You can have one default per provider. When a feature does not name a specific key, CompanyOS uses the org default.",
          "**Optional upstream validation.** A key can be checked against the provider with a free models-list call when it is stored. A 401 means the provider rejected it; a rate-limit response still counts as valid, so a busy account will not be wrongly refused.",
          "**Rename, re-default, delete.** You can rename a key or change which one is default at any time. The secret itself is immutable: to rotate a key, add the new one and delete the old. Deleting is one click and is also logged."
        ]
      },
      {
        "type": "callout",
        "variant": "warning",
        "title": "No key, no AI",
        "text": "If your org has not connected any provider key, AI features return a clear error: \"No AI provider key configured for this organization.\" Connect a key first and everything downstream lights up."
      },
      {
        "type": "h2",
        "text": "Every AI call is recorded: the run log"
      },
      {
        "type": "p",
        "text": "CompanyOS keeps an honest ledger. Each outbound call to your provider creates an **AI run** with the provider, the exact model used, the purpose (a meeting **summarize** or a **chat** answer), the input and output token counts, and a status of running, succeeded, or failed. Failed runs keep the provider's error message so you can see what went wrong (a bad key, a rate limit, a model that does not exist)."
      },
      {
        "type": "p",
        "text": "Admins can review the full history under the AI run list, newest first. This is your audit trail and your usage view in one place: who is spending tokens, on what model, and whether anything is erroring."
      },
      {
        "type": "table",
        "headers": [
          "Field",
          "What it tells you"
        ],
        "rows": [
          [
            "Provider & model",
            "Which account and which exact model handled the call"
          ],
          [
            "Purpose",
            "Summarize (a meeting summary) or chat (an Ask answer)"
          ],
          [
            "Input / output tokens",
            "What the call consumed, for cost tracking against your provider bill"
          ],
          [
            "Status",
            "Running, succeeded, or failed"
          ],
          [
            "Error",
            "The provider's message when a call fails, kept for debugging"
          ]
        ]
      },
      {
        "type": "h2",
        "text": "Ask: answers grounded in your own meetings"
      },
      {
        "type": "p",
        "text": "The Ask features turn your meeting archive into something you can question in plain language. There are two scopes: ask about one meeting, or ask across all of them. Both run on your BYOK key and both are built to be trustworthy rather than confidently wrong."
      },
      {
        "type": "h3",
        "text": "Ask one meeting"
      },
      {
        "type": "p",
        "text": "Open any meeting and ask a question grounded in that transcript: \"What did we agree the deadline was?\", \"Who owns the migration?\", \"Summarize the objections to the pricing change.\" The answer is drawn only from that meeting's segments, and the call is recorded as a chat run."
      },
      {
        "type": "h3",
        "text": "Ask across meetings"
      },
      {
        "type": "p",
        "text": "From the meetings view, use **Ask across meetings** to query the entire archive at once. This is the closest thing to semantic search over what your company actually said. Type a question like \"What did we decide about the API redesign this quarter?\" and CompanyOS does the retrieval, then answers with the relevant meetings cited inline."
      },
      {
        "type": "p",
        "text": "Under the hood it scans your recent meetings, ranks them by how well their titles and transcript text overlap your question, shortlists the strongest matches, and pulls the best few segments from each. Those excerpts, each tagged with its meeting and segment, are the only material the model is allowed to use. The system prompt is explicit: answer only from the provided excerpts, cite the meetings you draw on, and if the answer is not there, say so plainly instead of guessing."
      },
      {
        "type": "h3",
        "text": "Scope the question"
      },
      {
        "type": "ul",
        "items": [
          "**Project** — narrow the archive to a single project's meetings.",
          "**From / To dates** — limit the answer to a time window, for example just this quarter.",
          "**Pinned meetings** — force specific meetings into the consideration set so they are always weighed."
        ]
      },
      {
        "type": "h3",
        "text": "Citations, coverage, and confidence"
      },
      {
        "type": "p",
        "text": "Every cross-meeting answer comes with numbered **citations** that link straight to the meeting (and the moment in the transcript) the claim came from, so you can verify it yourself. It also shows a **coverage note** — \"consulted N of M\" — telling you how many meetings were relevant out of how many were scanned. From that, CompanyOS derives a conservative **confidence band**: low when nothing relevant was found, high only when several sources agree and they are a majority of what was consulted, and partial in between. Thin evidence never reads as a confident paragraph."
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "Permissions are respected",
        "text": "Cross-meeting Ask only ever draws on meetings you are allowed to see. Unless you are an org admin, retrieval is limited to org-wide meetings plus those in projects you belong to. The AI cannot leak a meeting you could not open yourself."
      },
      {
        "type": "h2",
        "text": "The company brain: catch up without reading everything"
      },
      {
        "type": "p",
        "text": "The Brain is a set of cross-project tools that answer the questions you actually have when you sit down: what changed, where did we leave off, and what is on my plate. They are reachable from AI clients connected to your CompanyOS brain (the MCP server) and they read live from your tasks, notes, and activity feed."
      },
      {
        "type": "h3",
        "text": "Catch me up — what changed"
      },
      {
        "type": "p",
        "text": "Ask for everything that has happened in the org since a point in time, and the brain returns the activity that landed after that moment: tasks created and moved, notes written, meetings imported, and more. This is the \"I was out for three days, what did I miss\" answer, scoped to a timestamp you choose."
      },
      {
        "type": "h3",
        "text": "Where did we leave off"
      },
      {
        "type": "p",
        "text": "Point the brain at a project and it reconstructs the state of play: the in-flight tasks (work actually started), the most recent notes, and the latest activity on that project. It is the fastest way to reload context on something you have not touched in a while, without scrolling a board."
      },
      {
        "type": "h3",
        "text": "Open threads — what's on my plate"
      },
      {
        "type": "p",
        "text": "Ask for your open threads and the brain pulls together the tasks assigned to you, the tasks you created, and your triage queue, filtering out anything already completed or cancelled. It is a single honest snapshot of your outstanding work across every project."
      },
      {
        "type": "table",
        "headers": [
          "You want to know",
          "The brain answers with"
        ],
        "rows": [
          [
            "What did I miss since Friday?",
            "Every change in the org after a timestamp you give"
          ],
          [
            "Where were we on this project?",
            "In-flight tasks, recent notes, and recent activity for that project"
          ],
          [
            "What's on my plate right now?",
            "Your open assigned tasks, tasks you created, and your triage queue"
          ]
        ]
      },
      {
        "type": "h2",
        "text": "AI Access: which apps can read your brain"
      },
      {
        "type": "p",
        "text": "The Brain and Ask tools are exposed to external AI clients (your chat app, your editor, a desktop assistant) through CompanyOS's connection layer. When you connect a client, it asks for specific permissions, and you approve them once. Settings → AI Access lists every connected app and device, the org it is connected to, and exactly which permissions it holds."
      },
      {
        "type": "h3",
        "text": "How permissions are scoped"
      },
      {
        "type": "p",
        "text": "Access is granted in narrow scopes, not all-or-nothing. Read scopes (like reading tasks, notes, meetings, calendar, activity, and the brain's catch-me-up tools) are baseline; write scopes and sensitive ones (like creating or budgeting AI agents) are elevated and granted deliberately. A client only ever gets the intersection of what it asked for and what you allowed."
      },
      {
        "type": "table",
        "headers": [
          "Scope",
          "Lets a connected app"
        ],
        "rows": [
          [
            "brain:read",
            "Use catch-me-up, search, and open threads"
          ],
          [
            "activity:read",
            "See what changed and where you left off"
          ],
          [
            "meetings:read / write",
            "Read transcripts and summaries; create and summarize meetings"
          ],
          [
            "tasks:read / write",
            "Read boards and triage; create, move, and delete tasks"
          ],
          [
            "agents:read",
            "See the org's AI agents and their runs"
          ],
          [
            "agents:write",
            "Create, update, pause, and budget AI agents (elevated)"
          ]
        ]
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open AI Access",
            "text": "Go to Settings → AI Access. Connected apps and devices are listed with their org and a badge for each permission they hold."
          },
          {
            "title": "Review the scopes",
            "text": "Each grant shows its exact permissions as badges, so you can confirm a client only has what it should."
          },
          {
            "title": "Revoke anytime",
            "text": "Click Revoke on any grant to cut a client off immediately. It loses access to your brain the moment you do."
          }
        ]
      },
      {
        "type": "h2",
        "text": "AI agents: assistants that live in your org"
      },
      {
        "type": "p",
        "text": "An AI agent (an \"AI user\") is a named, persistent assistant defined by your org. Unlike a one-off chat, an agent has a stable identity: a name, a provider, a specific model, and a system prompt that fixes its behavior and tone. Think \"Scribe\" who summarizes meetings, or \"Router\" who explains how work should be filed. Agents are managed under Settings → AI and from connected AI clients."
      },
      {
        "type": "h3",
        "text": "Create an agent"
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open AI settings",
            "text": "Settings → AI shows an AI users card. Click New AI user."
          },
          {
            "title": "Name it",
            "text": "Give the agent a clear name like Scribe. Names are unique in your org."
          },
          {
            "title": "Choose provider and model",
            "text": "Pick OpenAI or Anthropic, then type the exact model id you want it to run on (for example gpt-5.2). The agent runs on your org's BYOK key for that provider."
          },
          {
            "title": "Write the system prompt",
            "text": "Describe what the agent does and how it should behave, for example \"You summarize meetings for the team in tight, decision-first bullets.\" This instruction shapes every response."
          },
          {
            "title": "Create",
            "text": "Save it. The agent is active by default and immediately available to your org."
          }
        ]
      },
      {
        "type": "h3",
        "text": "Give an agent a budget"
      },
      {
        "type": "p",
        "text": "Each agent can carry a **monthly spend cap** so an automated assistant can never run away with your provider bill. The cap is set in cents per month — a Paperclip-style guardrail that bounds how much an agent is allowed to cost. Set it when you expect an agent to run on a schedule or react to events, so its spending stays inside a number you chose."
      },
      {
        "type": "h3",
        "text": "Pause, resume, edit, delete"
      },
      {
        "type": "ul",
        "items": [
          "**Pause and resume.** An agent has an active flag. Pause it to stop it from acting without losing its configuration; resume it later and it picks up exactly where it was. Inactive agents are clearly badged.",
          "**Edit.** Change an agent's name, model, or system prompt at any time — for example to move it to a cheaper model or sharpen its instructions.",
          "**Delete.** Remove an agent you no longer need. From connected AI clients, deletion is a two-step confirm so an agent is never wiped by accident."
        ]
      },
      {
        "type": "h3",
        "text": "Their runs"
      },
      {
        "type": "p",
        "text": "Everything an agent does flows through the same run log as the rest of your AI: each call is an AI run with its model, purpose, token counts, and status. So an agent is never a black box — you can always see what it spent and whether it succeeded, and connected clients with the agents:read scope can list the org's agents and their runs."
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "Budgets are an elevated action",
        "text": "Creating, updating, pausing, and budgeting agents all require admin-level permission (the agents:write scope). Read-only visibility into agents and their runs is baseline, so the whole team can see what the org's assistants are doing without being able to change them."
      },
      {
        "type": "h2",
        "text": "Triage automations: stop sorting the same work by hand"
      },
      {
        "type": "p",
        "text": "An automation is a saved rule that applies actions to a task automatically. Instead of dragging every inbound bug into the right project and tagging it, you write the rule once and it runs every time. Automations live under Settings → Automations & skills, and creating or editing them is admin-only."
      },
      {
        "type": "h3",
        "text": "Triggers — when a rule fires"
      },
      {
        "type": "table",
        "headers": [
          "Trigger",
          "Fires when"
        ],
        "rows": [
          [
            "On triage entry",
            "A task lands in the triage queue (unassigned, inbound work)"
          ],
          [
            "On status change",
            "A task moves to a new status on the board"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Actions — what a rule does"
      },
      {
        "type": "table",
        "headers": [
          "Action",
          "Effect on the task"
        ],
        "rows": [
          [
            "Label",
            "Adds a label (by name or id) that exists in your org"
          ],
          [
            "Route",
            "Moves the task into a specific project, renumbering it for that project"
          ],
          [
            "Assign",
            "Sets the assignee to a member of your org"
          ],
          [
            "Set priority",
            "Sets the task's priority to a valid level"
          ]
        ]
      },
      {
        "type": "p",
        "text": "A single rule can chain several actions, so one automation can label, route, and assign in one pass. CompanyOS validates actions when you save the rule — a label that does not exist, a project outside your org, or a non-member assignee is rejected up front, so a rule cannot silently misfire later. Every time a rule runs against a task, the execution is recorded in that task's activity, so you can always see what touched it and why."
      },
      {
        "type": "h3",
        "text": "Build an automation"
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open automations",
            "text": "Go to Settings → Automations & skills and click New automation."
          },
          {
            "title": "Name and trigger",
            "text": "Name the rule (for example \"Route inbound bugs\") and pick its trigger: on triage entry or on status change."
          },
          {
            "title": "Add actions",
            "text": "Add one or more actions — label, route, assign, set priority — and fill in each value. Use Add action to chain more."
          },
          {
            "title": "Save",
            "text": "Save the automation. New enabled rules start running on their trigger immediately."
          },
          {
            "title": "Toggle or remove later",
            "text": "Each rule has an enable switch and a delete button. Disable a rule to pause it without losing it, or delete it when it is no longer needed."
          }
        ]
      },
      {
        "type": "h2",
        "text": "Skills: reusable automations you invoke on demand"
      },
      {
        "type": "p",
        "text": "Sometimes you do not want a rule to fire on every trigger — you want to apply it deliberately, to the one task in front of you. That is a **skill**. A skill is the exact same kind of rule (the same label/route/assign/set-priority actions), but flagged so it does not run on its trigger automatically. Instead it sits ready to be invoked by hand."
      },
      {
        "type": "p",
        "text": "When you are working the **Triage** queue (Settings → Personal → Triage), each item shows a **Skills** menu listing your enabled skills. Pick one and its actions apply to that task instantly, with the run logged to the task's activity just like an automatic rule. It is the fast way to say \"file this the way I always file these\" without dragging through menus."
      },
      {
        "type": "h3",
        "text": "Save a rule as a skill"
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Build the rule",
            "text": "In Settings → Automations & skills, create a rule with the actions you want to reuse."
          },
          {
            "title": "Flip the skill switch",
            "text": "Turn on \"Save as an invocable skill.\" The rule now appears with a Skill badge and stops firing on its trigger."
          },
          {
            "title": "Run it from triage",
            "text": "Open the Triage queue, focus a task, open its Skills menu, and pick the skill. Its actions apply to that task on the spot."
          }
        ]
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "Triage itself is built for speed",
        "text": "The Triage queue processes one item at a time with single-key shortcuts — Accept (1 or A), Duplicate (2), Decline (3 or X), Snooze (S), arrow keys to move, Enter to open. Skills slot right into that flow, so routing and tagging never break your rhythm."
      },
      {
        "type": "h2",
        "text": "How the pieces work together"
      },
      {
        "type": "ul",
        "items": [
          "**BYOK powers everything.** Connect an OpenAI or Anthropic key once, and meeting summaries, Ask, and agents all run on it — on your account, at your cost, with full token visibility.",
          "**The Brain reads your work.** Catch-me-up, where-we-left-off, and open threads pull live from the same tasks, notes, and activity the rest of CompanyOS uses, so answers are always current.",
          "**Ask is honest.** Every cross-meeting answer cites its sources, shows how much it consulted, and downgrades its own confidence when the evidence is thin.",
          "**Agents are bounded.** Named assistants run on your key with a monthly cap, can be paused or edited any time, and log every call they make.",
          "**Automations and skills remove the busywork.** Rules sort triage on autopilot; skills let you apply your filing logic by hand in one keystroke. Both are validated on save and logged on every run."
        ]
      }
    ]
  },
  {
    "title": "The Company-Brain MCP",
    "slug": "company-brain-mcp",
    "description": "Connect Claude Code, Claude Desktop, or any MCP client to securely act on everything in CompanyOS — tasks, projects, meetings, notes, calendar, comments, teams, the org, activity, the brain, and AI agents — with OAuth 2.1, per-org or all-organization tokens, granular scopes, a Root/Admin switch, and full member parity across 130+ tools.",
    "blocks": [
      {
        "type": "h2",
        "text": "What the Company-Brain MCP is"
      },
      {
        "type": "p",
        "text": "The Company-Brain MCP is a first-party [Model Context Protocol](https://modelcontextprotocol.io) server built directly into the CompanyOS API. Connect an MCP client — Claude Code, Claude Desktop, or anything that speaks MCP — and it can read and write everything you can reach in CompanyOS: projects, tasks, boards, comments, notifications, meetings, notes, calendar, teams, the org and its members, activity, the knowledge brain, and the AI agents. Every tool call is scoped to one organization and runs with **your** permissions, so an agent can do exactly what you can do in the web app — nothing more."
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "Endpoint",
        "text": "`https://api.company.chele.bi/api/v1/mcp` — a single streamable-HTTP MCP endpoint. Authentication is OAuth 2.1; there is nothing to copy-paste, the client walks you through a browser consent the first time."
      },
      {
        "type": "h2",
        "text": "How access works"
      },
      {
        "type": "p",
        "text": "The MCP uses standard OAuth 2.1 so you never hand a client a raw API key. The first time a client connects it discovers the authorization server, registers itself, and opens a CompanyOS consent screen in your browser. You pick a workspace and approve a set of permissions; the client receives a token scoped to that org and those permissions."
      },
      {
        "type": "ul",
        "items": [
          "**OAuth 2.1 + Dynamic Client Registration (RFC 7591)** — clients self-register, no manual app setup.",
          "**PKCE (S256)** on the authorization code flow — safe for public/native clients.",
          "**RFC 9728 protected-resource metadata** — clients auto-discover the auth server from the MCP endpoint.",
          "**Per-organization or all-organization tokens** — mint a token for one workspace, or choose *All my organizations* to receive a single cross-org token that works in every workspace you belong to.",
          "**`org_id` targeting** — with an all-organization token, every tool accepts an optional `org_id` so the agent chooses which workspace a call lands in; a single-org token infers it automatically.",
          "**Granular scopes** — you approve exactly which domains the agent may read and write."
        ]
      },
      {
        "type": "h3",
        "text": "The consent screen"
      },
      {
        "type": "p",
        "text": "When a client connects you land on the CompanyOS authorization page. Choose a single **workspace**, or pick **All my organizations** to authorize every workspace you belong to at once with one cross-org token, then tick the **permissions**. Read permissions for the core domains are pre-checked as a sensible baseline; write and elevated permissions are an explicit, deliberate opt-in. Approve to connect, or decline to cancel — either way you are returned to the client."
      },
      {
        "type": "h3",
        "text": "Root / Admin — full access"
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "One switch for trusted agents",
        "text": "At the top of the consent screen is a **Root / Admin** toggle. Turn it on and every permission is selected and locked, granting the agent the complete tool surface on your behalf. Use it when you want an agent to act as a full operator of your workspace; leave it off and hand-pick scopes when you want to keep the agent narrow."
      },
      {
        "type": "h2",
        "text": "Install"
      },
      {
        "type": "h3",
        "text": "Claude Code"
      },
      {
        "type": "p",
        "text": "Add the server, then run `/mcp` and complete the browser consent:"
      },
      {
        "type": "code",
        "lang": "bash",
        "code": "claude mcp add --transport http companyos https://api.company.chele.bi/api/v1/mcp\n\n# then, inside Claude Code:\n/mcp        # opens the CompanyOS consent screen in your browser"
      },
      {
        "type": "h3",
        "text": "Cursor"
      },
      {
        "type": "p",
        "text": "Cursor speaks MCP natively. Add CompanyOS to `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (per-project), then open Cursor Settings → MCP and complete the browser consent on first use:"
      },
      {
        "type": "code",
        "lang": "json",
        "code": "{\n  \"mcpServers\": {\n    \"companyos\": {\n      \"url\": \"https://api.company.chele.bi/api/v1/mcp\"\n    }\n  }\n}"
      },
      {
        "type": "p",
        "text": "Or use the one-click [Add to Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=companyos&config=eyJ1cmwiOiJodHRwczovL2FwaS5jb21wYW55LmNoZWxlLmJpL2FwaS92MS9tY3AifQ%3D%3D) deeplink. The first tool call opens the same CompanyOS OAuth consent in your browser — no API key is stored in the file."
      },
      {
        "type": "h3",
        "text": "Claude Desktop and other clients"
      },
      {
        "type": "p",
        "text": "Point any MCP client at the endpoint. Clients that don't yet speak OAuth-protected HTTP natively can bridge through `mcp-remote`:"
      },
      {
        "type": "code",
        "lang": "json",
        "code": "{\n  \"mcpServers\": {\n    \"companyos\": {\n      \"command\": \"npx\",\n      \"args\": [\"-y\", \"mcp-remote\", \"https://api.company.chele.bi/api/v1/mcp\"]\n    }\n  }\n}"
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "First connection",
        "text": "The first call triggers the OAuth flow and opens the consent screen in your browser. After you approve, the client stores the per-org token and reconnects automatically."
      },
      {
        "type": "h2",
        "text": "Permissions (scopes)"
      },
      {
        "type": "p",
        "text": "Scopes are grouped by domain, with a read tier, a write tier, and a few elevated tiers for sensitive admin actions. Approving a domain's read scope lets the agent see that data; the write scope lets it create, edit, and delete. Root/Admin grants all of them at once."
      },
      {
        "type": "table",
        "headers": [
          "Domain",
          "Scopes",
          "Covers"
        ],
        "rows": [
          [
            "Tasks",
            "`tasks:read`, `tasks:write`",
            "Tasks, boards, sub-tasks, relations, labels, triage, and projects"
          ],
          [
            "Notes",
            "`notes:read`, `notes:write`",
            "Notes and documents"
          ],
          [
            "Meetings",
            "`meetings:read`, `meetings:write`",
            "Meetings, transcripts, summaries, share links, templates and recipes"
          ],
          [
            "Calendar",
            "`events:read`, `events:write`",
            "Calendar events and briefs"
          ],
          [
            "Comments",
            "`comments:read`, `comments:write`",
            "Comments on tasks, notes and meetings"
          ],
          [
            "Notifications",
            "`notifications:read`, `notifications:write`",
            "Your notifications, read/archive/snooze"
          ],
          [
            "Teams",
            "`teams:read`, `teams:write`",
            "Teams and their members"
          ],
          [
            "Organization",
            "`org:read`, `org:manage`, `org:create` (elevated)",
            "Org details, members, roles, invites, and creating new organizations"
          ],
          [
            "All organizations",
            "`orgs:all` (elevated)",
            "Granted by the **All my organizations** consent option — one token that acts across every workspace you belong to"
          ],
          [
            "Views",
            "`views:read`, `views:write`",
            "Saved board views"
          ],
          [
            "Vocabulary",
            "`vocabulary:read`, `vocabulary:write`",
            "The org glossary"
          ],
          [
            "Workflow",
            "`workflow:read`, `workflow:write`",
            "Custom workflow statuses"
          ],
          [
            "Automation",
            "`automation:read`, `automation:write`",
            "Automation rules and skills"
          ],
          [
            "Activity",
            "`activity:read`",
            "The activity feed and per-entity history"
          ],
          [
            "Brain",
            "`brain:read`",
            "Catch-me-up, open threads and resume points"
          ],
          [
            "AI agents",
            "`agents:read`, `agents:write`, `agents:keys` (elevated)",
            "AI users, runs, budgets, and provider API keys"
          ],
          [
            "Integrations",
            "`integrations:read`, `integrations:manage` (elevated)",
            "Slack connection and posting"
          ],
          [
            "Connected sources",
            "`sources:read`, `sources:write`, `sources:manage` (elevated)",
            "GitHub commits and pull requests linked to tasks"
          ],
          [
            "Profile",
            "`profile:read`, `profile:write`",
            "Your own user profile"
          ]
        ]
      },
      {
        "type": "h2",
        "text": "What the agent can do (tool catalog)"
      },
      {
        "type": "p",
        "text": "The MCP exposes the full member surface — every action a person can take in the web app, an agent can take through a tool. Tools are grouped below by domain. Creates accept an optional `idempotency_key` so a retried call never duplicates work, and destructive deletes take a `confirm` flag (call once to preview, again with `confirm=true` to apply)."
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "Targeting an organization",
        "text": "Every tool accepts an optional `org_id`. With a single-organization token you can omit it — the call uses the token's workspace. With an **All my organizations** token, pass `org_id` to choose which workspace a call acts on."
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "Linking to tasks and notes",
        "text": "Embed a clickable reference to a task or note in any description or comment using a Markdown link of the form `[label](/__mention/kind/id)`. See the References & Mentions page for the full format and examples."
      },
      {
        "type": "h3",
        "text": "Tasks and boards"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_project_tasks`",
            "List a project's tasks with board-style filters"
          ],
          [
            "`get_task`",
            "Fetch one task with its identifier, counts and blocked state"
          ],
          [
            "`create_task`",
            "Create a task (supports sub-tasks, bug kind, severity, mentions, relations)"
          ],
          [
            "`update_task`",
            "Edit title, description, priority, assignee, due date, labels, kind, severity"
          ],
          [
            "`transition_task_status`",
            "Move a task to a new workflow status"
          ],
          [
            "`delete_task`",
            "Delete a task (confirm-gated)"
          ],
          [
            "`create_tasks_batch`",
            "Create several tasks at once from a list of titles"
          ],
          [
            "`get_task_board`",
            "Read the board grouped into status columns"
          ],
          [
            "`list_my_tasks`",
            "Your assigned / created / subscribed / recent tasks"
          ],
          [
            "`list_subtasks`",
            "List a task's sub-tasks"
          ],
          [
            "`subscribe_task`, `unsubscribe_task`",
            "Follow or unfollow a task"
          ],
          [
            "`list_task_relations`",
            "List blocking / blocked-by / related links"
          ],
          [
            "`add_task_relation`, `remove_task_relation`",
            "Link or unlink two tasks"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Labels (tags)"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_labels`",
            "List the org's task labels"
          ],
          [
            "`create_label`",
            "Create a label (get-or-create, safe to retry)"
          ],
          [
            "`attach_task_labels`, `detach_task_labels`",
            "Add or remove labels on a task"
          ],
          [
            "`delete_label`",
            "Delete a label org-wide (confirm-gated)"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Triage"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_triage`",
            "Incoming items awaiting routing"
          ],
          [
            "`accept_triage_task`, `decline_triage_task`",
            "Accept or decline a triage item"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Projects"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_projects`, `get_project`, `create_project`",
            "Browse and create projects"
          ],
          [
            "`update_project`",
            "Edit name, description, status, team, lead, target date"
          ],
          [
            "`delete_project`, `restore_project`, `list_deleted_projects`",
            "Archive, restore, and review deleted projects (delete confirm-gated)"
          ],
          [
            "`subscribe_project`, `unsubscribe_project`, `get_project_subscription`",
            "Follow a project and check subscription"
          ],
          [
            "`list_project_members`, `add_project_member`, `remove_project_member`",
            "Manage who is on a project"
          ],
          [
            "`list_project_artifacts`, `add_project_artifact`, `remove_project_artifact`",
            "Attach and remove links/artifacts"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Comments"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_comments`, `get_comment`",
            "Read comments on a task, note or meeting"
          ],
          [
            "`create_comment`, `update_comment`, `delete_comment`",
            "Post, edit and remove comments (delete confirm-gated)"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Notifications"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_notifications`, `unread_count`",
            "Your notifications and unread total"
          ],
          [
            "`mark_notification_read`, `mark_all_notifications_read`",
            "Mark one or all read"
          ],
          [
            "`archive_notification`, `snooze_notification`",
            "Archive or snooze a notification"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Teams"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_teams`, `get_team`, `create_team`, `update_team`, `delete_team`",
            "Manage teams (delete confirm-gated)"
          ],
          [
            "`list_team_members`, `add_team_member`, `remove_team_member`",
            "Manage team membership"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Organization, members and invites"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_my_orgs`",
            "List every organization you belong to (works with an all-organization token)"
          ],
          [
            "`get_org`, `update_org`",
            "Read and edit the workspace"
          ],
          [
            "`create_org`",
            "Create a new organization — you become its owner"
          ],
          [
            "`delete_org`",
            "Delete an organization you own (confirm-gated)"
          ],
          [
            "`list_org_members`, `update_member_role`, `remove_org_member`",
            "Manage members and roles (remove confirm-gated)"
          ],
          [
            "`list_invites`, `create_invite`, `revoke_invite`",
            "Invite people and revoke invitations"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Meetings"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_meetings`, `get_meeting`, `create_meeting`",
            "Browse and create meetings"
          ],
          [
            "`import_folio_meeting`",
            "Import a meeting from [Folio](https://folio.chele.bi)"
          ],
          [
            "`update_meeting`, `delete_meeting`",
            "Edit or delete a meeting (delete confirm-gated)"
          ],
          [
            "`list_meeting_segments`, `list_meeting_chapters`, `list_meeting_summaries`",
            "Read transcript segments, chapters and summaries"
          ],
          [
            "`summarize_meeting`",
            "Generate a summary"
          ],
          [
            "`suggest_meeting_project`",
            "Suggest the project a meeting belongs to"
          ],
          [
            "`ask_meeting`, `meetings_chat`",
            "Q&A on one meeting, or across all meetings"
          ],
          [
            "`run_meeting_recipe`",
            "Run a saved meeting recipe"
          ],
          [
            "`get_meeting_share`, `create_meeting_share`, `update_meeting_share`",
            "Manage public share links"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Meeting templates and recipes"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_meeting_templates`, `create_meeting_template`, `update_meeting_template`, `delete_meeting_template`",
            "Manage meeting templates (delete confirm-gated)"
          ],
          [
            "`list_meeting_recipes`, `create_meeting_recipe`",
            "Browse and create recipes"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Notes"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_notes`, `get_note`",
            "Browse and read notes"
          ],
          [
            "`create_note`, `update_note`, `delete_note`",
            "Write, edit and delete notes (delete confirm-gated)"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Calendar"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_calendar_events`, `get_calendar_event`",
            "Browse and read events"
          ],
          [
            "`create_calendar_event`, `update_calendar_event`, `delete_calendar_event`",
            "Manage events (delete confirm-gated)"
          ],
          [
            "`get_event_brief`",
            "Get the AI brief for an event"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Activity"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_activity`",
            "The org-wide activity feed, newest first"
          ],
          [
            "`get_entity_activity`",
            "The change history of one task, note or meeting"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Company brain"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`brain_open_threads`",
            "Open loops that still need attention"
          ],
          [
            "`brain_changes_since`",
            "What changed since a point in time (catch-me-up)"
          ],
          [
            "`brain_resume`",
            "Where you left off, to resume work"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "AI agents and keys"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_ai_users`, `get_ai_user`, `create_ai_user`, `update_ai_user`",
            "Manage the org's AI agents"
          ],
          [
            "`pause_ai_user`, `set_ai_user_budget`, `delete_ai_user`",
            "Pause, budget and remove agents"
          ],
          [
            "`list_agent_runs`",
            "Recent agent runs"
          ],
          [
            "`list_ai_keys`, `create_ai_key`, `update_ai_key`, `revoke_ai_key`",
            "Manage provider API keys (elevated `agents:keys`; revoke confirm-gated)"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Views, vocabulary and workflow"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_views`, `create_view`, `update_view`, `delete_view`",
            "Saved board views (delete confirm-gated)"
          ],
          [
            "`list_vocabulary`, `create_term`, `update_term`, `delete_term`",
            "Org glossary (delete confirm-gated)"
          ],
          [
            "`list_workflow_statuses`, `create_workflow_status`, `update_workflow_status`, `delete_workflow_status`",
            "Custom statuses (delete confirm-gated)"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Automation"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`list_automations`, `create_automation`, `update_automation`, `delete_automation`",
            "Manage automation rules (delete confirm-gated)"
          ],
          [
            "`run_automation`",
            "Run a skill rule against a task"
          ]
        ]
      },
      {
        "type": "h3",
        "text": "Integrations and profile"
      },
      {
        "type": "table",
        "headers": [
          "Tool",
          "What it does"
        ],
        "rows": [
          [
            "`get_slack_integration`, `list_slack_channels`",
            "Read the Slack connection and channels"
          ],
          [
            "`post_meeting_to_slack`",
            "Post a meeting to a Slack channel (elevated `integrations:manage`)"
          ],
          [
            "`get_my_profile`, `update_my_profile`",
            "Read and update your own profile"
          ]
        ]
      },
      {
        "type": "h2",
        "text": "Safety and conventions"
      },
      {
        "type": "ul",
        "items": [
          "**Org-scoped** — every token is pinned to one organization; tools only ever touch that workspace.",
          "**Scope-checked per call** — a tool runs only if your token carries its scope, otherwise it returns `insufficient_scope`.",
          "**Idempotent creates** — pass an `idempotency_key` and a retried create returns the original result instead of duplicating.",
          "**Confirm-gated deletes** — destructive tools preview first and only act when called again with `confirm=true`.",
          "**Mirrors the app** — every action is exactly what a member can do in the UI, and shows up in activity the same way."
        ]
      },
      {
        "type": "callout",
        "variant": "warning",
        "title": "New permissions need a fresh consent",
        "text": "If you connected before a new tool domain shipped, your existing token won't carry the new scopes. Re-run the client's connect flow (`/mcp` in Claude Code) and approve again — ticking Root/Admin grants the entire current surface in one step."
      }
    ]
  },
  {
    "title": "Set up your agent",
    "slug": "agent-project-setup",
    "description": "Wire any project so your AI agent (Claude Code, Cursor, Claude Desktop) reliably uses the CompanyOS company brain for project search and save — a one-command, project-scoped, opt-in setup, plus the manual equivalents.",
    "blocks": [
      {
        "type": "h2",
        "text": "Set up your agent for a project"
      },
      {
        "type": "p",
        "text": "CompanyOS plugs into your AI coding agent — Claude Code and any MCP client — so it reaches for the company brain whenever it searches for or saves project information. Setup is **per project and opt-in**: you only wire the projects where you want it, and your other work is untouched."
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "Project-scoped",
        "text": "Everything here lives inside the project directory (`.mcp.json`, `CLAUDE.md`, `.claude/skills/`). Nothing is installed globally, so unrelated projects never see CompanyOS."
      },
      {
        "type": "h3",
        "text": "Quick setup (one command)"
      },
      {
        "type": "p",
        "text": "From the root of a project you want connected, fetch the setup script, review it, and run it:"
      },
      {
        "type": "code",
        "lang": "bash",
        "code": "# from the root of a project you want connected\ncurl -fsSL https://company.chele.bi/companyos-agent-init.sh -o companyos-agent-init.sh\nbash companyos-agent-init.sh"
      },
      {
        "type": "p",
        "text": "It writes the three pieces below and is safe to re-run (it refreshes its own managed block rather than duplicating):"
      },
      {
        "type": "ul",
        "items": [
          "`.mcp.json` — a project-scoped connection to the CompanyOS MCP (OAuth; no token is stored in the file).",
          "`CLAUDE.md` — a marked **CompanyOS** block that tells the agent to search and save in CompanyOS first.",
          "`.claude/skills/companyos/SKILL.md` — an on-demand skill with the tool map and when to use it."
        ]
      },
      {
        "type": "h3",
        "text": "Authorize once"
      },
      {
        "type": "steps",
        "steps": [
          {
            "title": "Open the project",
            "text": "Open it in Claude Code (or your MCP client). It detects `.mcp.json` and asks to approve the `companyos` server."
          },
          {
            "title": "Run /mcp",
            "text": "Run `/mcp` and approve **companyos**. A browser opens for CompanyOS consent — pick your workspace and grant access (tick **Root / Admin** for the full tool surface)."
          },
          {
            "title": "Done",
            "text": "Your agent now uses CompanyOS for project search and save in this project, and nowhere else."
          }
        ]
      },
      {
        "type": "h3",
        "text": "Prefer to wire it by hand?"
      },
      {
        "type": "p",
        "text": "The script only writes these three things — you can paste them yourself, which also works for Cursor, Claude Desktop, and other MCP clients."
      },
      {
        "type": "p",
        "text": "**1.** `.mcp.json` at the project root:"
      },
      {
        "type": "code",
        "lang": "json",
        "code": "{\n  \"mcpServers\": {\n    \"companyos\": {\n      \"type\": \"http\",\n      \"url\": \"https://api.company.chele.bi/api/v1/mcp\"\n    }\n  }\n}"
      },
      {
        "type": "p",
        "text": "**2.** A CompanyOS block in `CLAUDE.md` (or your client's project rules file):"
      },
      {
        "type": "code",
        "lang": "markdown",
        "code": "## CompanyOS (company brain)\n\nCompanyOS is the source of truth for this org's projects, tasks, meetings,\nnotes, calendar, and activity.\n\n- Search CompanyOS (`mcp__companyos__*`) before answering anything about the\n  company, a project, a task, a person, or a deadline.\n- Save tasks, notes, decisions, and follow-ups to CompanyOS, not just locally.\n- Treat it as authoritative; local memory should point to it, not duplicate it."
      },
      {
        "type": "p",
        "text": "**3.** Optionally, a skill at `.claude/skills/companyos/SKILL.md` whose description triggers on project search/save and lists the `mcp__companyos__*` tools."
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "Memory, not duplication",
        "text": "Let CompanyOS hold the data and have your agent's local memory point to it. One source of truth, no drift between the brain and scattered notes."
      },
      {
        "type": "h3",
        "text": "Other clients"
      },
      {
        "type": "p",
        "text": "Cursor and Claude Desktop also read a project `.mcp.json` (or their own MCP settings) plus a project rules file. Use the same three pieces, putting the routing block in that client's rules file instead of `CLAUDE.md`."
      }
    ]
  },
  {
    "title": "References & Mentions",
    "slug": "references-and-mentions",
    "description": "How inline @-references link tasks, notes, and people inside descriptions and comments, including the exact wire format so AI agents can read and create references through the MCP.",
    "blocks": [
      {
        "type": "h2",
        "text": "What a reference is"
      },
      {
        "type": "p",
        "text": "A reference is an inline @-mention that links one item to another (a task, a note, or a person) directly inside a task description, a project description, or a task comment. It renders as a compact chip showing the target's title, and clicking it jumps to that item. References keep work connected, so a task can point at the runbook note it depends on, and a description can cite a related task."
      },
      {
        "type": "h2",
        "text": "Creating a reference in the app"
      },
      {
        "type": "p",
        "text": "Type @ where you want the link. A picker opens listing the tasks and notes in the current project (and people), filtered as you type. Pick one and CompanyOS inserts a chip that is clickable right away and persists across save and reload."
      },
      {
        "type": "steps",
        "steps": [
          { "title": "Type @", "text": "In a task description, project description, or comment composer, type @ followed by a few letters of the target's title." },
          { "title": "Pick a target", "text": "The picker lists matching tasks (shown with their # identifier) and notes (shown with a Note tag). Select with the mouse, or the arrow keys and Enter." },
          { "title": "It becomes a chip", "text": "CompanyOS inserts a reference chip. Click it any time to open the referenced task or note." }
        ]
      },
      {
        "type": "h2",
        "text": "Kinds of reference"
      },
      {
        "type": "table",
        "headers": ["Kind", "Looks like", "Links to"],
        "rows": [
          ["task", "a # chip in monospace", "the task, opened in the task view"],
          ["note", "a chip with a note icon", "the note, opened in the notes view"],
          ["user", "an @ chip", "a person. This is a mention, not a navigation target"]
        ]
      },
      {
        "type": "h2",
        "text": "The wire format: how a reference is stored"
      },
      {
        "type": "p",
        "text": "Descriptions and comments are stored as Markdown. A reference is encoded as a standard Markdown link whose href is a relative sentinel path carrying the kind and the id of the target, in the form below."
      },
      {
        "type": "code",
        "lang": "markdown",
        "code": "[Visible label](/__mention/<kind>/<id>)"
      },
      {
        "type": "p",
        "text": "Here the kind is one of `task`, `note`, or `user`, the id is the target's identifier, and the visible label is the link text. For example:"
      },
      {
        "type": "code",
        "lang": "markdown",
        "code": "[Runbook — Deploy a backend change](/__mention/note/019ed7a1-2b3c-7d4e-9f01-aabbccddeeff)"
      },
      {
        "type": "p",
        "text": "When the text is rendered, CompanyOS recognizes any link whose href begins with `/__mention/` and re-hydrates it into a clickable reference chip. Ordinary Markdown links are left untouched. Because the kind and id live in the href, the reference survives the save and reload round trip. The label is display only, and the id is the source of truth."
      },
      {
        "type": "callout",
        "variant": "info",
        "title": "Why a relative path",
        "text": "The href is a relative sentinel path (`/__mention/...`), not an absolute URL, so it stays stable across environments. The editor intercepts it before it would ever be followed as a normal link."
      },
      {
        "type": "h2",
        "text": "Creating references as an AI agent (via the MCP)"
      },
      {
        "type": "p",
        "text": "Because a reference is just a Markdown link, an agent can embed one wherever a description or comment is written through the Company-Brain MCP: the `description` field of `create_task` and `update_task`, and the `content` field of `create_comment`. Write the link form inline and it renders as a chip for everyone who opens the item."
      },
      {
        "type": "steps",
        "steps": [
          { "title": "Resolve the id", "text": "Look up the target id first. Use `list_project_tasks` or `get_task` for a task, and `list_notes` or `get_note` for a note. Take the returned id." },
          { "title": "Embed the link", "text": "Inside the Markdown, write the reference link using that id, in the form shown in the example below." },
          { "title": "Write it", "text": "Call `update_task` with the new description, or `create_comment` with the content. The reference renders as a clickable chip for everyone who opens the item." }
        ]
      },
      {
        "type": "code",
        "lang": "markdown",
        "code": "## Plan\nMirror the steps in [Runbook — Deploy a backend change](/__mention/note/019ed7a1-2b3c-7d4e-9f01-aabbccddeeff).\nThis work is blocked by [#HML-42](/__mention/task/019ed802-4f5a-7b6c-8d9e-001122334455)."
      },
      {
        "type": "callout",
        "variant": "tip",
        "title": "Keep the label human, keep the id exact",
        "text": "The label is what readers see, so make it a short, readable title. The kind and id are what make the chip resolve, so they must be accurate. If the id does not match an entity the reader can access, the chip will not open anything."
      },
      {
        "type": "h2",
        "text": "Where references render as chips"
      },
      {
        "type": "ul",
        "items": [
          "Task descriptions.",
          "Project descriptions.",
          "Task comments can be composed with @, and the same link form is stored in the comment text."
        ]
      },
      {
        "type": "h2",
        "text": "Rules and behavior"
      },
      {
        "type": "ul",
        "items": [
          "References round trip. They are saved in the Markdown and re-hydrate into chips on reload, not only during the current edit session.",
          "Only links whose href starts with `/__mention/` become references. Normal Markdown links stay normal links.",
          "The label is display text and the id is authoritative. Editing the label does not change the target.",
          "Avoid unescaped square brackets in the label so the link form stays valid.",
          "The id must belong to an entity in the same organization, and the viewer must have access for the chip to open it."
        ]
      }
    ]
  }
];
