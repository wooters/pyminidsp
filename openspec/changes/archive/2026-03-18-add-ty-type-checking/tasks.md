## 1. Configuration & Scaffolding

- [x] 1.1 Add `[tool.ty]` section to `pyproject.toml` (target Python 3.9, exclude tests and `_build_minidsp.py`)
- [x] 1.2 Create empty `pyminidsp/py.typed` marker file
- [x] 1.3 Ensure `py.typed` is included in package data (update `pyproject.toml` if needed)

## 2. CFFI Type Stub

- [x] 2.1 Create `pyminidsp/_minidsp_cffi.pyi` with type declarations for `ffi` (cast, new, buffer, gc, etc.) and all `lib.MD_*` / `lib.BiQuad_*` functions used by the Python wrappers

## 3. Type Annotations — Helpers & Core

- [x] 3.1 Annotate `_helpers.py` (`_as_double_ptr`, `_new_double_array`, `shutdown`, constants)
- [x] 3.2 Annotate `_analysis.py` (all public functions)
- [x] 3.3 Annotate `_spectral.py` (all public functions)
- [x] 3.4 Annotate `_filters.py` (all public functions + `BiquadFilter` class)
- [x] 3.5 Annotate `_effects.py` (all public functions)
- [x] 3.6 Annotate `_generators.py` (all public functions)
- [x] 3.7 Annotate `_dtmf.py` (all public functions)
- [x] 3.8 Annotate `_gcc.py` (all public functions)
- [x] 3.9 Annotate `_resampling.py` (all public functions)
- [x] 3.10 Annotate `_steganography.py` (all public functions)
- [x] 3.11 Annotate `_core.py` (re-export module, if any signatures needed)

## 4. Validate & Fix

- [x] 4.1 Run `ty check` locally and fix all reported errors until exit code 0
- [x] 4.2 Run existing test suite (`pytest`) to confirm no runtime regressions

## 5. CI Integration

- [x] 5.1 Add `type-check` job to `.github/workflows/wheels.yml` that installs `ty` and runs `ty check`
