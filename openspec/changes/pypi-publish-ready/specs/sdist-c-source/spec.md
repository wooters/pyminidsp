## ADDED Requirements

### Requirement: Sdist includes C source
The sdist SHALL contain the miniDSP C source files under `vendor/miniDSP/` so that `pip install` from the sdist works without setting `MINIDSP_SRC`.

#### Scenario: Install from sdist without MINIDSP_SRC
- **WHEN** a user runs `pip install pyminidsp-0.1.0.tar.gz` without `MINIDSP_SRC` set
- **THEN** the build succeeds using the bundled C source in `vendor/miniDSP/`

#### Scenario: MINIDSP_SRC overrides bundled source
- **WHEN** a user sets `MINIDSP_SRC=/custom/path` and builds from sdist
- **THEN** the build uses the C source at `/custom/path` instead of the bundled copy

### Requirement: Build script resolves C source path
`_build_minidsp.py` SHALL look for the C source in this order:
1. `MINIDSP_SRC` environment variable (if set)
2. `vendor/miniDSP/` relative to the project root

#### Scenario: MINIDSP_SRC set
- **WHEN** `MINIDSP_SRC` is set to a valid path
- **THEN** that path is used for C source compilation

#### Scenario: Fallback to vendor directory
- **WHEN** `MINIDSP_SRC` is not set and `vendor/miniDSP/` exists
- **THEN** `vendor/miniDSP/` is used for C source compilation

#### Scenario: Neither source available
- **WHEN** `MINIDSP_SRC` is not set and `vendor/miniDSP/` does not exist
- **THEN** the build fails with a clear error message explaining how to provide the C source

### Requirement: CI sdist job bundles C source
The CI sdist build job SHALL copy the cloned miniDSP source into `vendor/miniDSP/` before building the sdist, and `MANIFEST.in` SHALL include `vendor/miniDSP/`.

#### Scenario: CI builds sdist with bundled source
- **WHEN** the CI sdist job runs
- **THEN** the resulting `.tar.gz` contains `vendor/miniDSP/` with the C source files
