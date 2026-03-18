## Why

The Sphinx `docs/installation.rst` lists a C compiler and FFTW3 headers as top-level prerequisites, making it look like *every* user needs all of them. In reality, `pip install pyminidsp` pulls a pre-built wheel (Linux x86-64, macOS ARM64) that includes the compiled C extension — no compiler needed. However, FFTW3 is dynamically linked and **is** still required at runtime (the wheel does not bundle it). The current docs conflate build-time and runtime prerequisites and don't distinguish wheel installs from source builds.

The README is structured better (prerequisites live under "Building from Source") but could also be clearer about what wheel users actually need.

## What Changes

- Restructure `docs/installation.rst` so the happy path (pre-built wheel) comes first, noting that only FFTW3 runtime library is needed (no compiler, no FFTW3 *dev headers*). Move C compiler and FFTW3 dev header requirements into a "Building from Source" section.
- Clarify in `README.md` that wheel installs need FFTW3 but not a C compiler.

## Capabilities

### New Capabilities

- `install-docs-clarity`: Restructure installation docs so wheel users see a streamlined path (FFTW3 runtime only, no compiler) and source-build users see the full requirements.

### Modified Capabilities

_(none)_

## Impact

- `docs/installation.rst` — restructured
- `README.md` — minor wording tweak
- No code, API, or dependency changes
