## Why

The Sphinx docs build fails with `-W` (warnings-as-errors) due to 7 RST substitution errors where `|...|` in prose text is interpreted as a substitution reference. This prevents using strict doc builds in CI.

## What Changes

- Escape `|` characters in RST prose across 4 files (3 Python docstrings, 2 RST files)
- Fix one underline-too-short warning in `basic-signal-operations.rst`

Specific warnings:
1. `docs/api/analysis.rst:41` — `|c|` in "RMS = |c|"
2. `docs/guides/basic-signal-operations.rst:18` — `|c|`
3. `docs/guides/basic-signal-operations.rst:2` — title underline too short
4. `pyminidsp/_effects.py` — `|feedback|` in `delay_echo` and `comb_reverb` docstrings
5. `pyminidsp/_spectral.py` — `|X(k)|` in `magnitude_spectrum` docstring, `|` in `power_spectral_density` docstring

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- None

## Impact

- **Documentation only** — no code logic changes, only docstring text and RST files
- Enables `sphinx-build -W` for strict doc validation
