## Why

The upstream miniDSP C library (v0.5.1) now includes voice activity detection (VAD) — a fundamental building block for speech processing pipelines. VAD enables users to distinguish speech from silence/noise, which is essential for tasks like speech segmentation, preprocessing for ASR systems, and noise-aware audio analysis. Since pyminidsp aims to expose the full miniDSP API surface, we need to wrap these new functions and bump the pinned C library version from v0.4.0 to v0.5.1.

## What Changes

- Bump the pinned miniDSP C library version from v0.4.0 to v0.5.1 across all build configuration (pyproject.toml cibuildwheel `before-all`, CI workflows).
- Add CFFI declarations for the new `MD_vad_*` C functions in `_build_minidsp.py`.
- Add any new C source files (e.g., `minidsp_vad.c`) to the compiled source list.
- Create a new `_vad.py` wrapper module with a `VAD` class following the stateful `BiquadFilter` pattern (the C API uses `MD_vad_state` that persists across frame calls).
- Export the `VAD` class and `VAD_NUM_FEATURES` constant from `_core.py` and `__init__.py`.
- Add tests for all new VAD functions.
- Add Sphinx API reference documentation (`docs/api/VAD.rst`).
- Add a user guide with examples (`docs/guides/voice-activity-detection.rst`).
- Update `docs/changelog.rst` and `pyproject.toml` version for the new release.

## Capabilities

### New Capabilities
- `voice-activity-detection`: Python wrapper for the miniDSP C library's VAD functions, exposing frame-level and signal-level voice activity detection with configurable parameters.

### Modified Capabilities
_(none — this is a purely additive feature)_

## Impact

- **Code**: New `_vad.py` module; changes to `_build_minidsp.py` (cdef + source list), `_core.py`, `__init__.py`.
- **Build**: C library pin bumps from v0.4.0 to v0.5.1 in `pyproject.toml` (cibuildwheel before-all) and `.github/workflows/wheels.yml`.
- **Dependencies**: No new Python dependencies. The C library may introduce new C-level dependencies (unlikely — VAD typically uses energy/ZCR which are already linked).
- **API**: Additive only — new public functions. No breaking changes to existing API.
- **Docs**: New API page, new guide, changelog entry.
- **Version**: Package version bump (0.5.0 → 0.6.0).
