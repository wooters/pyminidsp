## ADDED Requirements

### Requirement: Brickwall lowpass filter
The system SHALL provide a `lowpass_brickwall(signal, cutoff_hz, sample_rate)` function that applies an FFT-based ideal (brickwall) lowpass filter, zeroing all frequency bins above the cutoff.

#### Scenario: Filter a signal with brickwall lowpass
- **WHEN** calling `lowpass_brickwall(signal, cutoff_hz=4000.0, sample_rate=44100.0)`
- **THEN** a float64 NumPy array of the same length as the input is returned

#### Scenario: Frequencies above cutoff are removed
- **WHEN** applying `lowpass_brickwall` with `cutoff_hz=4000.0` to a signal containing 1 kHz and 10 kHz tones
- **THEN** the 1 kHz component is preserved and the 10 kHz component is completely removed

#### Scenario: Function is accessible from top-level
- **WHEN** importing `from pyminidsp import lowpass_brickwall`
- **THEN** the import succeeds and the function is callable
