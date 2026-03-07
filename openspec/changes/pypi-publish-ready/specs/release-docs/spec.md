## ADDED Requirements

### Requirement: Release process is documented
A `RELEASING.md` file SHALL describe the end-to-end release process from version bump to PyPI publication.

#### Scenario: Developer reads release instructions
- **WHEN** a developer opens `RELEASING.md`
- **THEN** they find step-by-step instructions covering: version bump in `pyproject.toml`, creating a git tag, pushing the tag, and verifying the release on PyPI

### Requirement: TestPyPI validation step documented
`RELEASING.md` SHALL include instructions for validating on TestPyPI before a production release.

#### Scenario: First-time release
- **WHEN** a developer is making their first release
- **THEN** `RELEASING.md` explains how to push a pre-release tag to trigger TestPyPI and how to verify the package installs correctly from TestPyPI
