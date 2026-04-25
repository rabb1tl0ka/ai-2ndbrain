---
status: todo
priority: medium
owner: ""
---

# Idea: Vault-Owned Claude Skills + Automated Meeting Notes Import

## One-Line Overview
Consolidate all vault-related Claude Skills into this repo, and add a deterministic Python script that imports Google Meet transcripts from Drive into the vault — keeping AI for reasoning, not fetching.

## What's the idea

Two related architectural decisions that came out of the same exploration:

### 1. Vault-owned skills (`ai-2ndbrain/claude-skills/`)

All Claude Skills that power the 2nd brain vault should live in this repo under `claude-skills/`. Skills that aren't vault-specific stay wherever they are (e.g. `claude-skills/` personal repo).

The first candidate to migrate: `/recap` (currently at `~/loka/code/claude-skills/recap`). It writes to the vault, depends on vault path config, and has no reason to live outside this repo.

**Architectural principle**: the vault is self-contained. One repo has the vault structure, the setup tooling, and the AI skills that operate on it.

### 2. Deterministic meeting notes import (`scripts/import-meeting-notes.py`)

Google Meet + Gemini generates transcript/notes docs that land in `My Drive > Meet Recordings`. Instead of using MCP tools (burning tokens on a mechanical fetch), a Python script handles the import:

- Auth via Google Drive API (OAuth, token cached locally)
- List files in `Meet Recordings/` newer than last run (timestamp watermark)
- Download and convert Google Docs → markdown
- Write to the vault's `meeting-notes/YYYY-MM-DD-<title>.md`

Claude then reasons over the already-imported local files — no MCP needed at read time.

**Architectural principle**: deterministic data fetch = code. Reasoning over that data = AI. Don't mix the two.

## Expected advantages / benefits

- Vault is fully self-contained — clone + setup gives you everything
- `/recap` and future skills version-controlled alongside the vault they serve
- Meeting notes import is fast, cheap, offline-capable after initial fetch
- Claude reads local markdown directly, no token overhead per meeting access
- Google Drive stays as source of truth; local is just a synced cache

## Downsides / risks

- Migrating `/recap` out of `claude-skills/` repo requires a one-time cleanup
- Python import script needs OAuth setup on each new machine (same friction as rclone)
- Skill install step needs to be added to `setup.sh` (symlink `claude-skills/` → `~/.claude/skills/`)

## What's been tried already

- `/recap` skill is live and working in the personal Loka vault setup
- rclone crypt already handles encrypted backup of sensitive vault dirs (meeting-notes, relationships, etc.) to Google Drive — the import script is the reverse direction
- LUKS full-disk encryption is already in place, so a vault-level lock/unlock feature is unnecessary (solved at the OS layer)

## Open questions

1. Should `setup.sh` auto-install skills via symlinks, or copy them?
2. What's the right watermark strategy for the import script — timestamp file, or a manifest of already-imported Drive file IDs?
3. Should the import script also handle the rclone backup sync, or stay single-purpose?
4. Where does the OAuth token for the Drive API live — alongside the script, or in a shared credentials dir?
