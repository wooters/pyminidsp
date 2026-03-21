## ADDED Requirements

### Requirement: Discover API modules automatically
The script SHALL discover API modules by scanning for `pyminidsp/_*.py` files
at runtime instead of using a hardcoded list. It SHALL exclude infrastructure
modules (`__init__.py`, `_build_minidsp.py`, `_core.py`).

#### Scenario: New module added
- **WHEN** a new file `pyminidsp/_foo.py` exists with a docstring and exports symbols via `__all__`
- **THEN** the script includes its symbols in the generated `llms-full.txt` without any manual registration

#### Scenario: Infrastructure modules excluded
- **WHEN** the script scans `pyminidsp/`
- **THEN** it skips `__init__.py`, `_build_minidsp.py`, and `_core.py`

### Requirement: Derive category names from module docstrings
The script SHALL use the first line of each module's docstring as the category
display name in the API reference section.

#### Scenario: Module with docstring
- **WHEN** `pyminidsp/_effects.py` has docstring `"""Simple audio effects: delay/echo, tremolo, comb reverb."""`
- **THEN** its category display name is `Simple audio effects: delay/echo, tremolo, comb reverb.`

#### Scenario: Module without docstring
- **WHEN** a discovered module has no docstring
- **THEN** the script emits a warning to stderr and uses a title-cased version of the filename as the category name (e.g. `_foo.py` → `Foo`)

### Requirement: Sort modules alphabetically
The script SHALL present discovered modules in alphabetical order by filename.

#### Scenario: Alphabetical ordering
- **WHEN** modules `_analysis.py`, `_effects.py`, `_dtmf.py` are discovered
- **THEN** they appear in the output in order: `_analysis`, `_dtmf`, `_effects`
