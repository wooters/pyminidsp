## ADDED Requirements

### Requirement: Build uses C17 standard
The build script SHALL pass `-std=c17` (not `-std=c2x` or `-std=c23`) as a compiler flag when compiling the miniDSP C source.

#### Scenario: Compiler flag is C17
- **WHEN** `_build_minidsp.py` configures the CFFI extension
- **THEN** `extra_compile_args` SHALL contain `-std=c17`

### Requirement: miniDSP source pinned to tagged release
All git clone commands for the miniDSP C library SHALL pin to a specific version tag (`v0.1.0`) rather than cloning the default branch HEAD.

#### Scenario: cibuildwheel clones miniDSP at tag
- **WHEN** cibuildwheel runs `before-all` commands on any platform (Linux, macOS, Windows)
- **THEN** the git clone command SHALL include `--branch v0.1.0`

#### Scenario: sdist workflow clones miniDSP at tag
- **WHEN** the `build-sdist` job in `wheels.yml` clones miniDSP
- **THEN** the git clone command SHALL include `--branch v0.1.0`

### Requirement: Compatible manylinux image
The cibuildwheel Linux configuration SHALL NOT require `manylinux_2_28` since C23 support is no longer needed.

#### Scenario: Default manylinux image used
- **WHEN** cibuildwheel builds Linux wheels
- **THEN** the explicit `manylinux_2_28` image overrides SHALL be removed, allowing cibuildwheel to use its default manylinux image

### Requirement: Comments reflect C17
All comments in build configuration files that reference C23 SHALL be updated to reflect C17.

#### Scenario: pyproject.toml comment updated
- **WHEN** reviewing `pyproject.toml` cibuildwheel Linux section
- **THEN** the comment SHALL reference C17, not C23
