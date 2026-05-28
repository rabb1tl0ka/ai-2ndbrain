---
name: recap
description: Extracts Claude Code sessions from the last 24h and writes a structured session log to $CLAUDE_SKILLS_VAULT/user/private/daily-claude-sessions/ (default: ~/2ndbrain). Can be run standalone or invoked by bye-recap() before vault backup and shutdown.
argument-hint: [--meetings]
---

# /recap — Daily Session Summary

Write today's session log based on Claude Code sessions from the last 24 hours. Then clean up.

---

## Step 0: Resolve vault path and load user profile

Run this bash command and capture the output — this is your `VAULT_PATH` for all subsequent steps:

```bash
echo "${CLAUDE_SKILLS_VAULT:-$HOME/2ndbrain}"
```

Call the output `VAULT_PATH`. Use this **exact resolved string** (e.g. `/home/alice/2ndbrain`) everywhere a path is needed — never use `$VAULT` or `$CLAUDE_SKILLS_VAULT` as literals in tool calls.

Then read the user profile at `<VAULT_PATH>/user/user.md`.

Use the **Role**, **2026 Arc**, **Observation Lens**, and **Tone** sections from that file to inform the note — especially "Claude's Observations." If the file doesn't exist, proceed without it.

---

## Step 0.5: Parse --meetings flag

Check the skill arguments. If `--meetings` was included in the invocation (e.g. `/recap --meetings`), set `WITH_MEETINGS=true`. Otherwise set `WITH_MEETINGS=false`.

All Drive-related steps are skipped entirely when `WITH_MEETINGS=false`.

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
CACHE_FILE="$HOME/.claude/skills/recap/cache/${WORK_DAY}.json"
ls "$CACHE_FILE" 2>/dev/null && echo "CACHE_EXISTS" || echo "NO_CACHE"
```

- If cache exists → read it with `cat "$CACHE_FILE"` — skip extraction
- If no cache → run the extractor:

```bash
python3 ~/.claude/skills/recap/extract_sessions.py
```

The extractor writes the cache automatically and prints the same JSON to stdout.

---

## Step 1b: Fetch meeting transcripts from Google Drive

> **Skip this entire step if `WITH_MEETINGS=false`.**

### Time window

Read `last_meetings_covered_until` from `~/.claude/skills/recap/state.json`. If the field is absent, fall back to 24h ago.

Then apply a hard cap: compute `now - 5 days` and use whichever is **more recent** between `last_meetings_covered_until` and the cap. This prevents a stale state from pulling in weeks of meetings at once.

This window is independent of the Claude sessions window (`covered_from`) so meetings are never missed due to session timing.

### Fetch docs

Load `mcp__claude_ai_Google_Drive__search_files` via ToolSearch, then search:

- Folder ID: `1hdV9eXl8t7JyIe78tR7i5wuA3Qlk7O1e`
- File name contains: `Notes by Gemini`
- Modified after: `covered_from`

### Read and truncate each doc

For each file returned:

1. Call `mcp__claude_ai_Google_Drive__read_file_content` with the file ID
2. Find the first occurrence of `# 📝 Transcript` or `# Transcript` in the content
3. Discard that line and everything after it — only keep the notes section
4. From the notes section, extract:
   - **Meeting title and time** (from the doc title or top heading, format: `{title} - {date} - Notes by Gemini`)
   - **Attendees** (from the Invited line)
   - **Summary** (the Summary subsection)
   - **Decisions** (the Decisions subsection)
   - **My Next Steps** (items from Next Steps assigned to Bruno Coelho only)
   - **My Contributions** (bullets from the Details subsection that explicitly attribute something to Bruno — what he raised, decided, emphasized, or requested)

### If no files found

Set `meetings = []` — the note will say "No meetings recorded in this period."

---

## Step 2: Determine note path

Use `work_day_date` from the JSON (not `date`) — this handles sessions that run past midnight.

`work_day_date_nodash` = `work_day_date` with dashes removed (e.g. `2026-04-21` → `20260421`).

Note path: `<VAULT_PATH>/user/private/daily-claude-sessions/claude-session-<work_day_date_nodash>.md`

Check if the file already exists:
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
<One sentence capturing the theme of the day. What was this day actually about?>

## Achievements & Progress
<Bullet list of concrete completions. What exists now that didn't before? Be specific.>

## Projects & Repos
| Project | Activity | Files Changed |
|---------|----------|---------------|
<One row per project. Use short file names, not full paths.>

## Things I Learned
<Technical, process, or strategic learnings extracted from user prompts and bash command descriptions. If Notion/Slack/Jira tools were used, note what external work happened.>

## Claude's Observations
<2–4 bullets. Anchor to the user's growth goals where relevant. Honest and sharp.>

## Open Threads
<Things started but not clearly resolved — infer from prompts without obvious follow-through, files read but not modified, tasks that seemed mid-flight.>

## Meetings
<Include this section only if WITH_MEETINGS=true. For each meeting, use the block below. If meetings=[], write: "No meetings recorded in this period.">

### <Meeting Title> — <HH:MM>
**Attendees**: <comma-separated list>
**Summary**: <1-2 sentences from the Gemini summary>
**Decisions**: <bullet list from the Decisions section>
**My Next Steps**: <action items from Next Steps assigned to Bruno only; omit if none>
**My Contributions**: <what Bruno specifically raised, decided, emphasized, or requested — sourced from Details bullets that name him>
```

### If the file ALREADY EXISTS — append this block at the end:

```markdown

---

## Claude Code Session — <HH:MM>

### Achievements & Progress
<...>

### Projects & Repos
| Project | Activity | Files Changed |
|---------|----------|---------------|

### Things I Learned
<...>

### Claude's Observations
<...>

### Open Threads
<...>

### Meetings
<Include this subsection only if WITH_MEETINGS=true. Same format as the full-note Meetings section above.>
```

Use the current local time for `HH:MM`.

---

## Step 4: Write the file

Use the Write tool (for new files) or Edit tool (to append to existing files).

The file path is the resolved absolute path from Step 0:
`<VAULT_PATH>/user/private/daily-claude-sessions/claude-session-<work_day_date_nodash>.md`

Do not use shell variables or `~` in the path passed to the Write/Edit tool — use the concrete string.

---

## Step 5: Save state and clean up cache

After successfully writing the note, save the high-water mark from the cache (so the next run doesn't re-cover these sessions), then delete the cache:

```bash
python3 -c "
import json
from pathlib import Path
cache = json.loads(Path('$HOME/.claude/skills/recap/cache/<work_day_date>.json').read_text())
covered_until = cache.get('covered_until')
if covered_until:
    state_path = Path('$HOME/.claude/skills/recap/state.json')
    try:
        state = json.loads(state_path.read_text())
    except Exception:
        state = {}
    state['last_covered_until'] = covered_until
    state_path.write_text(json.dumps(state))
"
rm -f ~/.claude/skills/recap/cache/<work_day_date>.json
```

If `WITH_MEETINGS=true`, also update `last_meetings_covered_until` to the current UTC timestamp:

```bash
python3 -c "
import json
from datetime import datetime, timezone
from pathlib import Path
state_path = Path('$HOME/.claude/skills/recap/state.json')
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

- **No sessions in last 24h**: write a minimal note — date frontmatter, header, and one line: `No Claude Code sessions recorded today.`
- **Cache exists but is from a different work_day_date**: ignore it, run fresh extraction
- **Extraction fails**: print the error and exit non-zero. The shell wrapper will warn the user and proceed to shutdown anyway. The cache (if written) will be reused next time.
- **user.md missing**: proceed without user context — don't fail the skill
- **--meetings: no Drive files found**: write `No meetings recorded in this period.` under `## Meetings` — never omit the section silently when `WITH_MEETINGS=true`
- **--meetings: Drive search or read fails**: note the failure inline under `## Meetings` (e.g. `Could not fetch meetings: <error>`), do not abort the rest of the recap
- **--meetings: a doc has no `# 📝 Transcript` marker**: read the full content as-is (it may be a shorter notes-only doc)
- **--meetings: last run was more than 5 days ago**: silently cap the window to 5 days back — don't warn, don't explain, just cap it
