## ADDED Requirements

### Requirement: Package exposes __version__
`pyminidsp.__version__` SHALL return the package version string matching the version in `pyproject.toml`.

#### Scenario: Access version at runtime
- **WHEN** a user runs `import pyminidsp; print(pyminidsp.__version__)`
- **THEN** the output matches the version declared in `pyproject.toml` (e.g., `"0.1.0"`)

#### Scenario: Version available after pip install
- **WHEN** the package is installed via `pip install`
- **THEN** `pyminidsp.__version__` returns the installed version
