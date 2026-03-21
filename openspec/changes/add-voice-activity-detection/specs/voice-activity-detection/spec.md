## ADDED Requirements

### Requirement: CFFI declarations for VAD C types and functions
The build script (`_build_minidsp.py`) SHALL declare the `MD_vad_params` and `MD_vad_state` structs (with array sizes hardcoded to 5, since CFFI cdef does not support `#define` macros) and all four VAD function signatures (`MD_vad_default_params`, `MD_vad_init`, `MD_vad_calibrate`, `MD_vad_process_frame`) in the `ffibuilder.cdef()` block. Any new C source files (e.g., `minidsp_vad.c`) SHALL be added to the `_core_sources` list.

#### Scenario: VAD symbols are available through CFFI
- **WHEN** the package is built with miniDSP v0.5.1 source
- **THEN** `lib.MD_vad_default_params`, `lib.MD_vad_init`, `lib.MD_vad_calibrate`, and `lib.MD_vad_process_frame` are accessible in Python, and `ffi.new("MD_vad_params *")` and `ffi.new("MD_vad_state *")` succeed

#### Scenario: New C source file is compiled
- **WHEN** the miniDSP v0.5.1 source includes a `minidsp_vad.c` file
- **THEN** it is listed in `_core_sources` and compiled into the extension module

### Requirement: VAD class with stateful frame-by-frame processing
The system SHALL provide a `VAD` class in `_vad.py` that manages `MD_vad_params` and `MD_vad_state` structs, following the same stateful pattern as `BiquadFilter` in `_filters.py`.

#### Scenario: Construct with default parameters
- **WHEN** calling `VAD()`
- **THEN** a detector is created with default parameters (weights=0.2 each, threshold=0.5, onset_frames=3, hangover_frames=15, adaptation_rate=0.01, band_low_hz=300.0, band_high_hz=3400.0)

#### Scenario: Construct with custom parameters
- **WHEN** calling `VAD(threshold=0.3, hangover_frames=20)`
- **THEN** a detector is created with the specified threshold and hangover frames, and defaults for all other parameters

#### Scenario: Custom feature weights
- **WHEN** calling `VAD(weights=[0.4, 0.1, 0.1, 0.1, 0.3])`
- **THEN** the detector uses the specified weights for the five features (energy, ZCR, spectral entropy, spectral flatness, band energy ratio)

### Requirement: Calibrate with silence
The `VAD` class SHALL provide a `calibrate(signal, sample_rate)` method that feeds a known-silence frame to seed the adaptive normalization without producing a decision.

#### Scenario: Calibrate improves accuracy
- **WHEN** calling `detector.calibrate(silence_signal, sample_rate=16000.0)` before processing
- **THEN** the method completes without error and the detector's internal normalization state is updated

#### Scenario: Multiple calibration calls
- **WHEN** calling `calibrate()` multiple times with different silence frames
- **THEN** each call succeeds and further refines the normalization estimates

### Requirement: Process a single frame
The `VAD` class SHALL provide a `process_frame(signal, sample_rate)` method that processes one audio frame and returns a named tuple or tuple of `(decision, score, features)`.

#### Scenario: Detect speech in an active frame
- **WHEN** calling `detector.process_frame(speech_frame, sample_rate=16000.0)` on a frame containing speech-like energy
- **THEN** the returned decision is 1 (speech), score is a float in [0.0, 1.0], and features is a float64 NumPy array of length `MD_VAD_NUM_FEATURES` (5)

#### Scenario: Detect silence in a quiet frame
- **WHEN** calling `detector.process_frame(silence_frame, sample_rate=16000.0)` on a frame of zeros
- **THEN** the returned decision is 0 (silence)

#### Scenario: Onset/hangover state machine
- **WHEN** processing a sequence of frames where speech starts and then stops
- **THEN** the detector applies onset confirmation (requires `onset_frames` consecutive active frames before switching to speech) and hangover (remains in speech state for `hangover_frames` after activity drops)

### Requirement: Process an entire signal (convenience method)
The `VAD` class SHALL provide a `process(signal, sample_rate, frame_len)` method that segments a signal into frames and processes each one, returning arrays of decisions, scores, and features for all frames.

#### Scenario: Batch process a multi-frame signal
- **WHEN** calling `detector.process(signal, sample_rate=16000.0, frame_len=320)` on a 16000-sample signal (1 second at 16 kHz, 320 samples = 20ms frames)
- **THEN** a tuple of `(decisions, scores, features)` is returned where decisions is an integer array of length 50, scores is a float64 array of length 50, and features is a float64 2D array of shape (50, 5)

#### Scenario: All-silence signal returns no active frames
- **WHEN** calling `process()` on a signal that is all zeros
- **THEN** all decisions are 0

### Requirement: VAD_NUM_FEATURES Python constant is exported
The system SHALL define a `VAD_NUM_FEATURES: int = 5` Python constant in `_helpers.py` (matching the pattern of other constants like `ERR_NULL_POINTER` and `STEG_LSB`), corresponding to the C library's `#define MD_VAD_NUM_FEATURES 5`.

#### Scenario: Constant is accessible
- **WHEN** running `from pyminidsp import VAD_NUM_FEATURES`
- **THEN** the import succeeds and the value is 5

### Requirement: VAD wrapper follows established patterns
The `VAD` class and any helper functions SHALL follow established pyminidsp patterns: accept NumPy-compatible arrays, auto-convert to contiguous float64 via `_as_double_ptr()`, check for errors via `_check_error()`, and return NumPy arrays.

#### Scenario: Non-contiguous input is accepted
- **WHEN** passing a non-contiguous NumPy array (e.g., a slice `signal[::2]`) to `process_frame()` or `process()`
- **THEN** the method succeeds (input is automatically made contiguous)

#### Scenario: Errors raise MiniDSPError
- **WHEN** a VAD method is called with invalid parameters (e.g., zero-length signal)
- **THEN** a `MiniDSPError` exception is raised with the appropriate error code

### Requirement: VAD and constants are exported from the public API
`VAD` and `VAD_NUM_FEATURES` SHALL be importable from the top-level `pyminidsp` package.

#### Scenario: Top-level imports
- **WHEN** running `from pyminidsp import VAD, VAD_NUM_FEATURES`
- **THEN** all imports succeed

#### Scenario: Listed in __all__
- **WHEN** inspecting `pyminidsp.__all__`
- **THEN** `"VAD"` and `"VAD_NUM_FEATURES"` are present

### Requirement: Sphinx API documentation for VAD
A new `docs/api/VAD.rst` file SHALL document the `VAD` class and `VAD_NUM_FEATURES` constant using autodoc directives, following the format of existing API reference pages.

#### Scenario: API page renders correctly
- **WHEN** building the Sphinx docs
- **THEN** the VAD API page appears in the documentation with the class, its methods, parameter descriptions, and return types

### Requirement: User guide for VAD
A new `docs/guides/voice-activity-detection.rst` file SHALL provide a tutorial-style guide with usage examples demonstrating initialization, calibration, frame-by-frame processing, and batch processing.

#### Scenario: Guide includes working code examples
- **WHEN** a user follows the guide examples
- **THEN** the code runs successfully and demonstrates VAD on a synthetic signal

### Requirement: Changelog and version update
The changelog (`docs/changelog.rst`) SHALL include an entry for the new version documenting the VAD addition and the C library bump. The package version in `pyproject.toml` SHALL be updated.

#### Scenario: Changelog entry
- **WHEN** reading `docs/changelog.rst`
- **THEN** there is an entry for 0.6.0 that mentions voice activity detection, the `VAD` class, and the miniDSP v0.5.1 upgrade

#### Scenario: Version bump
- **WHEN** reading `pyproject.toml`
- **THEN** the version field reads "0.6.0"
