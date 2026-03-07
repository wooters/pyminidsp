## Why

pyminidsp has working CI (cibuildwheel + GitHub Actions) and a nearly complete `pyproject.toml`, but several gaps prevent a successful first release to PyPI: no TestPyPI dry-run step, the sdist doesn't bundle the C source it needs, and the package lacks a single-source-of-truth version accessible at runtime. Closing these gaps enables `git tag v0.1.0 && git push --tags` to produce a working PyPI release.

## What Changes

- Bundle the miniDSP C source inside the sdist so `pip install pyminidsp` works without `MINIDSP_SRC` (download or vendor at build time).
- Expose `pyminidsp.__version__` sourced from `pyproject.toml` via `importlib.metadata`.
- Add a TestPyPI publish step to the CI workflow so every tagged pre-release (`v*rc*`, `v*a*`) goes to TestPyPI first.
- Add a `MANIFEST.in` entry for the C source (or adjust the build to fetch it).
- Verify `long_description` (README) renders correctly on PyPI with `twine check`.
- Document the release process (tag → CI → PyPI) in a short RELEASING.md.

## Capabilities

### New Capabilities
- `sdist-c-source`: Ensure the sdist is self-contained by bundling or fetching the miniDSP C source at build time.
- `runtime-version`: Expose `__version__` at runtime from package metadata.
- `testpypi-workflow`: Add a TestPyPI publish step to validate packages before production PyPI release.
- `release-docs`: Document the end-to-end release process.

### Modified Capabilities
(none)

## Impact

- `pyproject.toml` — minor metadata tweaks
- `MANIFEST.in` — add C source or fetch script
- `_build_minidsp.py` — adjust to find bundled C source in sdist
- `.github/workflows/wheels.yml` — add TestPyPI step, `twine check`
- `pyminidsp/__init__.py` — add `__version__`
- New file: `RELEASING.md`
