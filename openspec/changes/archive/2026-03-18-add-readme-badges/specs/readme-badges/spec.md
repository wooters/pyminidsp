## ADDED Requirements

### Requirement: README displays PyPI version badge
The README SHALL display a shields.io badge showing the current PyPI version of `pyminidsp`, linking to the PyPI project page.

#### Scenario: Visitor sees current version
- **WHEN** a visitor views the README on GitHub
- **THEN** they see a badge showing the latest PyPI version (e.g., "v0.5.0") that links to `https://pypi.org/project/pyminidsp/`

### Requirement: README displays Python version badge
The README SHALL display a shields.io badge showing supported Python versions (3.9–3.13), linking to the PyPI project page.

#### Scenario: Visitor sees supported Python versions
- **WHEN** a visitor views the README on GitHub
- **THEN** they see a badge indicating Python 3.9–3.13 support

### Requirement: README displays license badge
The README SHALL display a shields.io badge showing the MIT license, linking to the PyPI project page.

#### Scenario: Visitor sees license
- **WHEN** a visitor views the README on GitHub
- **THEN** they see a badge showing "MIT" as the license

### Requirement: README displays Build wheels workflow status badge
The README SHALL display a GitHub Actions status badge for the `Build wheels` workflow (`wheels.yml`), linking to the workflow runs page.

#### Scenario: Visitor sees CI status
- **WHEN** a visitor views the README on GitHub
- **THEN** they see a badge showing the current status (passing/failing) of the Build wheels workflow

### Requirement: README displays Docs workflow status badge
The README SHALL display a GitHub Actions status badge for the `Deploy Documentation` workflow (`docs.yml`), linking to the workflow runs page.

#### Scenario: Visitor sees docs build status
- **WHEN** a visitor views the README on GitHub
- **THEN** they see a badge showing the current status of the Deploy Documentation workflow

### Requirement: Badges are placed below the heading
All badges SHALL appear on a single line immediately after the `# pyminidsp` heading, before the documentation link.

#### Scenario: Badge placement
- **WHEN** a visitor views the README
- **THEN** badges appear between the `# pyminidsp` heading and the `**[Documentation](...)**` line
