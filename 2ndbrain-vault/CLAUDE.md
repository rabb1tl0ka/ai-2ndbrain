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

{{USER_NAME}} tracks relationships with key people using a consistent 4-file structure per person.

**Applies to**: `user/relationships/` (stakeholders, peers, direct reports — anyone worth tracking)

| File | Purpose | Content Type |
|------|---------|--------------|
| **profile.md** | Understanding the person | Goals, Challenges/Pains, Strengths & Style (team) or Needs/Wants (stakeholders), what makes them tick |
| **meetings.md** | Formal 1-on-1 interactions | Dated entries with Key Takeaways, Action Items |
| **log.md** | Captain's Log of observations | Notable interactions from any source (Slack, email, casual chats) — What Happened / What It Means / Follow-up |
| **tasks.md** | Action items for this person | Checkbox list of actions {{USER_NAME}} is taking for or because of them |
