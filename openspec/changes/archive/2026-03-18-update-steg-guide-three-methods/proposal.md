## Why

The Audio Steganography guide and API reference both say "Two methods" (LSB and Frequency-band), but `STEG_SPECTEXT` (method 2) was added in v0.5.0 as a hybrid LSB + spectrogram text encoding method. The docs are out of date and don't mention this third method anywhere in the steganography pages. Users won't discover it unless they happen to find the separate Spectrogram Text Art guide or read the constants reference.

## What Changes

- Update the guide (`docs/guides/audio-steganography.rst`) heading from "Two methods" to "Three methods" and add a row for STEG_SPECTEXT in the comparison table
- Add a brief description of how SPECTEXT works, with a code example and cross-reference to the Spectrogram Text Art guide
- Update the automatic detection code example to handle the third method
- Update the API reference (`docs/api/steganography.rst`) to mention STEG_SPECTEXT as a valid method alongside LSB and FREQ_BAND in parameter docs

## Capabilities

### New Capabilities

_(none — this is a documentation-only change)_

### Modified Capabilities

_(no spec-level behavior changes — the code already supports STEG_SPECTEXT; only the docs need updating)_

## Impact

- `docs/guides/audio-steganography.rst` — guide text, comparison table, code examples
- `docs/api/steganography.rst` — method parameter descriptions
- No code changes, no API changes, no breaking changes
