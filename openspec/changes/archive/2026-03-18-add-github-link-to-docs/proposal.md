## Why

The Sphinx docs (hosted on GitHub Pages) don't include a visible link back to the GitHub repository. Users reading the docs have no quick way to jump to the source code, file issues, or contribute. The Furo theme natively supports a header icon/link for this — it just needs to be configured.

## What Changes

- Add `html_theme_options` to `docs/conf.py` with Furo's built-in GitHub URL and icon settings, placing a clickable GitHub icon in the docs header.

## Capabilities

### New Capabilities
- `docs-github-link`: Add a GitHub repository link to the Sphinx documentation header via Furo theme options.

### Modified Capabilities
<!-- None — no existing spec-level behavior is changing. -->

## Impact

- **Code**: `docs/conf.py` only — a small addition to theme options.
- **Dependencies**: None — Furo already supports this natively.
- **Systems**: The change will be visible on the next GitHub Pages deploy.
