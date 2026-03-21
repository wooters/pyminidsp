## Context

`scripts/gen_llms_txt.py` generates `llms.txt` and `llms-full.txt` for AI agent
consumption. It currently relies on two hardcoded lists:

- `MODULE_CATEGORIES` — maps each `pyminidsp/_*.py` module to a display name
- `GUIDE_ORDER` — lists guide slugs in presentation order

Both must be updated manually when a new module or guide is added, which is
error-prone. The rest of the script (API extraction, RST conversion, rendering)
is unaffected by this change.

All `pyminidsp/_*.py` modules already have a one-line docstring that describes
their purpose. The guide presentation order is already defined in
`docs/guides/index.rst` via a `toctree` directive.

## Goals / Non-Goals

**Goals:**
- Eliminate the two hardcoded lists so new modules/guides are picked up
  automatically
- Use existing sources of truth: module docstrings for category names,
  `index.rst` toctree for guide order
- Maintain identical output for the current set of modules and guides
  (no change to the generated files)

**Non-Goals:**
- Changing the output format of `llms.txt` or `llms-full.txt`
- Modifying module docstrings (they're already suitable)
- Auto-generating `index.rst` or changing Sphinx configuration
- Supporting modules outside the `pyminidsp/` directory

## Decisions

### 1. Module discovery: scan `pyminidsp/_*.py` + use docstrings

**Decision**: Glob for `pyminidsp/_*.py`, exclude the known infrastructure
files (`__init__.py`, `_build_minidsp.py`, `_core.py`), import each module, and
use its `__doc__` first line as the category display name.

**Alternative considered**: Use a naming convention (e.g. `_analysis.py` →
"Analysis") to avoid importing. Rejected because the existing docstrings are
richer and more descriptive, and the script already imports pyminidsp anyway.

**Ordering**: Modules will be sorted alphabetically by filename. The current
`MODULE_CATEGORIES` order is arbitrary and not user-visible in a meaningful way
(AI agents don't care about section order). If a specific order is later
desired, an optional `LLMS_ORDER` attribute could be added to modules, but this
is not needed now.

### 2. Guide discovery: parse `index.rst` toctree

**Decision**: Read `docs/guides/index.rst`, extract the entries from the
`toctree` directive, and use those as the guide slugs in order. This preserves
the Sphinx-defined ordering without duplicating it.

**Alternative considered**: Glob for `docs/guides/*.rst` and sort
alphabetically. Rejected because the toctree order is pedagogically meaningful
(basics before advanced topics) and is already maintained as part of the Sphinx
docs workflow.

### 3. Exclusion list for infrastructure modules

**Decision**: Hardcode a small `_SKIP_MODULES` set: `{"__init__",
"_build_minidsp", "_core"}`. These are infrastructure, not API modules.

**Rationale**: This is a stable, rarely-changing set. A heuristic (e.g. "skip
if no `__all__`") would be fragile. Three explicit names is clearer than any
convention.

## Risks / Trade-offs

- **[Module without docstring]** → Emit a warning to stderr and fall back to a
  title-cased version of the filename (e.g. `_foo.py` → "Foo"). This prevents
  silent breakage while nudging the developer to add a docstring.
- **[Toctree parsing brittleness]** → The parser only needs to find indented
  lines after `.. toctree::` (skipping options like `:maxdepth:`). RST toctree
  format is stable and we control the file. Risk is low.
- **[Ordering change]** → Switching modules from the current manual order to
  alphabetical changes section order in `llms-full.txt`. This is acceptable
  since AI agents consume these files and don't depend on section order.
