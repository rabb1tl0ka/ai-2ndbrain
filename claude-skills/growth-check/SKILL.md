---
name: growth-check
description: Reads Claude session recaps since the last run and produces (1) a run report covering the new period and (2) an updated living sessions-growth-state.md that reflects current standing against your growth-plan.md.
argument-hint: (none)
---

# /growth-check — Growth Plan Progress Check

Analyze Claude session recaps since the last run, produce a period report, and update the living growth state.

---

## Step 0: Resolve vault path

```bash
echo "${CLAUDE_SKILLS_VAULT:-$HOME/2ndbrain}"
```

Call the output `VAULT_PATH`. Use this exact resolved string everywhere — never use shell variables in tool call paths.

---

## Step 1: Load state and find recaps to process

Read the state file:

```bash
cat ~/.claude/skills/growth-check/state.json 2>/dev/null || echo "NO_STATE"
```

The state file contains `last_covered_recap` — the filename (not full path) of the last recap processed (e.g. `claude-session-20260516.md`).

Note on file locations:
- `sessions-growth-state.md` lives at `<VAULT_PATH>/<state-dir>/sessions-growth-state.md` where `state-dir` comes from `growth-plan.md` frontmatter (default: `user/growth-plan`)
- Run reports live at `<VAULT_PATH>/user/private/growth-check/reports/<RUN_DATE>.md`

List all recap files sorted alphabetically (alphabetical = chronological):

```bash
ls <VAULT_PATH>/user/private/daily-claude-sessions/claude-session-*.md 2>/dev/null | sort
```

**If NO_STATE (first run):** process ALL recap files found.

**If state exists:** process only recap files whose filename sorts after `last_covered_recap`. Use simple string comparison on filenames — `claude-session-20260517.md` > `claude-session-20260516.md`.

If no new recaps exist since the last run, write one line to stdout: "No new recaps since last run." and stop — do not write any files.

Capture:
- `RECAP_FILES`: list of full paths to process
- `LAST_RECAP`: filename of the most recent recap in the list (e.g. `claude-session-20260516.md`)
- `PERIOD_START`: date from the first recap filename (strip `claude-session-` and `.md`, format as YYYY-MM-DD)
- `PERIOD_END`: date from the last recap filename
- `RUN_DATE`: today's date (`date +%Y-%m-%d`)
- `RUN_TIME`: current local time (`date +%H:%M`)

---

## Step 2: Load all context

Read each file in `RECAP_FILES` (use the Read tool).

Then read the growth plan:

```bash
ls <VAULT_PATH>/growth-plan.md 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

If MISSING: print the following and stop — do not create any files:

```
growth-plan.md not found at <VAULT_PATH>/growth-plan.md

Copy the template from:
~/.claude/skills/growth-check/growth-plan-template.md → <VAULT_PATH>/growth-plan.md

Fill in your focus behaviors, level framework, and name, then re-run /growth-check.
```

If EXISTS: read `<VAULT_PATH>/growth-plan.md` with the Read tool.

Check the frontmatter for optional keys:
- `patterns-file:` — if present, read that file (relative to VAULT_PATH)
- `cpf-scorecard:` — if present, read that file (relative to VAULT_PATH)
- `state-dir:` — directory (relative to VAULT_PATH) where `sessions-growth-state.md` is written and read (default: `user/growth-plan`)

If optional keys are missing or the files don't exist, proceed without them.

Then check if a current growth state exists and read it if so (using the resolved `state-dir`):

```bash
ls <VAULT_PATH>/<state-dir>/sessions-growth-state.md 2>/dev/null && echo "EXISTS" || echo "NEW"
```

If it exists, read it with the Read tool. This is the **previous state** — you will need it in Step 4 to write the delta.

---

## Step 3: Write the run report

**Path:** `<VAULT_PATH>/user/private/growth-check/reports/<RUN_DATE>.md`

Check if it already exists:

```bash
ls <VAULT_PATH>/user/private/growth-check/reports/<RUN_DATE>.md 2>/dev/null && echo "EXISTS" || echo "NEW"
```

**If NEW**, write the full report. **If EXISTS**, append a `---` separator and the block below with the current `RUN_TIME` in the header.

```markdown
---
date: <RUN_DATE>
period: <PERIOD_START> to <PERIOD_END>
recaps-analyzed: <count>
---

# Growth Check — <RUN_DATE>
Period: <PERIOD_START> → <PERIOD_END> (<N> recaps)

## Recaps Analyzed
- `claude-session-YYYYMMDD.md` — one bullet per file, one-line summary of what that day was about

## Behaviors Observed

For each focus behavior listed in `growth-plan.md`, generate one subsection. Quote or closely paraphrase specific moments from the recaps — no vague summaries. If a behavior had no observable evidence, say "No evidence in this period."

[One subsection per behavior from growth-plan.md]

## Behavior Score (this period)

For each focus behavior from growth-plan.md, one line:
- [Behavior name]: [strong / partial / low / no evidence]

## Leadership Focus (this period)

Using the leadership focus defined in `growth-plan.md` (e.g. multiplier shift, delegation, spotlight moves — whatever the plan names):
List specific moments from the recaps. If none observed: "None visible in session recaps for this period."

Note: IC work on assigned client deliverables is expected ownership — only flag as a miss if the plan explicitly calls it out.

## Growth Framework Standing (this period)

Using the level framework and success criteria defined in `growth-plan.md`:

**Operating at expected level:**
[specific behaviors that match — be concrete]

**Operating below expected level:**
[gaps — be direct, no softening]

**Operating above expected level:**
[moments where the person exceeded their current level — "None observed" if clean]

## Shift vs Previous State
[Compare against the previous sessions-growth-state.md. What improved? What regressed? What's unchanged?
If this is the first run, write "First run — no previous state to compare against."]
```

Use the Write tool for new files, Edit tool to append to existing ones.

---

## Step 4: Write the updated sessions-growth-state.md

**Path:** `<VAULT_PATH>/<state-dir>/sessions-growth-state.md` (resolve `state-dir` from growth-plan.md frontmatter, default `user/growth-plan`)

This file is always overwritten (Write tool). It is the single source of truth for current growth standing.

```markdown
---
updated: <RUN_DATE>
recaps-covered-through: <LAST_RECAP>
total-recaps-reviewed: <cumulative count — increment from previous state if it existed, otherwise count of recaps this run>
---

# Growth State — [Name from growth-plan.md] [Year]

## Focus Behaviors (current standing)

For each focus behavior from `growth-plan.md`, give a current rating and 1-2 sentences of evidence.
Base this on the full picture: previous state + new run report.

[One entry per behavior from growth-plan.md]
**[Behavior name]:** [strong / partial / low]
[Evidence]

## Leadership Focus (current standing)

[1-3 sentences using the leadership focus framing from growth-plan.md.
What's the trend? What's the most recent signal?]

## Growth Framework Standing

For each level dimension defined in `growth-plan.md`:

**[Dimension name]:** [meeting expected level / below expected level / above expected level]
[Evidence]

## Active Patterns

[Distilled cross-session patterns. Pull from patterns.md + observations across recaps.
Only include patterns with evidence across multiple sessions — not one-offs.
3-6 bullets max.]

## What Changed Since Last Run

[3-5 bullets. What's different from the previous sessions-growth-state.md?
Be specific: "Ask before tell moved from partial to strong — 1:1 with Ronny on May 12 showed..."
If this is the first run: "Initial baseline established."]

## Watch Going Forward

[2-3 specific things to look for in upcoming sessions — open threads, patterns that need confirmation, behaviors to test]
```

---

## Step 5: Save state

```bash
python3 -c "
import json
from pathlib import Path
state_dir = Path('$HOME/.claude/skills/growth-check')
state_dir.mkdir(parents=True, exist_ok=True)
state_dir.joinpath('state.json').write_text(json.dumps({'last_covered_recap': '<LAST_RECAP>'}))
print('state saved: <LAST_RECAP>')
"
```

Replace `<LAST_RECAP>` with the actual filename string before running.

---

## Edge cases

- **No recap files found at all**: write one line to stdout and stop. Do not create any files.
- **growth-plan.md missing**: print setup instructions and stop. Do not create any files.
- **patterns.md or cpf-scorecard.md missing**: skip, proceed without them
- **sessions-growth-state.md missing on non-first run**: treat as first run for the delta section
- **Report file already exists for today**: append with `---` separator and `## Growth Check — <RUN_DATE> <RUN_TIME>` header
