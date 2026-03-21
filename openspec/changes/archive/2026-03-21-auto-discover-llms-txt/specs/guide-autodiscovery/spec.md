## ADDED Requirements

### Requirement: Discover guides from toctree
The script SHALL determine which guide RST files to include and their
presentation order by parsing the `toctree` directive in
`docs/guides/index.rst` instead of using a hardcoded list.

#### Scenario: New guide added to toctree
- **WHEN** a new entry `my-new-guide` is added to the toctree in `docs/guides/index.rst` and `docs/guides/my-new-guide.rst` exists
- **THEN** the script includes it in `llms-full.txt` at the position specified in the toctree, without any manual registration in the script

#### Scenario: Guide removed from toctree
- **WHEN** a guide slug is removed from the toctree in `docs/guides/index.rst`
- **THEN** the script no longer includes that guide in the output

### Requirement: Preserve toctree ordering
The script SHALL present guides in the same order they appear in the
`toctree` directive.

#### Scenario: Order matches toctree
- **WHEN** the toctree lists `signal-generators`, `basic-signal-operations`, `window-functions`
- **THEN** the tutorials section of `llms-full.txt` presents them in that exact order

### Requirement: Warn on missing guide files
The script SHALL emit a warning to stderr if a slug listed in the toctree
has no corresponding `.rst` file, and continue processing the remaining guides.

#### Scenario: Missing RST file
- **WHEN** the toctree contains `nonexistent-guide` but `docs/guides/nonexistent-guide.rst` does not exist
- **THEN** the script prints a warning to stderr and skips that entry
