# 2nd Brain

A Claude-powered personal knowledge system. Clone it, configure it in 2 minutes, and have a working 2nd brain that Claude understands from day one.

## What's inside

```
2ndbrain-vault/        ← your knowledge vault (open this in Obsidian)
  inbox/               ← everything lands here first
  notes/               ← your thinking, evergreen
  learning/            ← knowledge being built
  sources/             ← external content (articles, references)
  daily/               ← daily notes
  archive/             ← processed inbox items worth keeping
  projects/            ← one folder per active project
  user/                ← who you are: goals, challenges, development, relationships
  templates/           ← note templates
brain.config.yaml      ← your personal config (fill this in)
setup.sh               ← applies your config to the vault
```

## Setup

**1. Clone**
```bash
git clone https://github.com/rabb1tl0ka/ai-2ndbrain
cd ai-2ndbrain
```

**2. Fill in your config**
```bash
# Edit brain.config.yaml — 6 fields, takes 2 minutes
```

```yaml
USER_NAME: "Your Name"
USER_HANDLE: "@yourhandle"
USER_ROLE: "Your Role"
USER_COMPANY: "Your Company"
USER_CONTEXT: "Describe your work context in 1-2 sentences."
VAULT_FOCUS: "work at Your Company"
```

**3. Run setup**
```bash
./setup.sh
```

That's it. All `{{placeholders}}` across the vault are replaced with your values.

**4. Add your first project and relationship**

```bash
# Start a new project
cp -r 2ndbrain-vault/projects/_example-project 2ndbrain-vault/projects/my-project

# Track a relationship
cp -r 2ndbrain-vault/user/relationships/_example-person 2ndbrain-vault/user/relationships/alex-chen
```

**5. Open the vault and spawn Claude Code**

Open `2ndbrain-vault/` in Obsidian (or any markdown editor).

Then start a Claude Code session inside the vault directory:
```bash
cd 2ndbrain-vault
claude
```

Claude reads `CLAUDE.md` automatically and knows how your vault works.

## How to use it

**Capture anything** → drop it in `inbox/` using `templates/inbox.md`

**Process inbox** → ask Claude: *"process my inbox"* — it reads each item and routes it to the right place

**Daily notes** → ask Claude: *"start today's note"* — creates `daily/YYYY-MM-DD.md`

**Track a relationship** → copy `_example-person/`, fill in `profile.md`, log interactions in `log.md`

**Develop yourself** → fill in `user/development/plan.md`, then ask Claude to process 1:1 notes or interactions against your plan

**Session reports** → ask Claude: *"report today"* — generates a summary from your session logs

## Vault structure in depth

| Directory | Purpose | Lifecycle |
|-----------|---------|-----------|
| `inbox/` | Raw captures — ideas, meeting notes, voice transcripts | Processed and moved out |
| `notes/` | Your thinking, written to last | Evergreen |
| `learning/` | Skills and knowledge being built | Grows over time |
| `sources/` | External content with attribution | Stays as-is |
| `daily/` | Daily notes and work logs | Chronological |
| `archive/` | Processed inbox items worth keeping | Done |
| `projects/` | Active project knowledge | Per-project lifecycle |
| `user/` | You: goals, challenges, development, relationships | Reference |

## Relationship tracking

Each person in `user/relationships/` gets 4 files:

| File | What goes here |
|------|---------------|
| `profile.md` | Who they are, what drives them, how to work with them |
| `meetings.md` | Formal 1:1s — key takeaways and action items |
| `log.md` | Observations from any interaction (Slack, email, hallway) |
| `tasks.md` | Actions you're taking for or because of them |

## Development plan

`user/development/` tracks your growth as a professional. Fill in `plan.md` with the behaviors you're building, then ask Claude to process interactions against it. The protocol in `user/development/CLAUDE.md` tells Claude how to extract evidence and write honest log entries.

## Requirements

- [Claude Code](https://claude.ai/code) — for AI-assisted knowledge work
- A markdown editor — [Obsidian](https://obsidian.md) recommended
- `bash` + `sed` — for `setup.sh` (standard on macOS and Linux)
