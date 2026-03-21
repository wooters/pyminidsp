## Context

pyminidsp wraps the miniDSP C library via CFFI API mode. Each functional domain lives in its own Python module (`_analysis.py`, `_effects.py`, `_resampling.py`, etc.). Stateless functions follow a thin-wrapper pattern (convert inputs, call C, return NumPy array). Stateful APIs use a class that manages C-allocated state — see `BiquadFilter` in `_filters.py`.

The miniDSP C library v0.5.1 adds a **stateful, frame-by-frame** VAD API consisting of two structs and four functions:

- `MD_vad_params` — configuration struct with fields: `weights[5]`, `threshold`, `onset_frames`, `hangover_frames`, `adaptation_rate`, `band_low_hz`, `band_high_hz`
- `MD_vad_state` — runtime state struct with fields: `params` (embedded), `min_features[5]`, `max_features[5]`, `state`, `frame_count`
- `MD_VAD_NUM_FEATURES` — `#define` constant equal to 5

The four functions:

- `MD_vad_default_params(MD_vad_params *params)` — populate params with defaults
- `MD_vad_init(MD_vad_state *state, const MD_vad_params *params)` — initialize state (NULL params → defaults)
- `MD_vad_calibrate(MD_vad_state *state, const double *signal, unsigned N, double sample_rate)` — seed normalization with known silence
- `MD_vad_process_frame(MD_vad_state *state, const double *signal, unsigned N, double sample_rate, double *score_out, double *features_out)` — process one frame, returns 1 (speech) or 0 (silence)

The VAD extracts five features per frame (energy, ZCR, spectral entropy, spectral flatness, band energy ratio), normalizes them adaptively, computes a weighted score, and applies an onset/hangover state machine.

## Goals / Non-Goals

**Goals:**
- Wrap the VAD API in a `VAD` class following the `BiquadFilter` pattern.
- Expose calibration, frame-by-frame processing, and a convenience batch-process method.
- Export the `VAD_NUM_FEATURES` constant.
- Provide full test coverage and Sphinx documentation.
- Bump the C library pin (v0.4.0 → v0.5.1) and package version (0.5.0 → 0.6.0).

**Non-Goals:**
- Streaming/real-time VAD beyond what the C library provides.
- Higher-level abstractions (speech segmentation, VAD-triggered recording).
- Wrapping any other new functions that may exist in v0.5.1 beyond VAD.
- Windows support (not currently supported).

## Decisions

### 1. Class-based wrapper (`VAD` class) — not free functions

**Decision**: Wrap the stateful C API in a `VAD` class, similar to `BiquadFilter`.

**Rationale**: The C API uses `MD_vad_state` that must persist across calls. A class naturally encapsulates this lifetime. `BiquadFilter` already establishes this pattern in the codebase.

**Alternative considered**: Free functions that create/destroy state internally per call. Rejected because the VAD's onset/hangover state machine and adaptive normalization require state to persist across frames.

### 2. Stack-allocated state via `ffi.new()` — not heap-allocated

**Decision**: Allocate `MD_vad_params` and `MD_vad_state` with `ffi.new()` (CFFI-managed memory) rather than calling a C allocator.

**Rationale**: `ffi.new()` ties the lifetime to the Python object. No need for explicit `free()` calls or `__del__` cleanup (unlike `BiquadFilter` which calls `lib.free()`). This is simpler and less error-prone, and works because the C API takes pointers to these structs rather than returning heap-allocated pointers.

### 3. Constructor accepts keyword overrides on top of defaults

**Decision**: The `VAD` constructor first calls `MD_vad_default_params()`, then applies any keyword arguments matching the `MD_vad_params` field names (`threshold`, `onset_frames`, `hangover_frames`, `adaptation_rate`, `band_low_hz`, `band_high_hz`, `weights`) to the params struct before calling `MD_vad_init()`.

**Rationale**: This gives users a clean Pythonic API (`VAD(threshold=0.3)`) while preserving the C library's defaults as the baseline. Using the same names as the C struct fields keeps the mapping transparent. No need to expose the params struct directly.

### 4. `process_frame()` returns `(decision, score, features)`

**Decision**: Return a tuple of `(int, float, ndarray)` from `process_frame()`.

**Rationale**: The C function writes to `score_out` and `features_out` pointers and returns the decision as an int. Returning all three gives users full access to the VAD internals without separate calls.

### 5. `process()` convenience method for batch processing

**Decision**: Add a `process(signal, sample_rate, frame_len)` method that segments the signal into non-overlapping frames and calls `process_frame()` on each, returning arrays.

**Rationale**: Frame-by-frame Python loops are the common case. A batch method avoids boilerplate and is more efficient. This is analogous to `BiquadFilter.process_array()`.

### 6. New `_vad.py` module

**Decision**: Create a dedicated `pyminidsp/_vad.py` module.

**Rationale**: Every functional domain in pyminidsp has its own module. VAD is a distinct speech-processing domain.

## Risks / Trade-offs

- **[Risk] Struct layout mismatch** — The CFFI cdef must match the exact struct layout from v0.5.1's header. Note that `MD_VAD_NUM_FEATURES` is a `#define` which CFFI cdef doesn't support, so array sizes must be hardcoded as `5` in the cdef. → *Mitigation*: Copy declarations directly from `minidsp.h` and replace the macro with its literal value. CFFI API mode compiles against the header, so mismatches cause build errors (not silent bugs).
- **[Risk] New C dependencies** — VAD uses spectral entropy and flatness which may need FFT. → *Mitigation*: FFTW3 is already a linked dependency. No new libraries expected.
- **[Risk] CI build breakage from version bump** — Changing the pinned tag from v0.4.0 to v0.5.1 could surface new compilation issues. → *Mitigation*: Test locally before pushing; CI covers Linux and macOS.
