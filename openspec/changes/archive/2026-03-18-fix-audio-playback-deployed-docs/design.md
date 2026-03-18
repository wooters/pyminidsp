## Context

The Sphinx docs build hooks (`builder-inited`) call `from gen_audio_samples import generate` and `from gen_signal_plots import generate` to produce WAV files and HTML plots at build time. Locally this works because the user's working directory or Sphinx internals put `docs/` on `sys.path`. In CI, `sphinx-build` runs from the repo root and `docs/` is not on `sys.path`, so both imports fail with `ModuleNotFoundError`. The `except Exception` handler in `conf.py` silently swallows the error.

## Goals / Non-Goals

**Goals:**
- Audio and plot generation works in CI exactly as it does locally.
- Build failures in generation are visible, not silently swallowed.

**Non-Goals:**
- Changing how audio/plots are generated or embedded.
- Committing generated files to git.

## Decisions

### Add `docs/` directory to `sys.path` in `conf.py`

Add `sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))` at the top of `conf.py`. This ensures `gen_audio_samples` and `gen_signal_plots` are importable regardless of the working directory used to invoke `sphinx-build`.

**Alternative considered:** Change the CI command to `cd docs && uv run sphinx-build ...`. Rejected because it's fragile — the fix belongs in `conf.py` so it works for any invocation.

**Alternative considered:** Convert `gen_audio_samples.py` to a Sphinx extension with proper entry points. Over-engineered for this fix.

### Tighten exception handling

Change the `except Exception` to `except ImportError` and let other errors propagate. This surfaces real failures while still gracefully handling environments where pyminidsp isn't installed (e.g., a docs-only build without the C extension).

## Risks / Trade-offs

- [Risk] Changing `except Exception` to `except ImportError` could break builds if `generate()` raises a non-import error. → Mitigation: This is the desired behavior — generation failures should be visible, not silent.
