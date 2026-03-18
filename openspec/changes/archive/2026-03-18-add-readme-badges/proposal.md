## Why

The README currently has no status badges, making it harder for visitors to quickly assess project health, version, supported Python versions, and license. Badges are a standard convention for open-source Python packages and improve discoverability and trust.

## What Changes

- Add a row of shields.io / GitHub badges at the top of `README.md`, below the `# pyminidsp` heading:
  - **PyPI version** — links to pypi.org/project/pyminidsp
  - **Python versions** — shows 3.9–3.13 support
  - **License** — MIT
  - **Build wheels** — GitHub Actions status for the `Build wheels` workflow
  - **Docs** — GitHub Actions status for the `Deploy Documentation` workflow

## Capabilities

### New Capabilities
- `readme-badges`: Status, version, and CI badges added to the top of the project README

### Modified Capabilities

(none)

## Impact

- Only `README.md` is modified (cosmetic change, no code impact)
