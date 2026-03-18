## ADDED Requirements

### Requirement: Guide documents all three steganography methods
The Audio Steganography guide SHALL describe three methods — LSB, Frequency-band, and Spectrogram Text (STEG_SPECTEXT) — with a comparison table covering capacity, audibility, robustness, and requirements for each.

#### Scenario: Comparison table includes SPECTEXT row
- **WHEN** a user reads the Audio Steganography guide
- **THEN** the comparison table contains a row for STEG_SPECTEXT with its characteristics

#### Scenario: Guide heading reflects three methods
- **WHEN** a user reads the methods section heading
- **THEN** it says "Three methods" (not "Two methods")

### Requirement: Guide includes SPECTEXT code example
The guide SHALL include a code example showing how to encode and decode a message using `method=md.STEG_SPECTEXT`.

#### Scenario: SPECTEXT encode/decode example present
- **WHEN** a user reads the "Hiding text" section
- **THEN** they find example code using `md.STEG_SPECTEXT` as the method parameter

### Requirement: Guide cross-references Spectrogram Text Art guide and miniDSP C library docs
The guide SHALL include cross-references to both the local Spectrogram Text Art guide and the upstream miniDSP C library's steganography documentation for users who want deeper detail.

#### Scenario: Local cross-reference present
- **WHEN** a user reads the SPECTEXT description in the guide
- **THEN** they find a link or seealso directive pointing to the local Spectrogram Text Art guide

#### Scenario: Upstream C library cross-reference present
- **WHEN** a user reads the SPECTEXT description in the guide
- **THEN** they find a link to the miniDSP C library steganography docs at `https://wooters.github.io/miniDSP/audio-steganography.html`

### Requirement: Detection example handles three methods
The automatic detection code example SHALL handle all three methods, not just LSB and Frequency-band.

#### Scenario: Detection example shows SPECTEXT case
- **WHEN** a user reads the "Automatic detection" section
- **THEN** the code example includes a case for `md.STEG_SPECTEXT`

### Requirement: API reference lists STEG_SPECTEXT as valid method
The API reference (`docs/api/steganography.rst`) SHALL list `STEG_SPECTEXT` alongside `STEG_LSB` and `STEG_FREQ_BAND` in all method parameter descriptions.

#### Scenario: steg_encode param docs include SPECTEXT
- **WHEN** a user reads the `steg_encode` API docs
- **THEN** the method parameter description lists `STEG_SPECTEXT` as a valid value

#### Scenario: steg_encode_bytes param docs include SPECTEXT
- **WHEN** a user reads the `steg_encode_bytes` API docs
- **THEN** the method parameter description lists `STEG_SPECTEXT` as a valid value

### Requirement: All audio and plot assets load in the built guide
All embedded audio players and interactive plot iframes in the Audio Steganography guide SHALL load correctly in the built HTML output.

#### Scenario: Audio players are functional
- **WHEN** a user opens the built Audio Steganography guide in a browser
- **THEN** all `<audio>` elements load their WAV source files and are playable

#### Scenario: Plot iframes render
- **WHEN** a user opens the built Audio Steganography guide in a browser
- **THEN** all `<iframe>` elements load their Plotly HTML plots and display correctly

#### Scenario: Relative paths resolve from guides subdirectory
- **WHEN** the guide is built at `guides/audio-steganography.html`
- **THEN** relative paths like `../_static/audio/*.wav` and `../_static/plots/*.html` resolve to existing files in the build output
