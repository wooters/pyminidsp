## Why

The CI pipeline fails when building wheels because the miniDSP C library used C23 features (`nullptr`, C23 `bool`), which aren't supported by all target compilers (especially older GCC in manylinux containers). The upstream miniDSP library has been updated to C17, tagged as v0.1.0, and now supports `make install` — pyminidsp needs to align with these changes.

## What Changes

- Update compiler flag from `-std=c2x` to `-std=c17` in `_build_minidsp.py`
- Pin `git clone` commands to the `v0.1.0` tag instead of cloning HEAD (in `pyproject.toml` cibuildwheel config and `wheels.yml` workflow)
- Downgrade manylinux image from `manylinux_2_28` back to `manylinux2014` since C23 support is no longer required
- Update comments referencing C23 to reflect C17

## Capabilities

### New Capabilities

- `c17-build-compat`: Update build configuration to use C17 standard and pin miniDSP to tagged release v0.1.0

### Modified Capabilities

(none — no existing specs)

## Impact

- `pyminidsp/_build_minidsp.py`: compiler flag change (`-std=c2x` → `-std=c17`)
- `pyproject.toml`: cibuildwheel `before-all` git clone commands pinned to tag; manylinux image may change; comment updates
- `.github/workflows/wheels.yml`: sdist build step git clone pinned to tag
