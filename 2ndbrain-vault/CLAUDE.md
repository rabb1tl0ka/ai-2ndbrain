# Claude Code Instructions

This is {{USER_NAME}}'s 2nd brain vault — a collection of notes that hold their knowledge about {{VAULT_FOCUS}}.

Read `user/` for info about {{USER_NAME}}: role, goals, context, and work style.

## Vault Structure

| Directory | Purpose | Lifecycle |
|-----------|---------|-----------|
| `inbox/` | Temporary queue for captures, ideas, meeting notes | Gets processed and moved out |
| `archive/` | Processed inbox items worth keeping but not categorized | Done, stored |
| `sources/` | External content (articles, references, research) | Stays as-is |
| `notes/` | {{USER_NAME}}'s thinking and knowledge | Evergreen |
| `learning/` | Knowledge being built (skills, topics, craft) | Grows over time |
| `projects/` | Project-level knowledge for active work | Active work |
| `user/` | {{USER_NAME}}: goals, challenges, development, relationships | Reference |
| `daily/` | Daily notes | Chronological |

## Quick Reference

- **Inbox processing**: Read inbox items, process and move to `archive/`, `sources/`, `projects/`, `learning/`, or `notes/`
- **No magic routing**: Everything lands in inbox first. {{USER_NAME}} decides where it goes.
- **Sources**: External content with `by:` frontmatter, `source:` URL, `date:` field
- **Attribution**: Use `by:` frontmatter for whole-note attribution
- **{{USER_NAME}}'s words**: No `by:` field needed

## Key Documents

Add your most important reference documents here after setup. Examples:

- **`user/development/plan.md`** — {{USER_NAME}}'s development plan. When {{USER_NAME}} asks to process interactions for their development plan, read the full protocol at `user/development/CLAUDE.md` first.
- **`{{KEY_DOC_1_PATH}}`** — {{KEY_DOC_1_DESC}}
- **`{{KEY_DOC_2_PATH}}`** — {{KEY_DOC_2_DESC}}

## Daily Notes Structure

Each day creates both a markdown file and a directory:
- **`daily/YYYY-MM-DD.md`** - Summary and index of the day's work (links to detailed notes)
- **`daily/YYYY-MM-DD/`** - Directory holding detailed research, extensive notes, and work products from that day

Use the directory for:
- Research too extensive to keep inline (ML workstation specs, technical deep-dives, etc.)
- Drafts and working notes not yet ready for `/notes/`
- Project work, experiments, or exploration specific to that day
- Files you're deciding whether to move to `/learning/`, `/notes/`, or `/archive/`

Link from the daily markdown to files in the directory so the daily file remains an index/summary. Clean up or archive the directory later if its contents aren't worth keeping.

## Saving External Content

All external content uses this frontmatter:

```markdown
---
by: "Author or @Handle"
source: https://...
date: YYYY-MM-DD
---

Content here

#optional-tags
```

Content lands in `inbox/` first. {{USER_NAME}} decides when to move to `sources/`.

## Preparing Messages for Relationships

When {{USER_NAME}} asks to "prep a msg" or "draft a message" for someone:

**Directory structure**: `user/relationships/{person}/messages/`

**File naming pattern**: `msg_{msg-title}_yyyy-MM-dd.md`

**Frontmatter template**:
```markdown
---
to: {Person Name}
date: YYYY-MM-DD
status: draft
topic: {Brief Topic}
---
```

**Process**:
1. Create the `messages/` directory if it doesn't exist
2. Draft the message based on context (Slack msg, email, etc.)
3. Save with proper naming pattern and frontmatter
4. Consider the relationship context (manager, peer, client) when setting tone

## Session Commands

| Command | Action |
|---------|--------|
| `report today` | Generate summary for current date |
| `report yesterday` | Generate summary for previous day |
| `report YYYY-MM-DD` | Generate summary for specific date |
| `log today` | Quick append to daily log (no confirmation) |

## Session Logging & Daily Reports

Two-tier system for tracking work:

**Layer 1 — Raw Session Logs** (automatic):
- Location: `.claude/session-logs/`
- Triggered: automatically on session end via SessionEnd hook
- Format: `YYYY-MM-DD_HHMMSS_sessionid.md`
- Content: full transcript — successes, failures, tangents, everything

**Layer 2 — Daily Summaries** (manual):
- Location: `daily/`
- Triggered: user says "report today"
- Format: `YYYY-MM-DD.md`
- Content: smart summary generated from session logs

Reports merge new content with existing daily files — nothing gets overwritten.

## Relationship & Team Tracking System

Two separate systems depending on the relationship type:

| System | Location | Who it covers |
|--------|----------|---------------|
| **Internal relationships** | `user/relationships/{firstname-lastname}/` | Colleagues, peers, direct reports, managers — same company |
| **Project stakeholders** | `projects/{project}/stakeholders/{firstname-lastname}/` | Clients, external partners — scoped to a specific engagement |

**Applies to internal relationships**: `user/relationships/` (peers, direct reports — anyone worth tracking within the company)

| File | Purpose | Content Type |
|------|---------|--------------|
| **profile.md** | Understanding the person | Goals, Challenges/Pains, Strengths & Style (team) or Needs/Wants (stakeholders), what makes them tick |
| **meetings.md** | Formal 1-on-1 interactions | Dated entries with Key Takeaways, Action Items |
| **log.md** | Captain's Log of observations | Notable interactions from any source (Slack, email, casual chats) — What Happened / What It Means / Follow-up |
| **tasks.md** | Action items for this person | Checkbox list of actions {{USER_NAME}} is taking for or because of them |

### Creating new relationship profiles

When {{USER_NAME}} references a person who doesn't have a profile in `user/relationships/` yet — from a team.md, a meeting note, a Slack thread, or any other context — **create the stub immediately**:

1. Copy `_example-person/` → `user/relationships/{firstname-lastname}/`
2. Fill in what you know: name, role, division, Slack ID if available
3. Leave unknown fields as placeholders — don't block on missing info
4. Reference the new profile from wherever it was first mentioned

Never ask the user to do this manually.

### Creating new stakeholder profiles

When {{USER_NAME}} references a client or external stakeholder in the context of a project who doesn't have a profile yet:

1. Create `projects/{project}/stakeholders/{firstname-lastname}/profile.md` and a `messages/` directory
2. Fill in what you know: name, role, Slack ID and channels if available
3. Leave unknown fields as placeholders — don't block on missing info
4. Reference the new profile from wherever it was first mentioned

Never ask the user to do this manually.

### Looking up updates from a person

When {{USER_NAME}} asks "what's going on with [person] about [topic]":

1. Read their profile at `user/relationships/{person}/profile.md`
2. Use their Slack ID + `#channels` from their profile to target the search
3. Search those channels via Slack MCP for recent activity
4. Cross-reference with project channels from any relevant `projects/{project}/team/team.md`
5. Summarize findings and save anything notable to their `log.md`

## Integrations (MCP)

At the start of each session, check which MCP tools are available. Integrations multiply the vault's power — Claude can read from and act on external systems directly, without the user leaving the terminal.

### If integrations are available

**Slack**
- "Save this Slack thread to my inbox" → read the thread via Slack MCP, save to `inbox/` with source attribution
- "Draft and send a message to [person/channel]" → draft from vault context, send via Slack MCP
- "What did [person] say about X?" → search Slack, summarize, save anything relevant to inbox

**Notion**
- "Update this Notion page with [content]" → fetch the page, apply changes via Notion MCP
- "Pull this Notion page into my vault" → fetch and save to appropriate vault location
- "Sync my project notes to Notion" → read from `projects/`, update corresponding Notion pages

**Google Calendar**
- "Set up today's daily note" → pull today's events via Calendar MCP, pre-populate `daily/YYYY-MM-DD.md` with meeting context
- "Prep for my meeting with [person]" → fetch calendar event, cross-reference with relationship profile and project notes

**Gmail**
- "Save this email thread to my inbox" → fetch via Gmail MCP, save to `inbox/` with attribution
- "Draft a reply to [person]" → read email context, draft from vault relationship knowledge

### If integrations are NOT available

Tell the user:

> "I don't see any MCP integrations connected. You can activate Notion, Slack, Gmail, and Google Calendar at **claude.ai → Settings → Integrations**. Once connected, I can read and act on those tools directly from your vault sessions."

Don't repeat this message every session — only mention it once if the user seems unaware, or if they explicitly ask to do something that requires an integration.
