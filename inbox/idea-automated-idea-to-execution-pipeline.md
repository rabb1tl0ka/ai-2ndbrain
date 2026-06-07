---
tags: [idea, automation, agents, 2ndbrain]
date: 2026-06-07
---

# Automated Idea-to-Execution Pipeline

The concept: wire the 2nd brain into a pipeline that takes a raw idea and carries it all the way to a finished project, with you stepping in only once.

## How it flows

1. **Capture**: dump a raw 3am idea as a single note — no structure, just the rambling
2. **Classification**: an automation reads the note and decides what it is (project, grocery item, random thought, content to make, etc.) and routes it automatically
3. **Processing** (if it's a project): the system researches it, checks what tools already exist, watches relevant content, and turns the mess into a proposed plan
4. **The only human step**: open a Claude Code session, review the plan, approve/cut/modify — about two minutes of actual time
5. **Execution**: on approval the plan becomes a full requirements doc, one command kicks off execution, a project manager agent spins up, reads requirements, creates the sub-agents that specific project needs (developer agent, research agent, etc.) — they build it

## The insight

The trick isn't capturing ideas — everyone has notes full of those. It's the layer that **decides, plans, and executes without waiting on you**. Idea to execution with ~2 minutes of human involvement.

## What this looks like for us

The 2nd brain already handles capture and routing. What's missing is the downstream:
- Classification agent that reads inbox and decides what a note is
- A "promote to project" command that spins up the planning pipeline
- Sub-agent orchestration per project type
- The approval checkpoint before execution starts

This is a natural extension of the current inbox-first pattern — just with agents picking up after capture instead of waiting for manual processing.
