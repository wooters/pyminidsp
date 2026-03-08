## Context

The README.md serves double duty: it's the repo landing page on GitHub and the project description on PyPI. Currently it's written entirely from a developer/contributor perspective — requiring users to clone the C library, set environment variables, and build from source. Since v0.2.0, pre-built wheels are published for Linux x86-64 and macOS ARM64 (Python 3.9–3.13), making `pip install pyminidsp` the standard install path.

## Goals / Non-Goals

**Goals:**
- Make `pip install pyminidsp` the primary, prominent installation method
- Document build-from-source as a secondary path for contributors or unsupported platforms
- List all publicly exported functions in the API Overview
- Keep the README concise — link to full docs site for details

**Non-Goals:**
- Rewriting the documentation site
- Changing any Python or C code
- Changing pyproject.toml metadata (classifiers, URLs, etc. are correct)

## Decisions

1. **Single file change (README.md only)** — The pyproject.toml metadata, classifiers, and URLs are all accurate. The only problem is the README content that renders on PyPI.

2. **Installation section structure**: Lead with a simple `pip install pyminidsp` code block. Add a "Platform support" note listing wheel availability. Move the build-from-source instructions into a collapsible "Building from source" section or clearly labeled subsection.

3. **Prerequisites split**: Move FFTW3/compiler prerequisites into the build-from-source section only. Wheel users need no prerequisites beyond Python ≥ 3.9.

4. **API Overview completeness**: Add three missing table sections — Window Functions (4 functions), Signal Scaling (4 functions), Signal Measurement (3 functions: `dot`, `entropy`, `mix`). Add missing utility functions as notes under their parent sections (`convolution_num_samples`, `stft_num_frames`, `dtmf_signal_length`, `steg_capacity`, `get_multiple_delays`).

## Risks / Trade-offs

- [README gets longer with more API tables] → Acceptable; completeness matters more on PyPI. Users scan tables quickly.
- [Build-from-source less prominent] → Intentional. Contributors will find it. Link to CONTRIBUTING or the docs site if needed.
