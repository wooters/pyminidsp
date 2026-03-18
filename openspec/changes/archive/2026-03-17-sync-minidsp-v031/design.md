## Context

pyminidsp wraps the miniDSP C library via CFFI API mode. Each Python function is a thin wrapper: convert inputs with `_as_double_ptr()`, allocate output with `_new_double_array()`, call `lib.MD_*()`, return NumPy array. The C library is pinned at v0.1.0 across 4 locations (3 in `pyproject.toml`, 1 in `wheels.yml`). The library is now at v0.3.1 with 7 new functions and 1 new source file.

## Goals / Non-Goals

**Goals:**
- Wrap all 7 new C functions following the existing thin-wrapper pattern
- Add the new `STEG_SPECTEXT` constant
- Add `minidsp_resample.c` to the CFFI build
- Bump the pinned tag to v0.3.1
- Test all new wrappers

**Non-Goals:**
- Changing the existing wrapper pattern or architecture
- Adding higher-level abstractions on top of the new functions
- Wrapping `fileio.c` or `liveio.c` (still excluded — they need libsndfile/portaudio)
- Windows wheel support

## Decisions

### 1. Where to put new wrappers

**Decision**: Add new functions to existing modules where they fit; create `_resampling.py` for the resampler.

- `design_lowpass_fir` → `_filters.py` (FIR filter design belongs with FIR filters)
- `lowpass_brickwall` → `_spectral.py` (FFT-based, fits with spectrum analysis)
- `kaiser_window` → `_spectral.py` (alongside other window functions)
- `bessel_i0`, `sinc` → `_analysis.py` (math primitives, alongside other signal measurement)
- `resample`, `resample_output_len` → new `_resampling.py` (distinct capability, deserves its own module)

**Alternative considered**: Put everything in a new `_new_v031.py`. Rejected — scatters related functions and breaks the domain-based organization.

### 2. `bessel_i0` and `sinc` — expose or keep internal?

**Decision**: Expose publicly. They're documented in `minidsp.h` and useful standalone (Kaiser window design, sinc interpolation).

### 3. `resample` output buffer sizing

**Decision**: The Python wrapper calls `MD_resample_output_len()` internally to allocate the correct output buffer, then calls `MD_resample()`. The user doesn't need to pre-calculate buffer sizes. We still expose `resample_output_len()` as a public function for advanced users who want to pre-allocate.

### 4. CFFI cdef additions

**Decision**: Add all 7 new function declarations plus the `MD_STEG_SPECTEXT` define to the existing `cdef()` block. Group them logically near related existing declarations.

## Risks / Trade-offs

- **[Risk] C library API drift** → Pinning to a specific tag (v0.3.1) mitigates. The `cdef` block acts as an explicit contract.
- **[Risk] `minidsp_resample.c` has new dependencies** → It only uses FFTW3 and math, both already linked. No new system deps.
- **[Risk] Kaiser window has different signature (extra `beta` param)** → Document clearly; it's intentionally different from the other window functions.

### 5. Documentation strategy

**Decision**: Update existing Sphinx `.rst` files in-place for functions added to existing modules. Create a new `docs/api/resampling.rst` for the resampler. Update the README API overview tables and changelog.

- `docs/api/fir.rst` — add `design_lowpass_fir`
- `docs/api/spectrum.rst` — add `lowpass_brickwall`
- `docs/api/windows.rst` — add `kaiser_window` with note about `beta` param
- `docs/api/analysis.rst` — add `bessel_i0`, `sinc`
- `docs/api/resampling.rst` (new) — `resample`, `resample_output_len`
- `docs/api/constants.rst` — add `STEG_SPECTEXT`
- `docs/api/index.rst` — add `resampling` to toctree
- `docs/changelog.rst` — new version entry
- `README.md` — add rows to API overview tables, add new Resampling section
