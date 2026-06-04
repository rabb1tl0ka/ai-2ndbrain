---
status: todo
priority: medium
owner: ""
---

# Idea: Whisper Integration for Video Transcription in /bootstrap

## One-Line Overview
Ship OpenAI Whisper alongside /bootstrap so users can opt in to transcribing video files before summarizing them, instead of silently skipping them.

## What's the idea

`/bootstrap` currently skips video files (mp4, mov, avi, etc.) in Drive folders and logs a warning. Most Drive folders from Google Meet contain a recording alongside the Gemini notes doc — the recording gets dropped while the notes get imported.

Whisper (local or API) would let /bootstrap transcribe videos into text, then summarize them the same way it handles Docs.

### Implementation options

**Option A — Local Whisper**
- Install via `pip install openai-whisper` or Faster-Whisper
- Runs offline, no API cost
- Slow on CPU (~4-10x real-time); fast on GPU
- Good for users with M-series Mac or Nvidia GPU

**Option B — Whisper API (OpenAI)**
- Requires `OPENAI_API_KEY` in config.yaml
- Fast, no local GPU needed
- Costs ~$0.006/min of audio
- 25MB file size limit per request (need chunking for long recordings)

### User flow in /bootstrap

After the file type filter step, add an opt-in prompt:

> "I found N video file(s). Transcribe them with Whisper? (requires OpenAI key or local Whisper install)
> (y) Yes  (n) No, skip them"

If yes: download video → transcribe → summarize transcript → save to inbox/ with `type: video-transcript` frontmatter.

## Expected advantages / benefits

- Meeting recordings without Gemini notes would become accessible
- Users who prefer recording-first workflows (no Gemini) get full coverage
- Same inbox format — downstream tooling (recap, etc.) doesn't need to change

## Downsides / risks

- Local Whisper: large model download (~1.5GB for medium), install friction
- API Whisper: adds a second API dependency (OpenAI) to a Claude-native tool
- Long recordings (1h+) need chunking and sequential API calls
- Video download from Drive to local disk is slow for large files

## Open questions

1. Default to API or local? Probably let user choose during /onboard integration step.
2. Where does `OPENAI_API_KEY` live — config.yaml or environment variable only?
3. Should transcription be a separate `/transcribe` command rather than part of /bootstrap?
4. What's the right chunking strategy for the 25MB Whisper API limit?
