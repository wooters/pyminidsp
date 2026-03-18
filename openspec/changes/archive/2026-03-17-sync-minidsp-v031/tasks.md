## 1. Bump miniDSP Version

- [x] 1.1 Update pinned tag from `v0.1.0` to `v0.3.1` in `pyproject.toml` (3 locations: lines 73, 83, 91)
- [x] 1.2 Update pinned tag from `v0.1.0` to `v0.3.1` in `.github/workflows/wheels.yml` (line 56)

## 2. CFFI Build Updates

- [x] 2.1 Add `src/minidsp_resample.c` to `_core_sources` in `_build_minidsp.py`
- [x] 2.2 Add `cdef` declarations for `MD_bessel_i0`, `MD_sinc`, `MD_Gen_Kaiser_Win`, `MD_design_lowpass_fir`, `MD_lowpass_brickwall`, `MD_resample_output_len`, `MD_resample`

## 3. Constants

- [x] 3.1 Add `STEG_SPECTEXT = 2` to `_helpers.py`
- [x] 3.2 Export `STEG_SPECTEXT` from `_core.py` and `__init__.py`

## 4. Python Wrappers — Math Utilities

- [x] 4.1 Add `bessel_i0(x)` and `sinc(x)` to `_analysis.py`

## 5. Python Wrappers — Kaiser Window

- [x] 5.1 Add `kaiser_window(n, beta)` to `_spectral.py`

## 6. Python Wrappers — FIR Filter Design

- [x] 6.1 Add `design_lowpass_fir(num_taps, cutoff_freq, sample_rate, kaiser_beta)` to `_filters.py`

## 7. Python Wrappers — Brickwall Filter

- [x] 7.1 Add `lowpass_brickwall(signal, cutoff_hz, sample_rate)` to `_spectral.py`

## 8. Python Wrappers — Resampling

- [x] 8.1 Create `_resampling.py` with `resample_output_len()` and `resample()`
- [x] 8.2 Wire `_resampling.py` into `_core.py`

## 9. Exports

- [x] 9.1 Add all new functions to `_core.py` imports
- [x] 9.2 Add all new functions to `__init__.py` imports and `__all__`

## 10. Tests

- [x] 10.1 Add tests for `bessel_i0` and `sinc`
- [x] 10.2 Add tests for `kaiser_window`
- [x] 10.3 Add tests for `design_lowpass_fir`
- [x] 10.4 Add tests for `lowpass_brickwall`
- [x] 10.5 Add tests for `resample_output_len` and `resample`
- [x] 10.6 Add test for `STEG_SPECTEXT` constant

## 11. Documentation — Sphinx API Pages

- [x] 11.1 Update `docs/api/fir.rst` — add `design_lowpass_fir` entry
- [x] 11.2 Update `docs/api/windows.rst` — add `kaiser_window` entry (note `beta` param differs from other windows)
- [x] 11.3 Update `docs/api/spectrum.rst` — add `lowpass_brickwall` entry
- [x] 11.4 Update `docs/api/analysis.rst` — add `bessel_i0` and `sinc` entries
- [x] 11.5 Create `docs/api/resampling.rst` with `resample` and `resample_output_len`
- [x] 11.6 Add `resampling` to toctree in `docs/api/index.rst`
- [x] 11.7 Update `docs/api/constants.rst` — add `STEG_SPECTEXT` entry

## 12. Documentation — README & Changelog

- [x] 12.1 Update `README.md` API overview tables: add new functions to relevant sections, add Resampling section, add `STEG_SPECTEXT` to Constants table
- [x] 12.2 Update `docs/changelog.rst` — add new version entry with all new features

## 13. Build Verification

- [x] 13.1 Run `MINIDSP_SRC=./miniDSP uv sync` and verify build succeeds
- [x] 13.2 Run full test suite and verify all tests pass
- [x] 13.3 Build Sphinx docs and verify no warnings for new entries
