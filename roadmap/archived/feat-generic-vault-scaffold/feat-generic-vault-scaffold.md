---
status: done
priority: high
owner: "@rabb1tl0ka"
---

# Feature Spec: Generic Vault Scaffold

## One-Line Overview
A fully scaffolded, placeholder-driven 2nd brain vault that anyone can clone and personalize by replacing `{{TAGS}}` to get a Claude-powered knowledge system working in minutes.

## Goal
Build the `2ndbrain-vault/` directory into a complete, ready-to-use vault template. Every directory is created, every file has real content with `{{PLACEHOLDER}}` tags where personal context belongs, and the CLAUDE.md instructions are fully generic. Someone clones the repo, runs a find-and-replace on their placeholders, and has a working 2nd brain.

## Expected advantages / benefits

- Zero friction onboarding — clone + replace tags = working vault
- CLAUDE.md is self-documenting: the instructions tell Claude how the vault works, so the user doesn't have to explain it every session
- Structure is opinionated enough to be useful but not so deep it's overwhelming (minimal project structure, flat learning/)
- Relationship tracking, development plan, and goals are first-class — the parts of a 2nd brain that make the biggest difference
- Target audience (Loka SWEs, PMs) can immediately see themselves in the structure

## Downsides / risks

- Placeholder tags require a manual find-and-replace step — easy to miss one
- Example files (`_example-person/`, `project_{ID}/`) need to be deleted after setup, which adds friction if the user forgets
- Generic development protocol loses CPF/level-specific nuance from the source (intentional tradeoff)

## Context

### Current flow
1. User clones repo — gets a `2ndbrain-vault/` with only `CLAUDE.md` (partially generified, has leftover Loka/TPM refs)
2. User has to figure out the directory structure themselves
3. No templates, no user profile, no example relationship or project

### Proposed flow
1. User clones repo — gets fully scaffolded `2ndbrain-vault/`
2. User runs: `grep -r "{{" 2ndbrain-vault/` to see all placeholders
3. User replaces each tag (name, role, company, context)
4. User deletes `_example-person/` and `project_{ID}/` after copying them as starting points
5. User opens vault in Obsidian (or any markdown editor) and starts a Claude Code session — it works immediately

### Files involved

```
2ndbrain-vault/
├── CLAUDE.md                                ← generified (fix typo, strip Loka/TPM refs)
├── inbox/.gitkeep
├── archive/.gitkeep
├── sources/.gitkeep
├── notes/.gitkeep
├── learning/.gitkeep
├── daily/.gitkeep
├── projects/
│   └── _example-project/
│       ├── _example-project.md              ← project spec template
│       ├── meeting-notes/.gitkeep
│       ├── notes/.gitkeep
│       └── team/.gitkeep
├── user/
│   ├── user.md                              ← who you are: role, context, work style
│   ├── goals/
│   │   └── goals.md
│   ├── challenges/
│   │   └── challenges.md
│   ├── development/
│   │   ├── CLAUDE.md                        ← protocol for processing development inputs
│   │   └── plan.md                          ← development/growth plan template
│   └── relationships/
│       └── _example-person/
│           ├── profile.md
│           ├── meetings.md
│           ├── log.md
│           └── tasks.md
└── templates/
    ├── daily.md
    ├── inbox.md
    ├── project.md
    ├── source.md
    ├── goal.md
    └── relationship-profile.md
```

**Branch:** `feat/generic-vault-scaffold`

---

## Design

### Placeholder system

| Tag | Meaning | Example |
|-----|---------|---------|
| `{{USER_NAME}}` | Full name | Bruno Coelho |
| `{{USER_HANDLE}}` | @handle | @rabb1tl0ka |
| `{{USER_ROLE}}` | Job title | Senior Software Engineer |
| `{{USER_COMPANY}}` | Company name | Loka |
| `{{USER_CONTEXT}}` | 1-2 sentences describing work context | AI development consultancy focused on... |
| `{{VAULT_FOCUS}}` | What this vault is for | work at {{USER_COMPANY}} |

### CLAUDE.md changes (2ndbrain-vault/CLAUDE.md)

1. Fix typo: `{{USER_NAME}` → `{{USER_NAME}}`
2. Line 5: Remove "at Loka" — keep generic
3. Vault structure table: add `development/` and `challenges/` rows
4. Key Strategic Documents section: replace hardcoded TPM/Loka paths with `{{KEY_DOC_N}}` placeholder block
5. Relationship & Team Tracking section: replace `tpm/tpm-team/` with `projects/{ID}/team/`, remove `user/Zach/` reference

### user/user.md
Generic profile file: role, work style, relationships intent, observation lens. Fully `{{PLACEHOLDER}}`-driven.

### user/development/CLAUDE.md
Ported from `loka2026/user/growth-plan/2026/CLAUDE.md`, stripped of:
- Loka CPF / M1/M2 level references
- TPM-specific behaviors
- Direct mentions of Bruno or Zach

Kept:
- 5-step processing protocol (read context → extract evidence → write log → update patterns → update scorecard)
- The 5 coaching behaviors (check before acting, ask before tell, build from their map, stay in exploration, close the loop)
- Log entry template structure
- What NOT to do rules

### user/development/plan.md
Template for the user's growth plan. Sections: Direction, What I'm Building, Key Behaviors, Learning Investments. Fully placeholder-driven, with inline comments showing what Bruno's version looked like as examples.

### _example-person/ relationship folder
All 4 files pre-filled with generic placeholder content + inline instructions on what goes where. Top of each file has a comment: `<!-- Copy this folder, rename to the person's name, delete this comment -->`

### projects/project_{ID}/
Minimal: spec file + 3 subdirs. The spec file uses the project template with `{{PROJECT_NAME}}`, `{{PROJECT_ID}}`, `{{CLIENT_OR_CONTEXT}}` placeholders.

---

## Changes required

| File | Change |
|------|--------|
| `2ndbrain-vault/CLAUDE.md` | Fix typo, strip Loka/TPM refs, update structure table, genericize Key Docs section |
| `2ndbrain-vault/inbox/.gitkeep` | Create |
| `2ndbrain-vault/archive/.gitkeep` | Create |
| `2ndbrain-vault/sources/.gitkeep` | Create |
| `2ndbrain-vault/notes/.gitkeep` | Create |
| `2ndbrain-vault/learning/.gitkeep` | Create |
| `2ndbrain-vault/daily/.gitkeep` | Create |
| `2ndbrain-vault/projects/_example-project/_example-project.md` | Create |
| `2ndbrain-vault/projects/_example-project/meeting-notes/.gitkeep` | Create |
| `2ndbrain-vault/projects/_example-project/notes/.gitkeep` | Create |
| `2ndbrain-vault/projects/_example-project/team/.gitkeep` | Create |
| `2ndbrain-vault/user/user.md` | Create |
| `2ndbrain-vault/user/goals/goals.md` | Create |
| `2ndbrain-vault/user/challenges/challenges.md` | Create |
| `2ndbrain-vault/user/development/CLAUDE.md` | Create |
| `2ndbrain-vault/user/development/plan.md` | Create |
| `2ndbrain-vault/user/relationships/_example-person/profile.md` | Create |
| `2ndbrain-vault/user/relationships/_example-person/meetings.md` | Create |
| `2ndbrain-vault/user/relationships/_example-person/log.md` | Create |
| `2ndbrain-vault/user/relationships/_example-person/tasks.md` | Create |
| `2ndbrain-vault/templates/daily.md` | Create |
| `2ndbrain-vault/templates/inbox.md` | Create |
| `2ndbrain-vault/templates/project.md` | Create |
| `2ndbrain-vault/templates/source.md` | Create |
| `2ndbrain-vault/templates/goal.md` | Create |
| `2ndbrain-vault/templates/relationship-profile.md` | Create |
| `brain.config.yaml` | Create — placeholder key/value config for setup |
| `setup.sh` | Create — reads brain.config.yaml, replaces tags across vault |
| `roadmap/README.md` | Add row to current roadmap table |

---

## Test plan

1. `grep -r "Bruno\|Loka\|TPM\|Zach\|tpm/" 2ndbrain-vault/` → zero matches
2. `grep -r "{{USER_NAME}" 2ndbrain-vault/` → fix typo, all instances use `{{USER_NAME}}`  
3. `find 2ndbrain-vault/ -type d | sort` → all expected dirs present
4. `find 2ndbrain-vault/ -name "*.md" | sort` → all expected files present
5. All 4 `_example-person/` files exist and contain meaningful placeholder content
6. `user/development/CLAUDE.md` contains the 5 coaching behaviors and 5-step protocol

---

## Open questions

~~1. Should the main repo README document the setup flow (clone → edit brain.config.yaml → run setup.sh)?~~ Done — `README.md` created at repo root.
