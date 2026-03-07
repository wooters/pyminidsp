## 1. Setup

- [ ] 1.1 Create `tests/conftest.py` with shared fixtures: `sine_1k` (1024 samples, 1000 Hz, 44100 SR), `white_noise_1k` (1024 samples, seed=42), `impulse_100` (100 samples, pos=0), `dc_signal` (100 samples, value=1.0), common sample rates
- [ ] 1.2 Create `tests/test_helpers.py` with tests for `_new_double_array`, `_as_double_ptr`, and `shutdown()`

## 2. Generator Tests

- [ ] 2.1 Create `tests/test_generators.py` — port existing generator tests from `test_pyminidsp.py`, then add: sine frequency content verification (spectrum peak at correct bin), white noise statistical properties (mean ~0, std ~amplitude), impulse energy (A^2), square wave RMS (equals amplitude), sawtooth range bounds, chirp frequency sweep verification, shepard tone shape

## 3. Analysis & Measurement Tests

- [ ] 3.1 Create `tests/test_analysis.py` — port existing measurement + analysis tests, then add: autocorrelation of white noise (lag-0=1, others ~0), entropy ordering (uniform > sparse), mix identity (`mix(a,b,1,0) == a`), dot product commutativity, power_db of known signal, zero_crossing_rate of DC (should be 0), f0 detection of multi-harmonic signal

## 4. Spectral Tests

- [ ] 4.1 Create `tests/test_spectral.py` — port existing spectrum/STFT/window tests, then add: Parseval's theorem, cosine phase ~0 at peak bin, STFT frame count consistency, mel filterbank column sums <= 1, MFCC with different num_coeffs, window symmetry for all window types, Hann endpoints = 0

## 5. Filter Tests

- [ ] 5.1 Create `tests/test_filters.py` — port existing FIR/biquad tests, then add: convolution with impulse = identity, convolution commutativity, FFT convolution matches time-domain, moving average of constant, biquad HPF passes high frequencies, biquad BPF passes center frequency, all biquad types process without error

## 6. Effects Tests

- [ ] 6.1 Create `tests/test_effects.py` — port existing effects tests, then add: delay echo with zero feedback behavior, tremolo at zero depth = identity, comb reverb energy relationship

## 7. DTMF Tests

- [ ] 7.1 Create `tests/test_dtmf.py` — port existing DTMF tests, then add: full character set roundtrip (0-9, A-D, *, #), single-digit timing validation, signal length calculation consistency

## 8. GCC Tests

- [ ] 8.1 Create `tests/test_gcc.py` — port existing GCC tests, then add: negative delay detection, zero delay (identical signals), GCC_SIMP weighting mode

## 9. Steganography Tests

- [ ] 9.1 Create `tests/test_steganography.py` — port existing steg tests, then add: frequency-band method text roundtrip, frequency-band detection, binary data with frequency-band method, capacity comparison between methods

## 10. Input Coercion Tests

- [ ] 10.1 Add input type coercion tests to `tests/test_helpers.py`: int32 array input, int64 array input, float32 array input, non-contiguous array input — verify all produce valid float64 results through representative functions (e.g., `rms`, `magnitude_spectrum`, `convolution_time`)

## 11. Cleanup

- [ ] 11.1 Delete `tests/test_pyminidsp.py` after verifying all original tests are ported to new files
- [ ] 11.2 Run full test suite, verify all tests pass
