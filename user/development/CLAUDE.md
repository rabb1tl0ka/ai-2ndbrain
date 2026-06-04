# Development Plan — Processing Protocol

This directory tracks {{USER_NAME}}'s progress against their development plan.

## Key References

- **Development plan**: `plan.md` (this directory)
- **Log files**: `YYYYMMDD-log.md` — one file per session/interaction
- **Patterns**: `patterns.md` — distilled cross-session patterns (updated periodically)

---

## What to Log

Log entries come from:
- 1:1 meeting notes
- Slack DMs or channel interactions
- Any interaction that reveals the behaviors in `plan.md` — good or bad

Trigger a new log entry whenever {{USER_NAME}} asks to process new meeting notes or interactions for their development plan.

---

## How to Process a New Entry

When {{USER_NAME}} gives you new input (meeting notes, Slack thread, transcript):

### Step 1 — Read context first

Before writing anything, read:
1. `plan.md` — the key behaviors and development direction
2. Most recent 2-3 log entries in this directory — to track patterns across sessions

### Step 2 — Extract evidence

Go through the input and find specific moments. Quote or paraphrase the actual behavior observed. Don't summarize vaguely.

Look for evidence of the behaviors listed in `plan.md`. For each one ask:
- Was this behavior present? Where specifically?
- Where was the gap between intention and action?
- What did the other person's response reveal?

Look for both what went well and where it fell short. Both matter.

### Step 3 — Write the log entry

**File name:** `YYYYMMDD-log.md`
**Date:** the date of the interaction, not the date of logging

Use this template:

```markdown
---
date: YYYY-MM-DD
interaction: [1:1 with Name | Slack thread | Team meeting | Other]
person: [Name or N/A]
---

# YYYY-MM-DD — [Interaction type]

**Context:** [1-2 sentences. What was the state going in?]

## What I did well
[Specific moments. Quote or paraphrase actual behavior. Link to the behavior from plan.md.]

## Where I fell short
[Specific moments. What did I do vs what the plan calls for? Be direct — this section has no value if it's soft.]

## Behavior check
[For each key behavior in plan.md: strong / partial / low / n/a]
- {{BEHAVIOR_1}}: 
- {{BEHAVIOR_2}}: 
- {{BEHAVIOR_3}}: 

## What this reveals
[1-2 sentences. What does this interaction show about where {{USER_NAME}} actually is right now — not where they intend to be?]

## Watch going forward
[1-3 specific things to observe in the next interaction with this person or in this context.]
```

### Step 4 — Update patterns.md

After writing the log entry, check `patterns.md`. If the new entry reveals a pattern that's emerging or shifting, update it. Don't create a new pattern for every session — only update when something is genuinely changing or compounding.

---

## File Naming

```
YYYYMMDD-log.md     — individual session log
patterns.md         — distilled cross-session patterns
plan.md             — development plan (do not edit casually)
CLAUDE.md           — this file
```

---

## What NOT to do

- Don't write generic reflections. Every line should be evidence-based.
- Don't soften the "where I fell short" section. Raw and honest is the point.
- Don't create a log entry for every minor interaction — only when there's meaningful behavior to assess.
- Don't rewrite history. If something wasn't observed, say it's unknown or TBD.
