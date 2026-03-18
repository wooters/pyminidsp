### Requirement: Wheel install section lists only runtime prerequisites
The `docs/installation.rst` page SHALL present the wheel install as the primary method. It SHALL list FFTW3 runtime library as the only prerequisite (not dev headers, not a C compiler). It SHALL include platform-specific install commands for the FFTW3 runtime library (e.g., `apt install libfftw3-3`, `brew install fftw`).

#### Scenario: User reads installation page
- **WHEN** a user opens the installation docs
- **THEN** the first install path they see is the wheel install, which lists only the FFTW3 runtime library as a prerequisite and does not mention a C compiler or FFTW3 dev headers

#### Scenario: Supported platforms are listed
- **WHEN** a user reads the wheel install section
- **THEN** the supported platforms (Linux x86-64, macOS ARM64) and Python versions (3.9–3.13) SHALL be listed

#### Scenario: No C compiler mentioned in wheel path
- **WHEN** a user reads the wheel install section
- **THEN** there SHALL be no mention of a C compiler as a requirement

### Requirement: Source-build prerequisites are scoped to their own section
The C compiler, FFTW3 development headers, and `MINIDSP_SRC` requirements SHALL appear only under a "Building from Source" section, not at the top of the page.

#### Scenario: Prerequisites not shown at top level
- **WHEN** a user reads `docs/installation.rst`
- **THEN** there SHALL be no top-level "Prerequisites" section listing a C compiler or FFTW3 dev headers

#### Scenario: Source-build section contains all build requirements
- **WHEN** a user navigates to the "Building from Source" section
- **THEN** it SHALL list FFTW3 development headers, a C compiler, and the `MINIDSP_SRC` environment variable as prerequisites

### Requirement: README clarifies wheel install prerequisites
The `README.md` SHALL include a note under the "Installation" heading that pre-built wheels require the FFTW3 library but no C compiler.

#### Scenario: README installation section
- **WHEN** a user reads the Installation section of `README.md`
- **THEN** they SHALL see a note that pre-built wheels require FFTW3 at runtime but do not require a C compiler
