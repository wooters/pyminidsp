## Why

The existing test suite (`tests/test_pyminidsp.py`, ~45 tests) covers every module but is shallow — most tests only verify output shape and dtype. There are no edge-case tests, no error/boundary tests, no numerical correctness checks against known DSP results, and no tests for the helper utilities. Complete unit tests will catch regressions, validate numerical accuracy, and give confidence for future refactoring.

## What Changes

- Expand test coverage for all 70+ public functions with numerical correctness assertions (e.g., Parseval's theorem for FFT, known filter responses, convolution properties)
- Add edge-case tests: empty arrays, length-1 signals, zero amplitude, DC signals, Nyquist-frequency signals
- Add boundary/parameter tests: extreme values, minimum valid inputs
- Add tests for `_helpers.py` internals (`_as_double_ptr`, `_new_double_array`, `shutdown`)
- Add tests for input type coercion (int arrays, float32 arrays, non-contiguous arrays)
- Add `conftest.py` with shared fixtures (common signals, sample rates)
- Split monolithic test file into per-module test files matching source structure

## Capabilities

### New Capabilities
- `comprehensive-unit-tests`: Complete unit test suite covering numerical correctness, edge cases, input coercion, and helper utilities across all pyminidsp modules

### Modified Capabilities

## Impact

- New files: `tests/conftest.py`, `tests/test_generators.py`, `tests/test_analysis.py`, `tests/test_filters.py`, `tests/test_spectral.py`, `tests/test_effects.py`, `tests/test_dtmf.py`, `tests/test_gcc.py`, `tests/test_steganography.py`, `tests/test_helpers.py`
- Removed file: `tests/test_pyminidsp.py` (replaced by per-module files)
- No production code changes
- No new dependencies (pytest already in dev deps)
