## ADDED Requirements

### Requirement: Pre-release tags publish to TestPyPI
The CI workflow SHALL publish packages to TestPyPI when a pre-release tag is pushed (matching `v*rc*`, `v*a*`, or `v*b*`).

#### Scenario: Push a release candidate tag
- **WHEN** a tag like `v0.1.0rc1` is pushed
- **THEN** wheels and sdist are built and published to TestPyPI (not production PyPI)

#### Scenario: Push a stable release tag
- **WHEN** a tag like `v0.1.0` is pushed (no pre-release suffix)
- **THEN** wheels and sdist are published to production PyPI only

### Requirement: Twine check validates packages
The CI workflow SHALL run `twine check` on built distributions to verify metadata and README rendering before publishing.

#### Scenario: README renders correctly
- **WHEN** the sdist and wheels are built
- **THEN** `twine check dist/*` passes with no warnings

#### Scenario: Malformed metadata detected
- **WHEN** `twine check` finds rendering issues
- **THEN** the CI job fails before any publishing step runs
