## Why

The v0.5.0 tag has been pushed and the package published to PyPI, but the live documentation at wooters.github.io/pyminidsp/changelog.html still shows "0.5.0 (unreleased)". Additionally, the Sphinx `release` variable in `docs/conf.py` is stuck at `"0.1.0"` — it was never updated after the initial release. Both issues make the published docs look stale and inconsistent with the actual release state.

## What Changes

- Update `docs/changelog.rst`: replace "0.5.0 (unreleased)" with "0.5.0 (2026-03-18)" to reflect the actual release date.
- Update `docs/conf.py`: change `release = "0.1.0"` to `release = "0.5.0"` so Sphinx renders the correct version.
- Update `RELEASING.md`: add a step reminding maintainers to update `docs/changelog.rst` and `docs/conf.py` as part of the release process, so this doesn't happen again.

## Capabilities

### New Capabilities

_(none — this is a docs-only fix)_

### Modified Capabilities

_(none — no spec-level behavior changes)_

## Impact

- **Docs site** (`wooters.github.io/pyminidsp`): changelog and version display will be corrected once changes are merged and the docs workflow runs.
- **Code**: no runtime code changes; only documentation and release-process files are touched.
