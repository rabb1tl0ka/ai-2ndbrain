Show the current status of this 2nd brain — what's set up, what's missing, what to do next.

Do not ask any questions. Do not run any setup. Just orient and point.

---

## Step 1 — Detect state

**Onboard check:**
Read `config.yaml`. It's complete if:
- The file exists
- None of the core values are still defaults (e.g. `"Your Name"`, `"Your Role"`, `"Your Company"`)

**Placeholder check:**
If config.yaml exists, check for unreplaced placeholders in vault .md files:
```bash
grep -r "{{" . --include="*.md" --exclude-dir=.kernel --exclude-dir=.git -l 2>/dev/null | head -10
```

**Bootstrap check:**
Read `.bootstrap-state.md`. It's complete if `last_ran` has a real date.

**Inbox count:**
```bash
find inbox/ -name "*.md" ! -name ".gitkeep" 2>/dev/null | wc -l
```

**Integration check:**
Read `DRIVE_FOLDERS` and `SLACK_CHANNELS` from `config.yaml`. Non-empty = configured.

---

## Step 2 — Print status

### State A — Not onboarded

```
2nd Brain — Status

  ✗  Not onboarded

Run /onboard to get started.
```

### State B — Onboarded, not bootstrapped

```
2nd Brain — Status

  ✓  Onboarded
       Owner:   <USER_NAME> (<USER_ROLE> at <USER_COMPANY>)
       Focus:   <VAULT_FOCUS>
  [✓  Drive:   <DRIVE_FOLDERS>  |  ⚠  Drive not configured]
  [✓  Slack:   <SLACK_CHANNELS> |  ⚠  Slack not configured]
  ✗  Bootstrap not run

[If Drive or Slack configured:]
Next: run /bootstrap to pull data into your inbox.

[If neither configured:]
Next: edit config.yaml to add DRIVE_FOLDERS and/or SLACK_CHANNELS, then run /bootstrap.
```

### State C — Fully set up

```
2nd Brain — Status

  ✓  Onboarded
       Owner:   <USER_NAME> (<USER_ROLE> at <USER_COMPANY>)
       Focus:   <VAULT_FOCUS>
  ✓  Drive:   <DRIVE_FOLDERS>
  ✓  Slack:   <SLACK_CHANNELS>
  ✓  Bootstrapped — last ran <last_ran>

  Inbox:  <N> items

[If unreplaced placeholders found:]
  ⚠  Unreplaced placeholders found in:
       <list of files>
     Re-run /onboard to fix them.
```

---

## Step 3 — Print command reference

Always print this after the status block:

```
Commands:
  /onboard    — initial setup (config, placeholders, integrations)
  /bootstrap  — pull Drive + Slack data into inbox
  /recap      — summarize today's Claude sessions
  /2ndbrain   — this screen
```
