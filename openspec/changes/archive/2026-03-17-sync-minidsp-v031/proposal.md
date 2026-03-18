## Why

The pyminidsp wrapper pins miniDSP at v0.1.0, but the C library is now at v0.3.1 with new DSP capabilities (FIR filter design, resampling, brickwall filtering, Kaiser windows) and bug fixes. Users can't access these features, and the wrapper is falling behind upstream.

## What Changes

- Bump pinned miniDSP tag from `v0.1.0` to `v0.3.1` in `pyproject.toml` and CI workflow
- Add `src/minidsp_resample.c` to the CFFI build sources
- Add CFFI `cdef` declarations for 7 new C functions
- Add `STEG_SPECTEXT = 2` constant to `_helpers.py`
- Write Python wrappers for all new functions:
  - `design_lowpass_fir()` — Kaiser-windowed sinc lowpass FIR filter design
  - `lowpass_brickwall()` — FFT-based brickwall lowpass filter
  - `bessel_i0()` — zeroth-order modified Bessel function
  - `sinc()` — normalized sinc function
  - `kaiser_window()` — Kaiser window generator (with beta parameter)
  - `resample_output_len()` — compute output buffer size for resampling
  - `resample()` — polyphase sinc resampler
- Export all new names from `__init__.py` and `__all__`
- Add tests for all new wrappers
- Update documentation:
  - Add Sphinx API docs for new functions (`docs/api/` rst files)
  - Add `resampling.rst` API page and wire into `docs/api/index.rst`
  - Update `docs/api/fir.rst` with `design_lowpass_fir`
  - Update `docs/api/windows.rst` with `kaiser_window`
  - Update `docs/api/constants.rst` with `STEG_SPECTEXT`
  - Update `docs/api/spectrum.rst` with `lowpass_brickwall`
  - Update `docs/api/measurement.rst` or `docs/api/analysis.rst` with `bessel_i0`, `sinc`
  - Update `docs/changelog.rst` with new version entry
  - Update `README.md` API overview tables with new functions and constants

## Capabilities

### New Capabilities
- `fir-filter-design`: FIR filter design via `design_lowpass_fir` — Kaiser-windowed sinc lowpass
- `resampling`: Sample rate conversion via polyphase sinc resampler (`resample`, `resample_output_len`)
- `brickwall-filter`: FFT-based brickwall lowpass filtering via `lowpass_brickwall`
- `math-utilities`: Expose `bessel_i0` and `sinc` math primitives
- `kaiser-window`: Kaiser window generation with configurable beta

### Modified Capabilities
- None (all existing function signatures are unchanged)

## Impact

- **Build**: New C source file (`minidsp_resample.c`) added to compilation; CFFI cdef block grows
- **Dependencies**: miniDSP pinned tag changes from v0.1.0 → v0.3.1 (4 locations)
- **API surface**: 7 new public functions, 1 new constant (`STEG_SPECTEXT`); no breaking changes
- **CI**: Wheel build workflow tag reference updated
- **Documentation**: Sphinx API pages, README API tables, and changelog all need new entries
