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
brain.config.example.yaml  ← config template (copy → brain.config.yaml, then fill in)
brain.config.yaml          ← your personal config, gitignored — never committed
setup.sh                   ← applies your config to the vault
```

## Setup

**1. Clone**
```bash
git clone https://github.com/rabb1tl0ka/ai-2ndbrain
cd ai-2ndbrain
```

**2. Fill in your config**

Run setup once to generate your personal config file:
```bash
./setup.sh
```

On first run, the script creates `brain.config.yaml` from the example template and exits. Fill in your details — 7 fields, takes 2 minutes:

```yaml
USER_NAME: "Your Name"
USER_HANDLE: "@yourhandle"
USER_ROLE: "Your Role"
USER_COMPANY: "Your Company"
USER_CONTEXT: "Describe your work context in 1-2 sentences."
VAULT_FOCUS: "work at Your Company"
VAULT_PATH: "~/2ndbrain"   # where to install your vault
```

`brain.config.yaml` is gitignored — your personal values are never committed.

**3. Run setup again**
```bash
./setup.sh
```

Copies the vault to `VAULT_PATH` and replaces all `{{placeholders}}` with your values. Your vault lives outside this repo — your personal knowledge stays yours.

**4. Open the vault and spawn Claude Code**

Open your vault folder in Obsidian (or any markdown editor).

Then start a Claude Code session inside it:
```bash
cd ~/2ndbrain
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

## Power features: connecting external tools

The vault alone is useful. Connected to your external tools, it's a different level.

Claude can read from and act on Notion, Slack, Gmail, and Google Calendar directly inside your vault sessions — no copy-pasting, no context switching.

**What this unlocks:**
- *"Save this Slack thread to my inbox"* → Claude fetches it and saves it with attribution
- *"Update the Notion page with my meeting notes"* → Claude pushes changes directly
- *"Set up today's daily note"* → Claude pulls your calendar events and pre-populates the file
- *"Draft and send a message to [person]"* → Claude writes it from vault context and sends it

**How to set it up:**

Go to **[claude.ai → Settings → Integrations](https://claude.ai/settings/integrations)** and connect the tools you use. Once connected, they're available in every Claude Code session automatically.

If Claude doesn't see your integrations in a vault session, it will tell you and point you here.

## Requirements

- [Claude Code](https://claude.ai/code) — for AI-assisted knowledge work
- A markdown editor — [Obsidian](https://obsidian.md) recommended (any editor works)
- `bash` + `sed` — for `setup.sh` (standard on macOS and Linux)
