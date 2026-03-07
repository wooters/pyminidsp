## Context

pyminidsp is a CFFI API-mode package that compiles C source from the external [miniDSP](https://github.com/wooters/miniDSP) repo at install time. The CI already builds wheels via cibuildwheel and has a PyPI publish job using trusted publishing (OIDC). However, the sdist cannot build without the `MINIDSP_SRC` env var pointing at a local clone, there is no TestPyPI validation step, and the package lacks a runtime `__version__`.

## Goals / Non-Goals

**Goals:**
- Make `pip install pyminidsp` work from an sdist without manual env vars
- Validate packages on TestPyPI before production releases
- Expose `__version__` at runtime
- Document the release workflow

**Non-Goals:**
- Vendoring miniDSP C source permanently into the repo (it stays external)
- Publishing to conda-forge
- Automating version bumps or changelog generation
- Supporting PyPy builds

## Decisions

### 1. Sdist bundles C source via `setup.py` / build hook

**Decision:** The sdist build step (already in CI) clones miniDSP into a temp dir. We'll adjust `_build_minidsp.py` to also look for the C source in a `vendor/miniDSP/` directory relative to the package root, falling back to `MINIDSP_SRC`. The CI sdist job will copy the cloned source into `vendor/miniDSP/` before running `uv build --sdist`, and `MANIFEST.in` will include it.

**Why not submodule?** Submodules add friction for contributors. The C source only needs to be present at build time, and CI already clones it.

**Why not download at build time?** PEP 517 builds should be hermetic — network access during `pip install` is unreliable and against best practices.

### 2. `__version__` via `importlib.metadata`

**Decision:** Use `importlib.metadata.version("pyminidsp")` in `__init__.py`. This reads from the installed package metadata, which is the canonical source (`pyproject.toml`).

**Why not `__version__ = "0.1.0"` hardcoded?** Single source of truth — no need to update two places.

### 3. TestPyPI as a separate workflow job

**Decision:** Add a `publish-test` job to `wheels.yml` that runs on pre-release tags (`v*rc*`, `v*a*`, `v*b*`). Uses the same trusted publishing mechanism but targets TestPyPI.

**Why not a separate workflow?** Keeps all publishing logic in one file. The `if:` conditions differentiate test vs production.

### 4. `twine check` in CI

**Decision:** Add `twine check dist/*` after building the sdist to catch README rendering issues before they reach PyPI.

## Risks / Trade-offs

- **[Sdist size increases]** → Bundling C source adds ~200KB. Acceptable for a one-time build artifact.
- **[C source version drift]** → The sdist pins to whatever commit CI clones. Mitigated by always building from the latest `main` at release time.
- **[TestPyPI name squatting]** → The `pyminidsp` name must be registered on TestPyPI separately. One-time manual step.
- **[Trusted publishing setup]** → Requires configuring the PyPI/TestPyPI project to trust the GitHub Actions workflow. One-time manual step per index.
