## 1. Fix RST substitution errors

- [x] 1.1 Fix `docs/api/analysis.rst:41` — escape `|c|` in RMS description
- [x] 1.2 Fix `docs/guides/basic-signal-operations.rst:18` — escape `|c|` and fix title underline (line 2)
- [x] 1.3 Fix `pyminidsp/_effects.py` — escape `|feedback|` in `delay_echo` and `comb_reverb` docstrings
- [x] 1.4 Fix `pyminidsp/_spectral.py` — escape `|X(k)|` in `magnitude_spectrum` and `|` in `power_spectral_density` docstrings

## 2. Verify

- [x] 2.1 Run `sphinx-build -W` on clean build and confirm zero warnings
