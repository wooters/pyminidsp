## 1. Sdist C Source Bundling

- [x] 1.1 Update `_build_minidsp.py` to resolve C source path: check `MINIDSP_SRC` env var first, then fall back to `vendor/miniDSP/` relative to project root, and fail with a clear error if neither exists
- [x] 1.2 Update `MANIFEST.in` to include `recursive-include vendor/miniDSP *.c *.h`
- [x] 1.3 Update CI sdist job in `wheels.yml` to copy cloned miniDSP source into `vendor/miniDSP/` before running `uv build --sdist`

## 2. Runtime Version

- [x] 2.1 Add `__version__ = importlib.metadata.version("pyminidsp")` to `pyminidsp/__init__.py`

## 3. TestPyPI and Validation

- [x] 3.1 Add `twine check dist/*` step to CI after sdist build
- [x] 3.2 Add `publish-test` job to `wheels.yml` that publishes to TestPyPI on pre-release tags (`v*rc*`, `v*a*`, `v*b*`) using trusted publishing
- [x] 3.3 Update the existing `publish` job's `if:` condition to exclude pre-release tags

## 4. Release Documentation

- [x] 4.1 Create `RELEASING.md` with step-by-step release instructions covering: version bump, pre-release tag for TestPyPI validation, stable tag for production PyPI, and post-release verification
