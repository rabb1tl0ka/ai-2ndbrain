# ai-2ndbrain

A personal knowledge vault powered by Claude Code. Clone it, run `/onboard`, and have a working 2nd brain from day one.

## What this is

A ready-to-use knowledge system — structured around how personal knowledge actually flows: inbox for captures, notes for thinking, projects for active work, learning for skills you're building, and a user directory for goals, relationships, and development.

Claude understands the vault structure from day one and helps you manage it.

## Setup

**1. Use this as a GitHub Template (or clone it)**

Click "Use this template" on GitHub, or:

```bash
git clone https://github.com/your-username/ai-2ndbrain ~/my-2ndbrain
cd ~/my-2ndbrain
claude
```

**2. Run `/onboard`**

Opens a guided setup that collects your name, role, and vault focus, replaces placeholders across the vault, and optionally connects Google Drive and Slack.

**3. Run `/bootstrap` (optional)**

If you connected Drive or Slack during onboarding, bootstrap pulls data from those sources into your inbox so Claude has real context from the start.

**4. Start**

The vault is ready. Open it in Obsidian (or any markdown editor) and use Claude Code from the repo root.

## Vault structure

```
inbox/          ← everything lands here first
notes/          ← your thinking and knowledge
learning/       ← skills and topics you're building
projects/       ← active project knowledge
sources/        ← external content (articles, references)
archive/        ← processed inbox items worth keeping
daily/          ← daily notes
user/           ← goals, challenges, relationships, development
templates/      ← note templates
```

## Commands

| Command | What it does |
|---------|-------------|
| `/onboard` | Initial setup — run once after cloning |
| `/bootstrap` | Pull Drive + Slack into inbox |
| `/2ndbrain` | Current status and what to do next |
| `/recap` | Summarize today's Claude Code sessions |
| `/growth-check` | Progress check against your growth plan |

## Configuration

`/onboard` creates `config.yaml` (gitignored) from `config.example.yaml`. Edit it directly to update values or add integrations later.

## What's in `.kernel/`

Internal tooling for the template maintainer — roadmap, supporting scripts for commands. Not relevant to vault users.
