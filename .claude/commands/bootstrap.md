Pull data from your configured Google Drive folders and Slack channels into your vault inbox.

Run after `/onboard`. Safe to re-run — warns before reprocessing.

---

## Pre-flight

Read `config.yaml`. If it doesn't exist or `DRIVE_FOLDERS` and `SLACK_CHANNELS` are both empty, stop:

> "Nothing to bootstrap. Run `/onboard` first and configure at least one Drive folder or Slack channel."

Read `.bootstrap-state.md` if it exists. If `last_ran` has a date, warn:

> "Bootstrap was already run on [date]. Re-running will re-fetch everything. Continue? [y/N]"

Stop if declined.

---

## Step 1 — Ask about filtering

Ask once:

> "Do you want to filter what gets pulled? (y/N)
> If no, I'll pull everything from your configured sources."

If **no**: set `SLUG_FILTER = ""`, `FILE_TYPES = ["doc", "presentation"]`, skip to Step 2.

If **yes**, ask two follow-up questions (one at a time):

**Slug filter:**
> "Filename slug filter — only pull files whose name contains this string.
> Useful if your Drive folder has mixed content from different projects.
> (e.g. `meeting`, `1on1`, `LokaSpeakers`)
> Press enter to skip (pull everything)."

Set `SLUG_FILTER` to the entered value, or `""` if skipped.

**File types:**
> "Which file types should I pull?
> (1) Docs + meeting notes only (default)
> (2) Docs + Presentations
> (3) Everything (Docs, Presentations, Sheets, PDFs)"

Map the choice:
- 1 → include: `application/vnd.google-apps.document`
- 2 → include: `application/vnd.google-apps.document`, `application/vnd.google-apps.presentation`
- 3 → include: `application/vnd.google-apps.document`, `application/vnd.google-apps.presentation`, `application/vnd.google-apps.spreadsheet`, `application/pdf`

---

## Step 2 — Pull from Google Drive

For each folder URL in `DRIVE_FOLDERS` (split on comma, trim whitespace):

1. Extract the folder ID from the URL (the segment after `/folders/`).
2. Search the folder using the Drive MCP (`mcp__claude_ai_Google_Drive__search_files`):
   - Query: `parentId = '<folder_id>'`
   - Load the tool schema first via ToolSearch if not already loaded.
3. For each file returned:
   - **Skip** if `mimeType` is `video/*` — log it: `skipped (video): <title>`
   - **Skip** if `mimeType` is not in the chosen FILE_TYPES list — log it: `skipped (type: <mimeType>): <title>`
   - **Skip** if SLUG_FILTER is set and the title does not contain SLUG_FILTER — log it: `skipped (filter): <title>`
   - **Process** everything else.

4. For each file to process:
   - Read content via `mcp__claude_ai_Google_Drive__read_file_content` (load schema via ToolSearch if needed).
   - Strip transcript sections: find the first occurrence of `# 📝 Transcript` or `# Transcript` and discard that line and everything after it.
   - Summarize the remaining content: title, date (from filename if available), key points (3-5 bullets), action items if any.
   - Save to `inbox/` as `YYYY-MM-DD-<slug>.md` where slug is a kebab-case version of the title and date comes from `createdTime`.

   Frontmatter:
   ```markdown
   ---
   source: <viewUrl>
   by: "Google Drive"
   date: YYYY-MM-DD
   type: drive-import
   original_title: "<title>"
   ---
   ```

---

## Step 3 — Pull from Slack

For each channel in `SLACK_CHANNELS` (split on comma, trim whitespace, strip `#`):

1. Load `mcp__claude_ai_Slack__slack_read_channel` via ToolSearch if not already loaded.
2. Read up to 100 messages from the channel.
3. If SLUG_FILTER is set, only include messages that contain SLUG_FILTER.
4. Group messages by day. For each day that has messages, save one file to `inbox/`:
   - Filename: `YYYY-MM-DD-slack-<channel>.md`
   - Frontmatter:
     ```markdown
     ---
     source: "slack://<channel>"
     by: "Slack"
     date: YYYY-MM-DD
     type: slack-import
     channel: "#<channel>"
     ---
     ```
   - Content: each message as `**@username** [HH:MM]: message text`

Skip join/leave notifications (messages with no text or only system subtypes).

---

## Step 4 — Write .bootstrap-state.md

```markdown
---
last_ran: YYYY-MM-DD HH:MM
drive_folders: <comma-separated list from config>
slack_channels: <comma-separated list from config>
slug_filter: "<value or empty>"
---

## Last Run Summary

**Drive:** <N> files processed, <M> skipped
  - Processed: <list of titles>
  - Skipped: <list with reasons>

**Slack:** <N> messages across <M> days saved
  - Channels: <list>
```

---

## Step 5 — Report

Print a summary:

```
Bootstrap complete.

Drive:  <N> files → inbox/   (<M> skipped)
Slack:  <N> messages → inbox/

Run /2ndbrain to see current status.
```
