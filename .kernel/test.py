#!/usr/bin/env python3
"""
2ndbrain template test suite.

Tests the mechanics that /onboard, /bootstrap, and /2ndbrain depend on.
Integration tests (real Drive + Slack) require --integration flag.

Usage:
    python3 .kernel/test.py               # unit tests only
    python3 .kernel/test.py --integration  # unit + integration tests
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"
SKIP = "\033[33m-\033[0m"

# Test Drive folder and Slack channel
TEST_DRIVE_FOLDER = "https://drive.google.com/drive/folders/14GDHf8Se8M7NPrnuY91C7eufcJgxTs7i"
TEST_DRIVE_FOLDER_ID = "14GDHf8Se8M7NPrnuY91C7eufcJgxTs7i"
TEST_SLACK_CHANNEL = "#bruno-test2"
TEST_SLACK_CHANNEL_ID = "C0B94DNRCN4"

passed = 0
failed = 0
skipped = 0


def ok(name):
    global passed
    passed += 1
    print(f"  {PASS}  {name}")


def fail(name, reason=""):
    global failed
    failed += 1
    msg = f"  {FAIL}  {name}"
    if reason:
        msg += f"\n       {reason}"
    print(msg)


def skip(name, reason=""):
    global skipped
    skipped += 1
    msg = f"  {SKIP}  {name} (skipped)"
    if reason:
        msg += f" — {reason}"
    print(msg)


def section(title):
    print(f"\n{title}")
    print("-" * len(title))


# ─── Unit Tests ───────────────────────────────────────────────────────────────

def test_repo_structure():
    section("Repo structure")
    repo = Path(__file__).parent.parent

    dirs = [
        "inbox", "archive", "daily", "learning", "notes",
        "sources", "templates", "user",
        ".claude/commands", ".kernel",
    ]
    for d in dirs:
        if (repo / d).is_dir():
            ok(f"{d}/ exists")
        else:
            fail(f"{d}/ exists")

    files = [
        "CLAUDE.md", "README.md", "config.example.yaml", ".gitignore",
        ".claude/commands/onboard.md",
        ".claude/commands/bootstrap.md",
        ".claude/commands/2ndbrain.md",
        ".claude/commands/recap.md",
        ".claude/commands/growth-check.md",
        ".kernel/roadmap/README.md",
        ".kernel/recap/extract_sessions.py",
        ".kernel/growth-check/growth-plan-template.md",
    ]
    for f in files:
        if (repo / f).is_file():
            ok(f"{f} exists")
        else:
            fail(f"{f} exists")

    gone = ["setup.sh", "brain.config.example.yaml", "2ndbrain-vault", "claude-skills"]
    for g in gone:
        if not (repo / g).exists():
            ok(f"{g} removed")
        else:
            fail(f"{g} removed", f"{g} still present")


def test_gitignore():
    section("Gitignore")
    repo = Path(__file__).parent.parent
    content = (repo / ".gitignore").read_text()

    if "config.yaml" in content:
        ok("config.yaml is gitignored")
    else:
        fail("config.yaml is gitignored")

    if "brain.config.yaml" not in content:
        ok("brain.config.yaml removed from gitignore")
    else:
        fail("brain.config.yaml removed from gitignore", "old entry still present")


def test_config_example():
    section("config.example.yaml")
    repo = Path(__file__).parent.parent
    content = (repo / "config.example.yaml").read_text()

    required_fields = ["USER_NAME", "USER_HANDLE", "USER_ROLE", "USER_COMPANY",
                       "USER_CONTEXT", "VAULT_FOCUS", "DRIVE_FOLDERS", "SLACK_CHANNELS"]
    for field in required_fields:
        if field in content:
            ok(f"{field} present")
        else:
            fail(f"{field} present")

    if "VAULT_PATH" not in content:
        ok("VAULT_PATH removed (vault is the repo)")
    else:
        fail("VAULT_PATH removed", "VAULT_PATH still present in config.example.yaml")


def test_placeholder_replacement():
    section("Placeholder replacement (synthetic vault)")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # Create synthetic vault files with placeholders
        (tmp / "CLAUDE.md").write_text(
            "# {{USER_NAME}}'s 2nd Brain\nFocus: {{VAULT_FOCUS}}\nRole: {{USER_ROLE}}\n"
        )
        (tmp / "user").mkdir()
        (tmp / "user" / "user.md").write_text(
            "Name: {{USER_NAME}}\nCompany: {{USER_COMPANY}}\n"
        )
        (tmp / "notes").mkdir()
        (tmp / "notes" / "note.md").write_text("No placeholders here.\n")

        config = {
            "USER_NAME": "Test User",
            "USER_HANDLE": "@testuser",
            "USER_ROLE": "Engineer",
            "USER_COMPANY": "ACME",
            "USER_CONTEXT": "I build things.",
            "VAULT_FOCUS": "work at ACME",
        }

        # Run the same sed commands /onboard uses
        for key, value in config.items():
            placeholder = f"{{{{{key}}}}}"
            result = subprocess.run(
                ["bash", "-c",
                 f"find {tmp} -name '*.md' -print0 | xargs -0 sed -i 's|{placeholder}|{value}|g'"],
                capture_output=True
            )
            if result.returncode != 0:
                fail(f"sed replacement for {key}", result.stderr.decode())
                continue

        # Verify replacements
        claude_md = (tmp / "CLAUDE.md").read_text()
        if "Test User" in claude_md and "{{USER_NAME}}" not in claude_md:
            ok("USER_NAME replaced in CLAUDE.md")
        else:
            fail("USER_NAME replaced in CLAUDE.md", repr(claude_md))

        if "work at ACME" in claude_md and "{{VAULT_FOCUS}}" not in claude_md:
            ok("VAULT_FOCUS replaced in CLAUDE.md")
        else:
            fail("VAULT_FOCUS replaced in CLAUDE.md")

        user_md = (tmp / "user" / "user.md").read_text()
        if "Test User" in user_md and "ACME" in user_md:
            ok("Placeholders replaced in nested file")
        else:
            fail("Placeholders replaced in nested file")

        note_md = (tmp / "notes" / "note.md").read_text()
        if note_md == "No placeholders here.\n":
            ok("Files without placeholders untouched")
        else:
            fail("Files without placeholders untouched")

        # Verify no placeholders remain
        result = subprocess.run(
            ["grep", "-r", "{{", str(tmp), "--include=*.md"],
            capture_output=True
        )
        if result.returncode != 0:  # grep returns 1 when no matches
            ok("No placeholders remain after replacement")
        else:
            fail("No placeholders remain after replacement",
                 f"Still found: {result.stdout.decode().strip()}")


def test_config_parsing():
    section("Config YAML parsing")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        config_content = '''USER_NAME: "Alice Smith"
USER_HANDLE: "@alice"
USER_ROLE: "Data Scientist"
USER_COMPANY: "Widgets Inc"
USER_CONTEXT: "I work on ML pipelines."
VAULT_FOCUS: "work at Widgets"
DRIVE_FOLDERS: "https://drive.google.com/drive/folders/abc123, https://drive.google.com/drive/folders/xyz456"
SLACK_CHANNELS: "#data-team, #ml-research"
'''
        (tmp / "config.yaml").write_text(config_content)

        # Parse using the same approach /onboard uses: line-by-line key: "value"
        parsed = {}
        for line in config_content.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            parsed[key] = value

        if parsed.get("USER_NAME") == "Alice Smith":
            ok("USER_NAME parsed correctly")
        else:
            fail("USER_NAME parsed correctly", repr(parsed.get("USER_NAME")))

        folders = [f.strip() for f in parsed.get("DRIVE_FOLDERS", "").split(",")]
        if len(folders) == 2 and "abc123" in folders[0]:
            ok("DRIVE_FOLDERS split into 2 folders")
        else:
            fail("DRIVE_FOLDERS split into 2 folders", repr(folders))

        channels = [c.strip() for c in parsed.get("SLACK_CHANNELS", "").split(",")]
        if len(channels) == 2 and channels[0] == "#data-team":
            ok("SLACK_CHANNELS split into 2 channels")
        else:
            fail("SLACK_CHANNELS split into 2 channels", repr(channels))


def test_bootstrap_filter_logic():
    section("Bootstrap filter logic (synthetic)")

    # Synthetic file list matching what Drive returns
    files = [
        {"title": "Copy of LokaSpeakers V2 - 2026/06/03 - Notes by Gemini",
         "mimeType": "application/vnd.google-apps.document"},
        {"title": "Copy of Loka Labs - siRNA Silencing ML Prediction Challenge",
         "mimeType": "application/vnd.google-apps.presentation"},
        {"title": "Copy of LokaSpeakers V2 - 2026/06/03 - Recording",
         "mimeType": "video/mp4"},
        {"title": "Copy of siRNA Silencing.drawio",
         "mimeType": "application/vnd.jgraph.mxfile"},
    ]

    SUPPORTED_TYPES = {
        "docs_only": ["application/vnd.google-apps.document"],
        "docs_and_presentations": [
            "application/vnd.google-apps.document",
            "application/vnd.google-apps.presentation",
        ],
        "everything": [
            "application/vnd.google-apps.document",
            "application/vnd.google-apps.presentation",
            "application/vnd.google-apps.spreadsheet",
            "application/pdf",
        ],
    }
    VIDEO_TYPES = ["video/"]

    def apply_filters(files, slug="", file_type_key="docs_and_presentations"):
        allowed_types = SUPPORTED_TYPES[file_type_key]
        results = {"process": [], "skip_video": [], "skip_type": [], "skip_slug": []}
        for f in files:
            mime = f["mimeType"]
            title = f["title"]
            if any(mime.startswith(v) for v in VIDEO_TYPES):
                results["skip_video"].append(title)
            elif mime not in allowed_types:
                results["skip_type"].append(title)
            elif slug and slug.lower() not in title.lower():
                results["skip_slug"].append(title)
            else:
                results["process"].append(title)
        return results

    # Test 1: No filter, docs+presentations
    r = apply_filters(files, slug="", file_type_key="docs_and_presentations")
    if len(r["process"]) == 2 and len(r["skip_video"]) == 1 and len(r["skip_type"]) == 1:
        ok("No filter: 2 processed, 1 video skipped, 1 unsupported type skipped")
    else:
        fail("No filter", repr(r))

    # Test 2: Slug filter "LokaSpeakers" — only the Notes doc matches
    r = apply_filters(files, slug="LokaSpeakers", file_type_key="docs_and_presentations")
    if len(r["process"]) == 1 and "Notes by Gemini" in r["process"][0]:
        ok("Slug filter 'LokaSpeakers': only meeting notes doc matches")
    else:
        fail("Slug filter 'LokaSpeakers'", repr(r))

    # Test 3: Slug filter "siRNA" — only the Slides matches (video excluded, drawio excluded)
    r = apply_filters(files, slug="siRNA", file_type_key="docs_and_presentations")
    if len(r["process"]) == 1 and "siRNA" in r["process"][0]:
        ok("Slug filter 'siRNA': only presentation matches")
    else:
        fail("Slug filter 'siRNA'", repr(r))

    # Test 4: Docs only — only the Google Doc matches
    r = apply_filters(files, slug="", file_type_key="docs_only")
    if len(r["process"]) == 1 and "Notes by Gemini" in r["process"][0]:
        ok("File type 'docs_only': only Google Doc matches")
    else:
        fail("File type 'docs_only'", repr(r))

    # Test 5: Video skip is checked before type and slug filters
    r = apply_filters(files, slug="Recording", file_type_key="everything")
    if "Recording" in str(r["skip_video"]) and "Recording" not in str(r["process"]):
        ok("Video skip takes priority over slug and type filters")
    else:
        fail("Video skip priority", repr(r))


def test_folder_id_extraction():
    section("Drive folder ID extraction")
    test_cases = [
        ("https://drive.google.com/drive/folders/14GDHf8Se8M7NPrnuY91C7eufcJgxTs7i?usp=drive_link",
         "14GDHf8Se8M7NPrnuY91C7eufcJgxTs7i"),
        ("https://drive.google.com/drive/folders/abc123def456",
         "abc123def456"),
        ("https://drive.google.com/drive/folders/xyz?usp=sharing",
         "xyz"),
    ]

    def extract_folder_id(url):
        url = url.split("?")[0]
        parts = url.rstrip("/").split("/")
        idx = parts.index("folders")
        return parts[idx + 1]

    for url, expected in test_cases:
        got = extract_folder_id(url)
        if got == expected:
            ok(f"Folder ID extracted: {expected}")
        else:
            fail(f"Folder ID extracted: {expected}", f"got {got!r}")


def test_bootstrap_state_writing():
    section("Bootstrap state file")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        state_path = tmp / ".bootstrap-state.md"

        state = {
            "last_ran": "2026-06-04 14:30",
            "drive_folders": TEST_DRIVE_FOLDER,
            "slack_channels": TEST_SLACK_CHANNEL,
            "slug_filter": "LokaSpeakers",
            "drive_processed": 1,
            "drive_skipped": 3,
            "slack_messages": 3,
        }

        state_path.write_text(f"""---
last_ran: {state["last_ran"]}
drive_folders: {state["drive_folders"]}
slack_channels: {state["slack_channels"]}
slug_filter: "{state["slug_filter"]}"
---

## Last Run Summary

**Drive:** {state["drive_processed"]} files processed, {state["drive_skipped"]} skipped
**Slack:** {state["slack_messages"]} messages across 1 day saved
""")

        content = state_path.read_text()
        if "last_ran: 2026-06-04" in content:
            ok("last_ran written to state file")
        else:
            fail("last_ran written to state file")

        if "LokaSpeakers" in content:
            ok("slug_filter written to state file")
        else:
            fail("slug_filter written to state file")

        # Simulate reading last_ran for pre-flight check
        last_ran = None
        for line in content.splitlines():
            if line.startswith("last_ran:"):
                last_ran = line.split(":", 1)[1].strip()
                break

        if last_ran == "2026-06-04 14:30":
            ok("last_ran readable for pre-flight check")
        else:
            fail("last_ran readable", repr(last_ran))


def test_inbox_file_format():
    section("Inbox file format")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        inbox = tmp / "inbox"
        inbox.mkdir()

        # Simulate what /bootstrap writes for a Drive file
        drive_file = inbox / "2026-06-03-lokaspeakers-v2-notes-by-gemini.md"
        drive_file.write_text("""---
source: https://docs.google.com/document/d/1v_I9I_h0o3v74acOyrx_C7dyKagCsNFxDURtMZ-qaSA/edit
by: "Google Drive"
date: 2026-06-03
type: drive-import
original_title: "Copy of LokaSpeakers V2 - 2026/06/03 16:14 WEST - Notes by Gemini"
---

## Summary

Session focused on public speaking techniques.

## Key Points

- Performance anxiety management techniques discussed
- Feedback on posture and filler words
- Module 2 completed successfully

## Action Items

- [Riste Mingov] Watch recording to identify areas for improvement
- [Bruno Coelho] Answer design question about Claude slide exports
""")

        # Simulate what /bootstrap writes for a Slack channel
        slack_file = inbox / "2026-06-04-slack-bruno-test2.md"
        slack_file.write_text("""---
source: "slack://bruno-test2"
by: "Slack"
date: 2026-06-04
type: slack-import
channel: "#bruno-test2"
---

**@Bruno Coelho** [14:16]: Test message

**@Bruno Coelho** [14:16]: and another one

**@Bruno Coelho** [14:16]:
""")

        # Verify Drive file
        content = drive_file.read_text()
        if "source:" in content and "by: \"Google Drive\"" in content and "type: drive-import" in content:
            ok("Drive inbox file has correct frontmatter")
        else:
            fail("Drive inbox file frontmatter", repr(content[:200]))

        if "## Summary" in content and "## Action Items" in content:
            ok("Drive inbox file has summary structure")
        else:
            fail("Drive inbox file structure")

        # Verify Slack file
        content = slack_file.read_text()
        if "source: \"slack://" in content and "type: slack-import" in content:
            ok("Slack inbox file has correct frontmatter")
        else:
            fail("Slack inbox file frontmatter")

        if "@Bruno Coelho" in content:
            ok("Slack messages formatted with @username")
        else:
            fail("Slack message format")

        # Count inbox files
        md_files = list(inbox.glob("*.md"))
        if len(md_files) == 2:
            ok("Inbox file count matches expected (2)")
        else:
            fail("Inbox file count", f"expected 2, got {len(md_files)}")


# ─── Integration Tests ────────────────────────────────────────────────────────

def test_integration_drive():
    """Test against real Drive folder using MCP — run via Claude, not directly."""
    section("Drive integration (real folder)")
    print(f"  Folder ID: {TEST_DRIVE_FOLDER_ID}")
    print()
    print("  Expected results:")
    print("  ✓ 4 files found in folder")
    print("  ✓ 1 Google Doc (LokaSpeakers Notes by Gemini) — should be processed")
    print("  ✓ 1 Google Slides (siRNA Challenge) — processed if type includes presentations")
    print("  ✓ 1 mp4 video (LokaSpeakers Recording) — should be skipped")
    print("  ✓ 1 .drawio file (siRNA Silencing) — should be skipped (unsupported type)")
    print()
    print("  Slug filter tests:")
    print("  → filter='LokaSpeakers': Doc matches, Slides excluded, video skipped")
    print("  → filter='siRNA': Slides matches, Doc excluded, drawio skipped")
    print("  → no filter, docs+presentations: Doc + Slides processed, video+drawio skipped")
    print()
    print("  This test must be validated by running /bootstrap with the test folder.")
    print(f"  Config: DRIVE_FOLDERS: \"{TEST_DRIVE_FOLDER}\"")
    skip("Drive integration", "requires Claude to run /bootstrap — validate manually")


def test_integration_slack():
    """Test against real Slack channel."""
    section("Slack integration (real channel)")
    print(f"  Channel: {TEST_SLACK_CHANNEL} ({TEST_SLACK_CHANNEL_ID})")
    print()
    print("  Expected results:")
    print("  ✓ 3 messages from Bruno Coelho (join notification excluded)")
    print("  ✓ Messages saved to inbox/2026-06-04-slack-bruno-test2.md")
    print("  ✓ No slug filter: all 3 messages included")
    print()
    skip("Slack integration", "requires Claude to run /bootstrap — validate manually")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="2ndbrain test suite")
    parser.add_argument("--integration", action="store_true",
                        help="Run integration tests (shows expected results for manual validation)")
    args = parser.parse_args()

    print("2ndbrain Test Suite")
    print("=" * 40)

    test_repo_structure()
    test_gitignore()
    test_config_example()
    test_placeholder_replacement()
    test_config_parsing()
    test_bootstrap_filter_logic()
    test_folder_id_extraction()
    test_bootstrap_state_writing()
    test_inbox_file_format()

    if args.integration:
        test_integration_drive()
        test_integration_slack()

    print()
    print("=" * 40)
    total = passed + failed + skipped
    print(f"Results: {passed}/{total} passed", end="")
    if skipped:
        print(f", {skipped} skipped", end="")
    if failed:
        print(f", {failed} FAILED", end="")
    print()

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
