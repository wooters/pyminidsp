## Why

The upstream miniDSP C library received a bug fix (v0.5.2) that affects the VAD feature. Since pyminidsp v0.6.0 ships VAD bindings compiled against v0.5.1, users are exposed to this bug. A patch release is needed to pick up the fix and publish corrected wheels to PyPI.

## What Changes

- Bump the pinned miniDSP C library tag from v0.5.1 to v0.5.2 in all build configurations (`pyproject.toml` cibuildwheel `before-all`, `.github/workflows/wheels.yml` sdist job).
- Bump the pyminidsp package version from 0.6.0 to 0.6.1 (`pyproject.toml`, `docs/conf.py`).
- Add a 0.6.1 changelog entry documenting the upstream bug fix.

## Capabilities

### New Capabilities

_None — this is a patch release with no new capabilities._

### Modified Capabilities

_None — no spec-level behavior changes, only an upstream bug fix picked up via version bump._

## Impact

- **Build config**: `pyproject.toml` (3 `before-all` blocks + version field), `.github/workflows/wheels.yml` (sdist clone step), `docs/conf.py` (release string).
- **Docs**: `docs/changelog.rst` gets a new 0.6.1 entry.
- **PyPI**: A new v0.6.1 tag triggers the existing CI pipeline to build wheels and publish to PyPI.
- **No API changes**: The Python wrapper code is unchanged; only the compiled C library underneath is updated.
