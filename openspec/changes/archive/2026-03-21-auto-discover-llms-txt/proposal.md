## Why

Every time a new module or guide is added to pyminidsp, the developer must also
remember to register it in `MODULE_CATEGORIES` and `GUIDE_ORDER` inside
`scripts/gen_llms_txt.py`. This manual step is easy to forget and has already
caused omissions. The fix is straightforward: scan the filesystem for
`pyminidsp/_*.py` modules and `docs/guides/*.rst` files instead of maintaining
hardcoded lists.

## What Changes

- **Remove `MODULE_CATEGORIES` list** — replace with automatic discovery of
  `pyminidsp/_*.py` files (excluding `__init__.py`, `_build_minidsp.py`, and
  `_core.py`). Category display names will be derived from each module's
  docstring (first line) or, as a fallback, from the filename.
- **Remove `GUIDE_ORDER` list** — replace with automatic discovery that reads
  the `toctree` directive in `docs/guides/index.rst` to determine which guides
  exist and their presentation order. This keeps the single source of truth in
  the Sphinx docs rather than duplicating it.
- **Add warnings** when a discovered module has no docstring (prompting the
  developer to add one for a good category name).

## Capabilities

### New Capabilities
- `module-autodiscovery`: Automatically discover `pyminidsp/_*.py` modules and derive display category names from module docstrings
- `guide-autodiscovery`: Automatically discover guide RST files by parsing the `toctree` in `docs/guides/index.rst`

### Modified Capabilities

_(none — no existing spec-level requirements change)_

## Impact

- **Code**: `scripts/gen_llms_txt.py` — the two hardcoded lists are removed and
  replaced with discovery functions. The rest of the script (API extraction, RST
  conversion, rendering) is unchanged.
- **Module docstrings**: Each `pyminidsp/_*.py` module needs a first-line
  docstring that serves as the category display name. Most already have one; any
  that don't will trigger a warning.
- **No API or dependency changes**.
