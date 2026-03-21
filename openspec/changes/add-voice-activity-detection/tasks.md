## 1. Bump C Library Version

- [x] 1.1 Update `pyproject.toml` cibuildwheel `before-all` to clone miniDSP v0.5.1 (replace v0.4.0 tag)
- [x] 1.2 Update `.github/workflows/wheels.yml` if it references the miniDSP tag separately
- [x] 1.3 Clone miniDSP v0.5.1 locally and verify it builds

## 2. CFFI Build Script Updates

- [x] 2.1 Inspect miniDSP v0.5.1 `include/minidsp.h` for exact `MD_vad_params` struct, `MD_vad_state` struct, and `MD_VAD_NUM_FEATURES` constant definitions
- [x] 2.2 Add `MD_vad_params` and `MD_vad_state` struct declarations (replacing `MD_VAD_NUM_FEATURES` with literal `5` since CFFI cdef doesn't support `#define`) and all four VAD function signatures (`MD_vad_default_params`, `MD_vad_init`, `MD_vad_calibrate`, `MD_vad_process_frame`) to `ffibuilder.cdef()` in `_build_minidsp.py`
- [x] 2.3 Add `src/minidsp_vad.c` (or equivalent) to `_core_sources` list if it exists as a new file
- [x] 2.4 Rebuild the CFFI extension locally and verify `lib.MD_vad_*` symbols are accessible

## 3. Python Wrapper Module

- [x] 3.1 Create `pyminidsp/_vad.py` with `VAD` class: constructor calls `MD_vad_default_params()` then applies keyword overrides (`threshold`, `onset_frames`, `hangover_frames`, `adaptation_rate`, `band_low_hz`, `band_high_hz`, `weights`), then calls `MD_vad_init()`
- [x] 3.2 Implement `VAD.calibrate(signal, sample_rate)` — calls `MD_vad_calibrate()`
- [x] 3.3 Implement `VAD.process_frame(signal, sample_rate)` — calls `MD_vad_process_frame()`, returns `(decision, score, features)` tuple
- [x] 3.4 Implement `VAD.process(signal, sample_rate, frame_len)` convenience method — segments signal into frames, calls `process_frame()` on each, returns `(decisions, scores, features)` arrays
- [x] 3.5 Add `VAD_NUM_FEATURES: int = 5` constant to `_helpers.py` (matching the pattern of other constants like `ERR_NULL_POINTER`, `STEG_LSB`)
- [x] 3.6 Add VAD exports (`VAD`, `VAD_NUM_FEATURES`) to `pyminidsp/_core.py`
- [x] 3.7 Add VAD imports and exports to `pyminidsp/__init__.py` (both the import block and `__all__`)

## 4. Tests

- [x] 4.1 Create `tests/test_vad.py` with tests covering the `VAD` class
- [x] 4.2 Test default construction and custom parameter overrides
- [x] 4.3 Test `calibrate()` with a silence signal
- [x] 4.4 Test `process_frame()` on silence (decision=0) and on a sine tone (decision=1)
- [x] 4.5 Test `process_frame()` returns correct tuple structure: `(int, float, ndarray of length 5)`
- [x] 4.6 Test `process()` batch method returns correctly shaped arrays
- [x] 4.7 Test error handling (invalid inputs raise `MiniDSPError`)
- [x] 4.8 Run full test suite to ensure no regressions

## 5. Documentation

- [x] 5.1 Create `docs/api/VAD.rst` with autodoc directives for `VAD` class and `VAD_NUM_FEATURES` constant
- [x] 5.2 Add VAD.rst to the API docs toctree in `docs/api/index.rst`
- [x] 5.3 Create `docs/guides/voice-activity-detection.rst` with tutorial covering initialization, calibration, frame-by-frame processing, and batch processing
- [x] 5.4 Add the guide to the guides toctree
- [x] 5.5 Build docs locally and verify VAD pages render correctly

## 6. Version and Release Prep

- [x] 6.1 Update version in `pyproject.toml` from 0.5.0 to 0.6.0
- [x] 6.2 Update version in `docs/conf.py` if it's tracked there
- [x] 6.3 Add 0.6.0 changelog entry to `docs/changelog.rst` documenting `VAD`, `VAD_NUM_FEATURES`, and the miniDSP v0.5.1 upgrade
