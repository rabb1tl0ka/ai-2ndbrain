# /growth-check — Growth Plan Progress Check

Analyze Claude session recaps since the last run, produce a period report, and update the living growth state.

---

## Step 0: Resolve vault path

```bash
pwd
```

Call the output `VAULT_PATH`. Use this exact resolved string everywhere — no shell variables in tool calls.

---

## Step 1: Load state and find recaps to process

Read the state file:

```bash
cat ~/.claude/growth-check/state.json 2>/dev/null || echo "NO_STATE"
```

The state contains `last_covered_recap` — the filename (not full path) of the last recap processed (e.g. `claude-session-20260516.md`).

Note on file locations:
- `sessions-growth-state.md` lives at `<VAULT_PATH>/<state-dir>/sessions-growth-state.md` where `state-dir` comes from `growth-plan.md` frontmatter (default: `user/growth-plan`)
- Run reports live at `<VAULT_PATH>/user/private/growth-check/reports/<RUN_DATE>.md`

List all recap files sorted alphabetically:

```bash
ls <VAULT_PATH>/user/private/daily-claude-sessions/claude-session-*.md 2>/dev/null | sort
```

**If NO_STATE (first run):** process ALL recap files found.

**If state exists:** process only recap files whose filename sorts after `last_covered_recap`.

If no new recaps exist, write "No new recaps since last run." and stop — do not write any files.

Capture:
- `RECAP_FILES`: list of full paths to process
- `LAST_RECAP`: filename of the most recent recap
- `PERIOD_START`: date from the first recap filename (YYYY-MM-DD)
- `PERIOD_END`: date from the last recap filename
- `RUN_DATE`: `date +%Y-%m-%d`
- `RUN_TIME`: `date +%H:%M`

---

## Step 2: Load all context

Read each file in `RECAP_FILES`.

Then read the growth plan:

```bash
ls <VAULT_PATH>/growth-plan.md 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

If MISSING, print:

```
growth-plan.md not found at <VAULT_PATH>/growth-plan.md

Copy the template:
  <VAULT_PATH>/.kernel/growth-check/growth-plan-template.md → <VAULT_PATH>/growth-plan.md

Fill in your focus behaviors, level framework, and name, then re-run /growth-check.
```

Stop. Do not create any files.

If EXISTS: read `<VAULT_PATH>/growth-plan.md`.

Check frontmatter for optional keys:
- `patterns-file:` — if present, read that file (relative to VAULT_PATH)
- `cpf-scorecard:` — if present, read that file (relative to VAULT_PATH)
- `state-dir:` — directory for `sessions-growth-state.md` (default: `user/growth-plan`)

Check and read existing growth state if present.

---

## Step 3: Write the run report

**Path:** `<VAULT_PATH>/user/private/growth-check/reports/<RUN_DATE>.md`

Check if it already exists. If EXISTS, append with `---` separator. If NEW, write full report.

```markdown
---
date: <RUN_DATE>
period: <PERIOD_START> to <PERIOD_END>
recaps-analyzed: <count>
---

# Growth Check — <RUN_DATE>
Period: <PERIOD_START> → <PERIOD_END> (<N> recaps)

## Recaps Analyzed
- `claude-session-YYYYMMDD.md` — one-line summary per file

## Behaviors Observed

For each focus behavior in growth-plan.md — one subsection with specific quotes or moments from the recaps. If no evidence: "No evidence in this period."

## Behavior Score (this period)

- [Behavior name]: [strong / partial / low / no evidence]

## Leadership Focus (this period)

Specific moments from the recaps using the leadership focus framing from growth-plan.md. If none: "None visible in session recaps for this period."

## Growth Framework Standing (this period)

**Operating at expected level:** [specific behaviors]
**Operating below expected level:** [gaps — direct, no softening]
**Operating above expected level:** [moments above level, or "None observed"]

## Shift vs Previous State
[What improved, regressed, or is unchanged vs previous sessions-growth-state.md.
If first run: "First run — no previous state to compare against."]
```

---

## Step 4: Write the updated sessions-growth-state.md

**Path:** `<VAULT_PATH>/<state-dir>/sessions-growth-state.md`

Always overwritten (Write tool). Single source of truth for current growth standing.

```markdown
---
updated: <RUN_DATE>
recaps-covered-through: <LAST_RECAP>
total-recaps-reviewed: <cumulative count>
---

# Growth State — [Name from growth-plan.md] [Year]

## Focus Behaviors (current standing)

**[Behavior name]:** [strong / partial / low]
[Evidence — 1-2 sentences]

## Leadership Focus (current standing)

[1-3 sentences. What's the trend? Most recent signal?]

## Growth Framework Standing

**[Dimension name]:** [meeting / below / above expected level]
[Evidence]

## Active Patterns

[3-6 bullets. Cross-session patterns only — not one-offs.]

## What Changed Since Last Run

[3-5 specific bullets.]

## Watch Going Forward

[2-3 things to look for in upcoming sessions.]
```

---

## Step 5: Save state

```bash
python3 -c "
import json
from pathlib import Path
state_dir = Path('$HOME/.claude/growth-check')
state_dir.mkdir(parents=True, exist_ok=True)
state_dir.joinpath('state.json').write_text(json.dumps({'last_covered_recap': '<LAST_RECAP>'}))
print('state saved: <LAST_RECAP>')
"
```

---

## Edge cases

- **No recap files found**: write one line to stdout, stop. Do not create files.
- **growth-plan.md missing**: print setup instructions, stop.
- **Optional files missing**: skip, proceed without them.
- **sessions-growth-state.md missing on non-first run**: treat as first run for the delta section.
- **Report already exists for today**: append with `---` separator.
