## Why

The README.md (which renders as the PyPI project description) contains installation instructions written for developers building from source — clone the C library, set `MINIDSP_SRC`, use `uv sync`. Users discovering pyminidsp on PyPI expect to run `pip install pyminidsp` with pre-built wheels and find these instructions confusing and misleading. Additionally, the API Overview table is incomplete — ~20 public functions (window functions, scaling utilities, `mix`, `dot`, `entropy`, etc.) are exported but undocumented in the README.

## What Changes

- Restructure README installation section: lead with `pip install pyminidsp` for end users, move source/development build instructions to a secondary section
- Remove prerequisite section's prominence (FFTW3/compiler not needed for wheel installs)
- Add missing function categories to the API Overview: Window Functions, Signal Scaling, and additional utility functions (`mix`, `dot`, `entropy`, `convolution_num_samples`, `stft_num_frames`, `dtmf_signal_length`, `steg_capacity`, `get_multiple_delays`)
- Keep the README concise — full docs live at the documentation site

## Capabilities

### New Capabilities
- `pypi-friendly-readme`: README content is structured for PyPI visitors — install via pip first, build-from-source second, complete API overview

### Modified Capabilities

(none)

## Impact

- `README.md` — primary file being rewritten
- PyPI project page — will reflect changes on next release
- No code changes, no API changes, no dependency changes
