## 1. Bump C Library Tag

- [x] 1.1 Update `pyproject.toml` generic `before-all` to clone miniDSP v0.5.2 (line 76)
- [x] 1.2 Update `pyproject.toml` Linux `before-all` to clone miniDSP v0.5.2 (line 86)
- [x] 1.3 Update `pyproject.toml` macOS `before-all` to clone miniDSP v0.5.2 (line 95)
- [x] 1.4 Update `.github/workflows/wheels.yml` sdist job to clone miniDSP v0.5.2 (line 68)

## 2. Bump Package Version

- [x] 2.1 Update `pyproject.toml` version from `"0.6.0"` to `"0.6.1"`
- [x] 2.2 Update `docs/conf.py` release from `"0.6.0"` to `"0.6.1"`

## 3. Update Documentation

- [x] 3.1 Add 0.6.1 changelog entry to `docs/changelog.rst` documenting the miniDSP v0.5.2 bug fix

## 4. Verify

- [x] 4.1 Clone miniDSP v0.5.2 locally and run `MINIDSP_SRC=./miniDSP uv sync` to verify build
- [x] 4.2 Run test suite against the new C library version
- [x] 4.3 Commit changes and tag `v0.6.1` to trigger CI publish
