## ADDED Requirements

### Requirement: Docs build generates audio and plots in CI

The Sphinx build SHALL successfully generate audio samples and interactive plots when run from any working directory, including the CI environment where `sphinx-build` is invoked from the repository root.

#### Scenario: CI build generates audio files
- **WHEN** `sphinx-build` is run from the repo root (as in the GitHub Actions workflow)
- **THEN** `gen_audio_samples.generate()` executes successfully and WAV files are present in the build output at `_static/audio/`

#### Scenario: CI build generates plot files
- **WHEN** `sphinx-build` is run from the repo root
- **THEN** `gen_signal_plots.generate()` executes successfully and HTML plot files are present in the build output at `_static/plots/`

### Requirement: Generation failures are surfaced

The build SHALL NOT silently swallow errors from audio or plot generation (other than `ImportError` for optional dependencies).

#### Scenario: Generation raises a non-import error
- **WHEN** `generate()` raises an exception that is not `ImportError`
- **THEN** the exception propagates and the Sphinx build fails with a visible error message
