## ADDED Requirements

### Requirement: pip install is the primary installation method
The README SHALL present `pip install pyminidsp` as the first and most prominent installation method. It SHALL NOT require users to clone a C library or set environment variables for standard installation.

#### Scenario: PyPI visitor reads installation section
- **WHEN** a user visits the PyPI page and reads the Installation section
- **THEN** the first instruction they see is `pip install pyminidsp` with no prerequisites

#### Scenario: Platform support is documented
- **WHEN** a user reads the installation section
- **THEN** they see which platforms have pre-built wheels (Linux x86-64, macOS ARM64) and which Python versions are supported (3.9–3.13)

### Requirement: Build-from-source is a secondary section
The README SHALL include build-from-source instructions in a clearly separate subsection below the primary install method. This section SHALL list prerequisites (FFTW3, C compiler, miniDSP C library clone, `MINIDSP_SRC` env var).

#### Scenario: Contributor finds build instructions
- **WHEN** a developer wants to build from source or contribute
- **THEN** they find a "Building from Source" subsection with all necessary steps including prerequisites

### Requirement: API Overview lists all public functions
The README API Overview SHALL document all publicly exported functions and classes from `pyminidsp`. This includes Window Functions, Signal Scaling, and Signal Measurement categories that are currently missing.

#### Scenario: User checks if a function exists
- **WHEN** a user looks at the API Overview on PyPI
- **THEN** every function available via `import pyminidsp as md; dir(md)` (excluding private/dunder attributes) is listed in a categorized table

#### Scenario: Missing categories are added
- **WHEN** the README is updated
- **THEN** it includes tables for Window Functions (`hann_window`, `hamming_window`, `blackman_window`, `rect_window`), Signal Scaling (`scale`, `scale_vec`, `fit_within_range`, `adjust_dblevel`), and Signal Measurement (`dot`, `entropy`, `mix`)
