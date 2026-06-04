---
argument-hint: [--meetings]
---

# /recap — Daily Session Summary

Write today's session log based on Claude Code sessions from the last 24 hours.

---

## Step 0: Resolve vault path and load user profile

The vault is this repo — resolve the absolute path:

```bash
pwd
```

Call the output `VAULT_PATH`. Use this exact resolved string everywhere a path is needed — never use shell variables in tool calls.

Then read the user profile at `<VAULT_PATH>/user/user.md`.

Use the **Role**, **Observation Lens**, and **Tone** sections to inform the note. If the file doesn't exist, proceed without it.

---

## Step 0.5: Parse --meetings flag

Check the command arguments. If `--meetings` was included, set `WITH_MEETINGS=true`. Otherwise `WITH_MEETINGS=false`.

All Drive-related steps are skipped when `WITH_MEETINGS=false`.

---

## Step 1: Get session data

### Check for existing cache first

```bash
WORK_DAY=$(python3 -c "
from datetime import datetime, timedelta
now = datetime.now()
d = (now - timedelta(days=1)).strftime('%Y-%m-%d') if now.hour < 4 else now.strftime('%Y-%m-%d')
print(d)
")
CACHE_FILE="$HOME/.claude/recap/cache/${WORK_DAY}.json"
ls "$CACHE_FILE" 2>/dev/null && echo "CACHE_EXISTS" || echo "NO_CACHE"
```

- If cache exists → read it: `cat "$CACHE_FILE"` — skip extraction
- If no cache → run the extractor:

```bash
python3 <VAULT_PATH>/.kernel/recap/extract_sessions.py
```

The extractor writes the cache to `~/.claude/recap/cache/` and prints JSON to stdout.

---

## Step 1b: Fetch meeting transcripts from Google Drive

> **Skip this entire step if `WITH_MEETINGS=false`.**

### Time window

Read `last_meetings_covered_until` from `~/.claude/recap/state.json`. If absent, fall back to 24h ago.

Apply a hard cap: compute `now - 5 days` and use whichever is more recent. This prevents a stale state from pulling weeks of meetings at once.

### Resolve Drive folder

Read `DRIVE_FOLDERS` from `<VAULT_PATH>/config.yaml`. Use the first folder URL. Extract the folder ID (the segment after `/folders/`).

If `DRIVE_FOLDERS` is empty, skip this step silently.

### Fetch docs

Load `mcp__claude_ai_Google_Drive__search_files` via ToolSearch, then search:

- Folder ID from above
- File name contains: `Notes by Gemini`
- Modified after: `covered_from`

### Read and truncate each doc

For each file returned:

1. Call `mcp__claude_ai_Google_Drive__read_file_content` with the file ID
2. Find the first occurrence of `# 📝 Transcript` or `# Transcript`
3. Discard that line and everything after it — keep only the notes section
4. Extract: meeting title and time, attendees, summary, decisions, next steps assigned to the vault owner (from `USER_NAME` in config.yaml), owner contributions from Details

### If no files found

Set `meetings = []` — the note will say "No meetings recorded in this period."

---

## Step 2: Determine note path

Use `work_day_date` from the JSON (not `date`).

`work_day_date_nodash` = `work_day_date` with dashes removed (e.g. `2026-04-21` → `20260421`).

Note path: `<VAULT_PATH>/user/private/daily-claude-sessions/claude-session-<work_day_date_nodash>.md`

Check if it already exists:
```bash
ls "<VAULT_PATH>/user/private/daily-claude-sessions/claude-session-<work_day_date_nodash>.md" 2>/dev/null && echo "EXISTS" || echo "NEW"
```

---

## Step 3: Write the note

### If the file does NOT exist — write a full note:

```markdown
---
date: YYYY-MM-DD
---

# <Month Day, Year>

## Overview
<One sentence capturing the theme of the day.>

## Achievements & Progress
<Bullet list of concrete completions.>

## Projects & Repos
| Project | Activity | Files Changed |
|---------|----------|---------------|

## Things I Learned
<Technical, process, or strategic learnings.>

## Claude's Observations
<2–4 bullets. Honest and sharp.>

## Open Threads
<Things started but not clearly resolved.>

## Meetings
<Only if WITH_MEETINGS=true. One block per meeting. If meetings=[], write: "No meetings recorded in this period.">

### <Meeting Title> — <HH:MM>
**Attendees**: ...
**Summary**: ...
**Decisions**: ...
**My Next Steps**: ...
**My Contributions**: ...
```

### If the file ALREADY EXISTS — append this block:

```markdown

---

## Claude Code Session — <HH:MM>

### Achievements & Progress
...

### Projects & Repos
| Project | Activity | Files Changed |
|---------|----------|---------------|

### Things I Learned
...

### Claude's Observations
...

### Open Threads
...

### Meetings
<Only if WITH_MEETINGS=true. Same format as above.>
```

---

## Step 4: Write the file

Use Write tool (new files) or Edit tool (append to existing).

Path: `<VAULT_PATH>/user/private/daily-claude-sessions/claude-session-<work_day_date_nodash>.md`

Use the concrete absolute path — no shell variables or `~`.

---

## Step 5: Save state and clean up cache

```bash
python3 -c "
import json
from pathlib import Path
cache_path = Path('$HOME/.claude/recap/cache/<work_day_date>.json')
state_path = Path('$HOME/.claude/recap/state.json')
try:
    cache = json.loads(cache_path.read_text())
    covered_until = cache.get('covered_until')
    if covered_until:
        try:
            state = json.loads(state_path.read_text())
        except Exception:
            state = {}
        state['last_covered_until'] = covered_until
        state_path.write_text(json.dumps(state))
except Exception as e:
    print(f'state save warning: {e}')
"
rm -f ~/.claude/recap/cache/<work_day_date>.json
```

If `WITH_MEETINGS=true`, also update `last_meetings_covered_until`:

```bash
python3 -c "
import json
from datetime import datetime, timezone
from pathlib import Path
state_path = Path('$HOME/.claude/recap/state.json')
state_path.parent.mkdir(parents=True, exist_ok=True)
try:
    state = json.loads(state_path.read_text())
except Exception:
    state = {}
state['last_meetings_covered_until'] = datetime.now(timezone.utc).isoformat()
state_path.write_text(json.dumps(state))
"
```

---

## Edge cases

- **No sessions in last 24h**: write a minimal note with `No Claude Code sessions recorded today.`
- **Cache from a different work_day_date**: ignore, run fresh extraction
- **Extraction fails**: print error, exit. Cache (if written) reused next time.
- **user.md missing**: proceed without user context
- **--meetings: no Drive files found**: write `No meetings recorded in this period.` under `## Meetings`
- **--meetings: Drive search fails**: note the failure inline, do not abort the recap
- **--meetings: doc has no Transcript marker**: read full content as-is
- **--meetings: last run > 5 days ago**: silently cap window to 5 days, no warning
