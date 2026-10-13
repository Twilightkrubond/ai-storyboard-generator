# Contributing to ai-storyboard-generator

Thanks for wanting to push panels. This is a hobbyist project — keep PRs
small, keep them testable, keep them honest.

## Getting set up

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest -q
storyboard --help
```

## What we accept

- New feature modules under `storyboard/features/<name>/` with a
  `FEATURE` manifest and at least one handler.
- New image backends implementing the `ImageBackend` protocol.
- Schema additions in `storyboard/models/schemas.py` **with** a migration
  note in the PR body.
- Bug fixes, especially around shot timing math and panel layout.

## What we reject

- Anything that phones home without an explicit opt-in in
  `config/local.toml`.
- Silent failures. Handlers must raise `StoryboardError` subclasses.
- PRs that reformat unrelated files. Run `ruff format` on what you touch.

## Commit style

`area: short imperative summary` — e.g. `frames: cache renders by prompt hash`.

## Tests

Every handler gets a unit test under `tests/`. Integration tests that
touch a real image backend must be marked `@pytest.mark.integration`
and skipped by default.