## ADDED Requirements

### Requirement: miniDSP C library pinned to v0.5.2
The build system SHALL clone the miniDSP C library at tag v0.5.2 (not v0.5.1) for all wheel and sdist builds.

#### Scenario: Wheel build clones correct tag
- **WHEN** cibuildwheel runs the `before-all` step
- **THEN** it clones `https://github.com/wooters/miniDSP.git` at branch/tag `v0.5.2`

#### Scenario: Sdist build clones correct tag
- **WHEN** the GitHub Actions sdist job clones the C library source
- **THEN** it clones at tag `v0.5.2`

### Requirement: Package version is 0.6.1
The package SHALL report version 0.6.1 in `pyproject.toml` and documentation.

#### Scenario: pyproject.toml version field
- **WHEN** a user inspects `pyproject.toml`
- **THEN** the `version` field reads `"0.6.1"`

#### Scenario: Sphinx docs version
- **WHEN** the documentation is built
- **THEN** `docs/conf.py` `release` is set to `"0.6.1"`
