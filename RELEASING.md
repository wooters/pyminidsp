# Releasing pyminidsp

## Prerequisites (one-time setup)

1. **PyPI**: Create the `pyminidsp` project on [pypi.org](https://pypi.org). Configure trusted publishing for the GitHub Actions workflow (`wooters/pyminidsp`, workflow `wheels.yml`, environment `pypi`).

2. **TestPyPI**: Create the `pyminidsp` project on [test.pypi.org](https://test.pypi.org). Configure trusted publishing with environment `testpypi`.

## Release process

### 1. Bump the version

Edit `pyproject.toml` and update the `version` field:

```toml
version = "0.2.0"
```

Commit:

```bash
git add pyproject.toml
git commit -m "Bump version to 0.2.0"
git push
```

### 2. Update documentation

Update the changelog and Sphinx version to reflect the new release:

- `docs/changelog.rst` — replace `(unreleased)` with the release date, e.g. `0.5.0 (2026-03-18)`.
- `docs/conf.py` — set `release = "0.5.0"` to match the new version.

Commit alongside the version bump or as a separate commit before tagging.

### 3. Validate on TestPyPI (recommended for first release or major changes)

Push a pre-release tag to trigger a TestPyPI publish:

```bash
git tag v0.2.0rc1
git push origin v0.2.0rc1
```

CI will build wheels + sdist and publish to TestPyPI. Verify the package installs correctly:

```bash
uv run --no-project \
  --with pyminidsp==0.2.0rc1 \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  python -c "import pyminidsp; print(pyminidsp.__version__)"
```

The `--extra-index-url` is needed so that dependencies (numpy, cffi) resolve from production PyPI.

### 4. Publish to production PyPI

Once satisfied, push the stable tag:

```bash
git tag v0.2.0
git push origin v0.2.0
```

CI will build and publish to PyPI automatically.

### 5. Verify

```bash
uv run --no-project --with pyminidsp==0.2.0 \
  python -c "import pyminidsp; print(pyminidsp.__version__)"
```

Check the release page at https://pypi.org/project/pyminidsp/

## Tag conventions

| Tag pattern | Destination |
|------------|-------------|
| `v1.2.3` | Production PyPI |
| `v1.2.3rc1` | TestPyPI |
| `v1.2.3alpha1` | TestPyPI |
| `v1.2.3beta1` | TestPyPI |

**Note:** The workflow uses `contains()` substring matching on tag names. Single-letter
suffixes like `a1`/`b1` are **not** supported — they match normal version strings
(e.g., `v0.2.0` contains `b`). Always use the full words `alpha`/`beta`.
