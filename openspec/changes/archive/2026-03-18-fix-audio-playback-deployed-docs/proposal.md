## Why

Audio snippets (and interactive plots) don't play on the deployed GitHub Pages documentation. They work locally because `docs/` is implicitly on `sys.path`, but in CI the Sphinx build runs from the repo root and `from gen_audio_samples import generate` raises `ImportError`. The broad `except Exception` handler in `conf.py` silently swallows the error, so the build succeeds but produces HTML with `<audio>` tags pointing to non-existent WAV files.

## What Changes

- Fix the `sys.path` setup in `docs/conf.py` so that `gen_audio_samples` and `gen_signal_plots` are importable regardless of the working directory.
- Tighten the exception handling in `conf.py` to surface import/generation failures more visibly (or let them fail the build).

## Capabilities

### New Capabilities

_None — this is a bug fix, not a new capability._

### Modified Capabilities

_None — no spec-level behavior changes._

## Impact

- **`docs/conf.py`** — `sys.path` setup and `_generate_audio` / `_generate_plots` error handling.
- **Deployed docs** — all guide pages with `<audio>` elements will have working playback after the fix.
- **Interactive plots** — same root cause; the fix addresses both audio and plot generation.
