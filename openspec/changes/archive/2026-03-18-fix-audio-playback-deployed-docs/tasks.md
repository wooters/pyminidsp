## 1. Fix module import path

- [x] 1.1 Add `sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))` to `docs/conf.py` so that `gen_audio_samples` and `gen_signal_plots` are importable from any working directory

## 2. Tighten error handling

- [x] 2.1 In `_generate_audio()`, change `except Exception` to `except ImportError` so non-import errors propagate
- [x] 2.2 In `_generate_plots()`, change `except Exception` to `except ImportError` so non-import errors propagate

## 3. Verify

- [x] 3.1 Run `sphinx-build` from the repo root (matching CI invocation) and confirm audio files appear in `docs/_build/html/_static/audio/`
- [x] 3.2 Run `sphinx-build` from the repo root and confirm plot files appear in `docs/_build/html/_static/plots/`
