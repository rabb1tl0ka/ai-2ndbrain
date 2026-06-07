---
status: todo
priority: medium
owner: ""
---

# Idea: Automated Idea-to-Execution Pipeline

## One-Line Overview

Wire the 2nd brain inbox into a classify → plan → approve pipeline so a raw idea can become a scoped project plan with only ~2 minutes of human involvement.

## What's the idea

Right now ideas land in inbox and sit there. This pipeline would:

1. **Classify** — a scheduled agent reads unprocessed inbox notes and labels each one (`project`, `task`, `content`, `reference`, `noise`) by writing a `type:` field into the frontmatter
2. **Plan** — for notes labeled `type: project`, a planner agent researches the idea (web search, checks existing tools), then writes a structured plan to `projects/pending/{slug}/plan.md`
3. **Approve** — a `/review-plans` command lists all pending plans so the user can approve, cut, or modify. On approval, the plan moves to `projects/active/`

The user's only touch point is the approval step. Everything before and after is automated.

## Expected advantages / benefits

- Inbox stops being a graveyard — ideas actually get processed
- Forces a research + scoping step before any building starts
- The approval checkpoint keeps the human in the loop without requiring them to drive
- Natural extension of the existing inbox-first pattern — no new capture behavior needed
- Sets up the right foundation if execution automation is added later

## Downsides / risks

- Classification accuracy: a bad classifier routes things wrong and creates noise instead of reducing it
- Planner agents can produce generic, shallow plans without strong prompting — needs good prompt engineering
- Scope creep: easy to keep adding to this instead of shipping the simple version

## What's been tried already

Scoped in conversation on 2026-06-07. Left half (classify → plan → approve) deemed feasible now. Right half (approve → autonomous build → ship) deferred — too many environment and guardrail questions to solve upfront.

The inbox note `inbox/idea-automated-idea-to-execution-pipeline.md` has the original raw capture.

## Open questions

1. What triggers the classifier — cron (nightly) or a manual `/classify-inbox` command?
2. What's the rule for `project` vs `task`? (Proposed: anything needing more than one work session)
3. Where do approved plans live — inside this repo or a separate projects repo?
4. How does the user get notified when a new plan is ready to review?
