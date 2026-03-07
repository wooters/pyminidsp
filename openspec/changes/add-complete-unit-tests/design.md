## Context

pyminidsp has a single test file (`tests/test_pyminidsp.py`) with ~45 tests across 14 classes. Tests primarily check output shapes and dtypes. The library wraps 70+ C functions via CFFI with a consistent pattern: convert inputs, call `lib.MD_*`, return numpy array. This uniformity makes systematic test expansion straightforward.

## Goals / Non-Goals

**Goals:**
- Achieve thorough test coverage of all public API functions
- Validate numerical correctness against known DSP identities (Parseval's theorem, convolution commutativity, filter frequency response)
- Test edge cases and boundary conditions
- Test input type coercion (int, float32, non-contiguous arrays)
- Organize tests into per-module files matching source structure
- Provide shared fixtures via `conftest.py`

**Non-Goals:**
- Performance/benchmark testing
- Integration testing with external audio files
- Testing the C library internals directly
- Testing the CFFI build system (`_build_minidsp.py`)
- Achieving 100% line coverage of Python wrapper code (some error paths may be C-level)

## Decisions

### 1. Split tests into per-module files
**Decision:** One test file per source module (e.g., `test_generators.py` for `_generators.py`), plus `test_helpers.py`.
**Rationale:** Mirrors source structure, makes it easy to find tests, enables running subsets. The monolithic file is already 444 lines and will grow 3-4x.
**Alternative considered:** Keep single file — rejected because it becomes unwieldy at 1500+ lines.

### 2. Shared fixtures in conftest.py
**Decision:** Create `tests/conftest.py` with pytest fixtures for common signals (sine, noise, impulse, DC) and sample rates.
**Rationale:** Many tests need the same input signals; fixtures reduce duplication and ensure consistency.

### 3. Numerical correctness via DSP identities
**Decision:** Validate results using known mathematical properties rather than hardcoded expected values.
**Rationale:** Hardcoded values are fragile and opaque. DSP identities (e.g., Parseval's theorem: energy in time == energy in frequency) are self-documenting and implementation-independent.
**Key identities to test:**
- Parseval's theorem for FFT
- Convolution with impulse == identity
- Convolution commutativity: `conv(a,b) == conv(b,a)`
- LPF attenuates above cutoff, HPF attenuates below
- Window functions: symmetric, endpoints match known values
- RMS of sine wave = amplitude / sqrt(2)

### 4. Retain existing test logic
**Decision:** Port all existing tests into the new per-module files (preserving assertions), then add new tests alongside them.
**Rationale:** Existing tests are correct and useful; no reason to discard them.

## Risks / Trade-offs

- **[Risk] Tests depend on C library numerical precision** → Use `pytest.approx` and `np.testing.assert_allclose` with reasonable tolerances (1e-6 to 1e-2 depending on operation)
- **[Risk] Edge-case inputs could crash C code (segfault)** → Only test edge cases that the Python wrapper should handle gracefully; don't test inputs that bypass the wrapper
- **[Trade-off] More test files = more maintenance** → Mitigated by consistent structure and shared fixtures
