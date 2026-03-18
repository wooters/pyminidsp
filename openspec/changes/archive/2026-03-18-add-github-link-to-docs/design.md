## Context

The pyminidsp Sphinx docs use the Furo theme and are deployed to GitHub Pages. The repo URL (`https://github.com/wooters/pyminidsp`) is already defined in `pyproject.toml` but not surfaced in the docs header. Furo provides built-in support for source repository links via `html_theme_options`.

## Goals / Non-Goals

**Goals:**
- Display a clickable GitHub icon in the docs header that links to the repository.

**Non-Goals:**
- Adding "Edit on GitHub" links to individual pages.
- Changing the docs theme or layout beyond the header icon.

## Decisions

**Use Furo's `source_repository` theme option.**
Furo's `html_theme_options` supports `source_repository`, `source_branch`, and `source_directory` keys. Setting `source_repository` alone adds a GitHub icon to the top navigation bar. This is the simplest path — no custom templates or extra extensions needed.

Alternative considered: adding a manual link in `index.rst` or a custom Jinja template override. Rejected because Furo's native option is simpler and stays consistent with theme updates.

## Risks / Trade-offs

- **[Minimal risk]** If the Furo theme is replaced in the future, this option would need to be migrated. → Low likelihood; Furo is the established theme for this project.
