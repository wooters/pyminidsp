## ADDED Requirements

### Requirement: Kaiser window generation
The system SHALL provide a `kaiser_window(n, beta)` function that generates a Kaiser window of length `n` with shape parameter `beta`, returning a float64 NumPy array.

#### Scenario: Generate a Kaiser window
- **WHEN** calling `kaiser_window(256, beta=5.0)`
- **THEN** a float64 NumPy array of length 256 is returned

#### Scenario: Window peaks at center
- **WHEN** generating a Kaiser window of length 256
- **THEN** the maximum value is at or near the center of the array

#### Scenario: Window is symmetric
- **WHEN** generating a Kaiser window of length 256
- **THEN** the window values are symmetric around the center

#### Scenario: Function is accessible from top-level
- **WHEN** importing `from pyminidsp import kaiser_window`
- **THEN** the import succeeds and the function is callable

### Requirement: STEG_SPECTEXT constant
The system SHALL export a `STEG_SPECTEXT = 2` constant for the hybrid LSB + spectrogram text steganography method.

#### Scenario: Constant is accessible from top-level
- **WHEN** importing `from pyminidsp import STEG_SPECTEXT`
- **THEN** the value is 2
