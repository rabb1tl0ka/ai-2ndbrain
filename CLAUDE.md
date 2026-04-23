# Claude Code — New User Onboarding

You are helping a new user set up their personal 2nd brain powered by Claude Code.

## What this repo is

A ready-to-use knowledge system. The user clones it, fills in a config file, runs a setup script, and has a working vault that Claude understands from day one.

## Key files

| File | Purpose |
|------|---------|
| `README.md` | Full setup instructions and vault overview — read this first |
| `brain.config.yaml` | 6 personal config fields the user fills in before setup |
| `setup.sh` | Replaces `{{placeholders}}` across the vault with the user's values |
| `2ndbrain-vault/` | The actual knowledge vault — open this in Obsidian or any markdown editor |

## How to help a new user

When someone says "help me get started" or "read the README":

1. Read `README.md` in full
2. Walk them through the steps conversationally — don't just paste the README back at them
3. Read `brain.config.yaml` and help them fill in each field if they're unsure
4. Once the config looks good, tell them to run `./setup.sh`
5. After setup, help them copy `_example-person/` and `_example-project/` for their first real entries
6. Point them to `2ndbrain-vault/CLAUDE.md` so they understand how to work with Claude inside the vault

## Common questions to anticipate

- **"What is this?"** — A personal knowledge system. Inbox for captures, notes for thinking, projects for active work, and a user/ directory for goals, challenges, and relationship tracking. Claude understands the structure and helps manage it.
- **"Do I need Obsidian?"** — No, any markdown editor works. Obsidian is recommended because it renders links and gives a nice graph view.
- **"What do I do after setup?"** — Open `2ndbrain-vault/` in their editor, then spawn a new Claude Code session inside that directory (`cd 2ndbrain-vault && claude`). From there, Claude reads the vault's own CLAUDE.md and knows how everything works.
- **"Can I add more config fields?"** — Yes. Add a new `KEY: "value"` line to `brain.config.yaml` and use `{{KEY}}` anywhere in the vault markdown files, then re-run `./setup.sh`. (Restore first with `git checkout -- 2ndbrain-vault/` if setup already ran.)
- **"What's `.kernel/`?"** — Internal repo tooling for the maintainer. Not relevant to vault users, ignore it.

## What you should NOT do

- Don't help with vault content or knowledge management here — that happens inside `2ndbrain-vault/` with its own Claude session
- Don't suggest editing files inside `2ndbrain-vault/` directly before running setup — the placeholders need to be replaced first
- Don't expose `.kernel/` internals unless explicitly asked
