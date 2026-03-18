## Context

The v0.5.0 release has been tagged and published to PyPI, but two documentation files were not updated as part of the release:

1. `docs/changelog.rst` — still says "0.5.0 (unreleased)"
2. `docs/conf.py` — `release` is hardcoded to `"0.1.0"` (never updated since initial setup)

The docs site rebuilds automatically on push to `main` via `.github/workflows/docs.yml`.

## Goals / Non-Goals

**Goals:**
- Fix the changelog to show 0.5.0 as released with the correct date (2026-03-18)
- Update the Sphinx version to 0.5.0
- Add a release-checklist step to `RELEASING.md` so these files don't fall out of sync again

**Non-Goals:**
- Automating version extraction from `pyproject.toml` into `docs/conf.py` (nice-to-have, but out of scope)
- Changing the docs build/deploy workflow

## Decisions

1. **Use the tag date (2026-03-18) for the changelog entry.** The v0.5.0 tag was created today. This is the authoritative release date.

2. **Keep the Sphinx `release` as a hardcoded string.** An alternative would be to read it dynamically from `importlib.metadata` or `pyproject.toml` at build time. This adds complexity for marginal benefit — a simple reminder in the release checklist is sufficient.

3. **Add a docs update step to `RELEASING.md`.** This is the lightest-weight solution to prevent recurrence — no tooling changes, just process.

## Risks / Trade-offs

- **Risk**: The `release` in `docs/conf.py` will drift again on future releases. → **Mitigation**: The new checklist step in `RELEASING.md` addresses this. A future change could automate it if it keeps happening.
