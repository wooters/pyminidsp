## Context

pyminidsp v0.6.0 compiles and ships the miniDSP C library at tag v0.5.1. The upstream repo has published v0.5.2 with a bug fix affecting the VAD feature. Since pyminidsp uses CFFI API mode (compiling C source at wheel-build time), picking up the fix requires only changing the git tag in build configuration — no Python wrapper code changes.

The C library tag is referenced in four places:
1. `pyproject.toml` — three `before-all` blocks (generic, Linux, macOS)
2. `.github/workflows/wheels.yml` — sdist job clone step

## Goals / Non-Goals

**Goals:**
- Pick up the miniDSP v0.5.2 bug fix in all built wheels.
- Publish pyminidsp 0.6.1 to PyPI as a patch release.
- Update documentation (changelog, version strings) to reflect the new release.

**Non-Goals:**
- Wrapping any new C API functions (there are none in v0.5.2).
- Changing the Python API surface.
- Modifying CI workflow structure or adding new platforms.

## Decisions

**Patch version bump (0.6.0 → 0.6.1)**: This is a bug fix with no API changes, so a patch bump is appropriate per semver. Alternatives considered: keeping 0.6.0 and re-publishing — rejected because PyPI does not allow re-uploading the same version.

**Same release workflow**: The existing CI pipeline already handles tag-triggered builds and publishes to PyPI. No workflow changes needed — just push a `v0.6.1` tag.

## Risks / Trade-offs

- **[Risk] v0.5.2 introduces unexpected changes beyond the bug fix** → *Mitigation*: Review the v0.5.1..v0.5.2 diff before merging. The CFFI API-mode build will catch any header-level incompatibilities at compile time.
- **[Risk] Existing tests fail with new C library** → *Mitigation*: Run the full test suite locally against v0.5.2 before tagging.
