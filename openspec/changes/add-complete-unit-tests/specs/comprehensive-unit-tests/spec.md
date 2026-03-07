## ADDED Requirements

### Requirement: Shared test fixtures
The test suite SHALL provide a `conftest.py` with reusable pytest fixtures for common signals (sine, white noise, impulse, DC) and standard sample rates.

#### Scenario: Fixtures produce consistent signals
- **WHEN** a test uses the `sine_1k` fixture
- **THEN** it receives a 1024-sample, 44100 Hz sine wave at 1000 Hz with amplitude 1.0

#### Scenario: Fixtures are float64
- **WHEN** any signal fixture is used
- **THEN** the resulting array has dtype `np.float64`

### Requirement: Generator numerical correctness
Tests SHALL verify that generator outputs match known mathematical properties beyond shape/dtype checks.

#### Scenario: Sine wave frequency content
- **WHEN** a sine wave is generated at frequency F with sample rate SR
- **THEN** the magnitude spectrum peak SHALL be at bin closest to F

#### Scenario: White noise statistical properties
- **WHEN** white noise is generated with amplitude A
- **THEN** the mean SHALL be approximately 0 and standard deviation SHALL be approximately A

#### Scenario: Impulse energy
- **WHEN** an impulse is generated with amplitude A
- **THEN** the energy SHALL equal A^2

#### Scenario: Square wave RMS
- **WHEN** a square wave is generated with amplitude A
- **THEN** RMS SHALL equal A (within tolerance)

### Requirement: Analysis numerical correctness
Tests SHALL verify analysis functions against known DSP identities and mathematical results.

#### Scenario: Autocorrelation of white noise
- **WHEN** autocorrelation is computed on white noise
- **THEN** lag-0 SHALL be 1.0 and other lags SHALL be near 0

#### Scenario: Entropy of uniform vs sparse signal
- **WHEN** entropy is computed on a uniform-magnitude signal vs a single-peak signal
- **THEN** the uniform signal SHALL have higher entropy

#### Scenario: Mix identity
- **WHEN** `mix(a, b, 1.0, 0.0)` is called
- **THEN** the result SHALL equal `a`

### Requirement: Spectral numerical correctness
Tests SHALL verify FFT and spectral functions using known DSP identities.

#### Scenario: Parseval's theorem
- **WHEN** a signal's time-domain energy and frequency-domain energy (from PSD) are computed
- **THEN** they SHALL be approximately equal

#### Scenario: Phase of cosine is zero
- **WHEN** phase spectrum is computed on a pure cosine at a known bin
- **THEN** the phase at that bin SHALL be approximately 0

#### Scenario: STFT frame count
- **WHEN** `stft_num_frames` is called with signal_len, n, hop
- **THEN** the returned count SHALL match the actual number of rows from `stft()`

#### Scenario: Mel filterbank rows sum to at most 1
- **WHEN** a mel filterbank is generated
- **THEN** each column SHALL sum to at most 1.0 (triangular filters don't overlap excessively)

### Requirement: Filter numerical correctness
Tests SHALL verify filter behavior using known signal processing properties.

#### Scenario: Convolution with impulse is identity
- **WHEN** a signal is convolved with a unit impulse at position 0
- **THEN** the output SHALL equal the original signal (within the valid region)

#### Scenario: Convolution commutativity
- **WHEN** `convolution_time(a, b)` and `convolution_time(b, a)` are computed
- **THEN** the results SHALL be equal

#### Scenario: FFT convolution matches time-domain
- **WHEN** `convolution_fft_ola(a, b)` and `convolution_time(a, b)` are computed
- **THEN** the results SHALL be approximately equal

#### Scenario: Moving average of constant signal
- **WHEN** a moving average is applied to a constant signal
- **THEN** the output SHALL equal the constant (after startup)

#### Scenario: Biquad HPF passes high frequencies
- **WHEN** a high-pass biquad filter at 500 Hz processes a 5000 Hz sine
- **THEN** the output RMS SHALL be close to the input RMS

### Requirement: Effects preserve signal length
Tests SHALL verify that effect functions preserve signal properties.

#### Scenario: Delay echo with zero feedback
- **WHEN** `delay_echo` is called with feedback=0
- **THEN** the output SHALL contain the original signal plus a single delayed copy

#### Scenario: Tremolo at zero depth is identity
- **WHEN** `tremolo` is called with depth=0
- **THEN** the output SHALL approximately equal the input

### Requirement: DTMF extended character set
Tests SHALL verify DTMF generation and detection for the full character set.

#### Scenario: All valid DTMF digits roundtrip
- **WHEN** DTMF is generated for all valid digits (0-9, A-D, *, #)
- **THEN** detection SHALL recover all digits in order

### Requirement: GCC with known delay
Tests SHALL verify GCC delay estimation accuracy.

#### Scenario: Negative delay detection
- **WHEN** signal B leads signal A by N samples
- **THEN** `get_delay` SHALL return -N

#### Scenario: Zero delay
- **WHEN** two identical signals are compared
- **THEN** `get_delay` SHALL return 0

### Requirement: Steganography frequency-band method
Tests SHALL verify steganography with both LSB and frequency-band methods.

#### Scenario: Frequency-band text roundtrip
- **WHEN** a message is encoded with `STEG_FREQ_BAND` and decoded
- **THEN** the decoded message SHALL match the original

#### Scenario: Detection identifies frequency-band method
- **WHEN** `steg_detect` is called on a frequency-band encoded signal
- **THEN** it SHALL return `STEG_FREQ_BAND`

### Requirement: Window function properties
Tests SHALL verify mathematical properties of window functions.

#### Scenario: Window symmetry
- **WHEN** any window function is generated with even length N
- **THEN** the window SHALL be symmetric: `w[k] == w[N-1-k]`

#### Scenario: Hann window endpoints are zero
- **WHEN** a Hann window is generated
- **THEN** the first and last samples SHALL be 0

#### Scenario: Rectangular window is all ones
- **WHEN** a rectangular window of length N is generated
- **THEN** all N values SHALL be exactly 1.0

### Requirement: Input type coercion
Tests SHALL verify that functions accept non-float64 inputs and produce correct results.

#### Scenario: Integer array input
- **WHEN** a function receives a numpy int32 or int64 array
- **THEN** it SHALL produce a valid float64 result without error

#### Scenario: Float32 array input
- **WHEN** a function receives a numpy float32 array
- **THEN** it SHALL produce a valid float64 result without error

#### Scenario: Non-contiguous array input
- **WHEN** a function receives a non-contiguous array (e.g., `arr[::2]`)
- **THEN** it SHALL produce a valid result without error

### Requirement: Helper utilities
Tests SHALL verify the internal helper functions.

#### Scenario: _new_double_array returns correct shape and dtype
- **WHEN** `_new_double_array(N)` is called
- **THEN** it SHALL return a numpy array of shape (N,) with dtype float64

#### Scenario: _as_double_ptr handles contiguous float64
- **WHEN** `_as_double_ptr` receives a contiguous float64 array
- **THEN** it SHALL return a valid CFFI pointer without copying

#### Scenario: shutdown is callable
- **WHEN** `shutdown()` is called
- **THEN** it SHALL complete without error
