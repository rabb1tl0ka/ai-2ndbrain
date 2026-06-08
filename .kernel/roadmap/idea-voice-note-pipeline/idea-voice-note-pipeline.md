---
status: todo
priority: medium
owner: ""
---

# Idea: Voice Note Pipeline

## One-Line Overview

Record a voice note on Android, have it automatically transcribed via Groq Whisper, and get a daily summary with connections flagged against your existing notes — all landing in `inbox/voice/` without manual steps.

## What's the idea

Right now voice notes die on your phone. This pipeline closes that gap:

1. **Capture**: record audio on Android using the Google Drive app (2 taps — open app → `+` → record). File saves directly to a dedicated Drive folder (e.g. `voice-notes-inbox/`). Syncs automatically when online.
2. **Transcribe**: a scheduled agent (daily, via `/schedule`) polls the Drive folder for new audio files and sends each one to the Groq Whisper API for transcription.
3. **Summarize + connect**: Claude summarizes the transcript and scans all of `notes/` for relevant connections — existing notes, themes, or open questions that relate to what you said.
4. **Output**: one file per voice note in `inbox/voice/`, containing the full transcript, the summary, and any flagged connections. You review when you want, decide what to keep or promote.

Manual trigger also available for when you don't want to wait for the daily run.

## Expected advantages / benefits

- Voice notes stop dying on your phone — they surface in your 2nd brain automatically
- Groq Whisper is fast and has a free tier — no meaningful cost to get started
- Connections to existing notes surface things you'd miss reading the transcript alone
- `inbox/voice/` keeps it visible without requiring immediate action — you review on your own schedule
- Works offline for capture (records locally, syncs to Drive when signal is available)

## Downsides / risks

- Groq API key required — small signup friction before anything can be built
- Drive audio recording is 2 taps, not zero — not as frictionless as a dedicated voice app
- Daily schedule means up to 24h lag between recording and the processed note appearing
- Connections quality depends on how much is in `notes/` — sparse vault = sparse connections
- Drive folder polling needs to track which files have already been processed (avoid re-transcribing)

## What's been tried already

Shaped in conversation on 2026-06-07. Related idea `idea-whisper-video-transcription` covers Whisper for meeting recordings in `/bootstrap` — different scope, but the Groq API approach here could inform that one too.

## Open questions

1. ~~How does the agent track which files have already been processed?~~ **Closed**: move processed files from `voice-notes-inbox/` to `voice-notes-processed/` on Drive after transcription. The folder is the state — no manifest needed.
2. What's the Drive folder name/path — does the user configure this in `config.yaml`?
3. What does "connections" output look like — a bullet list of note titles + a one-line reason each is relevant?
4. After reviewing in `inbox/voice/`, where does a voice note go if promoted? `notes/`? `archive/`?
