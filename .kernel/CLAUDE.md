@.kernel/roadmap/CLAUDE.md

## Test Gate

After any change to `.kernel/` or `.claude/commands/`, run the test suite and verify all tests pass before considering the work done:

```bash
python3 .kernel/test.py
```

All 62 tests must pass. If any fail, fix the issue before moving on.
