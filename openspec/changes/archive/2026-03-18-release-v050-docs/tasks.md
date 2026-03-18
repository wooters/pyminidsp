## 1. Fix Documentation Files

- [x] 1.1 Update `docs/changelog.rst`: change "0.5.0 (unreleased)" to "0.5.0 (2026-03-18)"
- [x] 1.2 Update `docs/conf.py`: change `release = "0.1.0"` to `release = "0.5.0"`

## 2. Prevent Future Drift

- [x] 2.1 Add a "Update docs" step to `RELEASING.md` reminding maintainers to update `docs/changelog.rst` (mark version as released with date) and `docs/conf.py` (bump `release` variable)

## 3. Verify

- [x] 3.1 Build docs locally with `sphinx-build` to confirm no errors and correct version/changelog rendering
