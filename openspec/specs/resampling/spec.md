## ADDED Requirements

### Requirement: Compute resampled output length
The system SHALL provide a `resample_output_len(input_len, in_rate, out_rate)` function that returns the number of output samples for a given resampling operation.

#### Scenario: Upsample length calculation
- **WHEN** calling `resample_output_len(1000, 22050.0, 44100.0)`
- **THEN** the result is 2000 (double the input length)

#### Scenario: Downsample length calculation
- **WHEN** calling `resample_output_len(1000, 44100.0, 22050.0)`
- **THEN** the result is 500 (half the input length)

### Requirement: Resample a signal
The system SHALL provide a `resample(signal, in_rate, out_rate, num_zero_crossings=13, kaiser_beta=5.0)` function that performs polyphase sinc resampling with Kaiser-windowed anti-aliasing.

#### Scenario: Upsample 22050 Hz to 44100 Hz
- **WHEN** calling `resample(signal, in_rate=22050.0, out_rate=44100.0)` on a 1000-sample input
- **THEN** a float64 NumPy array of approximately 2000 samples is returned

#### Scenario: Downsample preserves content below Nyquist
- **WHEN** downsampling a signal containing a 1 kHz tone from 44100 Hz to 22050 Hz
- **THEN** the 1 kHz tone is preserved in the output

#### Scenario: Output buffer is auto-sized
- **WHEN** calling `resample(signal, in_rate, out_rate)` without specifying buffer sizes
- **THEN** the wrapper internally computes the output length via `resample_output_len` and allocates the correct buffer

#### Scenario: Functions are accessible from top-level
- **WHEN** importing `from pyminidsp import resample, resample_output_len`
- **THEN** the imports succeed and the functions are callable
