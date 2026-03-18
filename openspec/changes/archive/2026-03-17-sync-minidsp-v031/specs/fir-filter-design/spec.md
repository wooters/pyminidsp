## ADDED Requirements

### Requirement: Design lowpass FIR filter
The system SHALL provide a `design_lowpass_fir(num_taps, cutoff_freq, sample_rate, kaiser_beta)` function that returns a NumPy float64 array of FIR filter coefficients for a Kaiser-windowed sinc lowpass filter.

#### Scenario: Design a 64-tap lowpass filter
- **WHEN** calling `design_lowpass_fir(num_taps=64, cutoff_freq=4000.0, sample_rate=44100.0, kaiser_beta=5.0)`
- **THEN** a float64 NumPy array of length 64 is returned containing the filter coefficients

#### Scenario: Resulting filter attenuates above cutoff
- **WHEN** applying the designed filter to a signal containing 1 kHz and 10 kHz tones with `cutoff_freq=4000.0`
- **THEN** the 1 kHz component is preserved and the 10 kHz component is significantly attenuated

#### Scenario: Function is accessible from top-level
- **WHEN** importing `from pyminidsp import design_lowpass_fir`
- **THEN** the import succeeds and the function is callable
