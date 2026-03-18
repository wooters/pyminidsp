## Why

The pyminidsp codebase has zero type annotations today. Adding type checking with `ty` (from the Astral team behind `uv` and `ruff`) catches bugs at development time, improves editor autocompletion, and documents the API contract for consumers of the library. `ty` is a natural fit since the project already uses `uv` for package management.

## What Changes

- Add `ty` as a dev dependency and configure it in `pyproject.toml`
- Add type annotations to all public functions and the `BiquadFilter` class
- Create a type stub (`.pyi`) for the CFFI-generated `_minidsp_cffi` extension module so `ty` can reason about `ffi` and `lib`
- Add a `py.typed` marker so downstream consumers get type information
- Add a type-checking step to CI

## Capabilities

### New Capabilities
- `type-checking`: Configuration, annotations, CFFI stubs, and CI integration for `ty`-based static type checking

### Modified Capabilities
<!-- No existing spec-level requirements are changing -->

## Impact

- **Code**: All `pyminidsp/_*.py` modules gain type annotations; new `pyminidsp/_minidsp_cffi.pyi` stub and `pyminidsp/py.typed` marker
- **Dependencies**: `ty` added as a dev/CI dependency (installed via `uv tool install ty`)
- **CI**: `.github/workflows/wheels.yml` gains a type-check job
- **API**: No runtime behavior changes — annotations only
