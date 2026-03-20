## Why

AI coding agents increasingly look for `llms.txt` and `llms-full.txt` files to quickly understand a library's purpose and API. The miniDSP C library already ships these files, but pyminidsp — the primary way most users interact with miniDSP — does not. Adding them will make it easy for AI agents to write correct pyminidsp code without manually crawling docs or source.

## What Changes

- Add a Python script (`scripts/gen_llms_txt.py`) that generates `llms.txt` and `llms-full.txt` from the existing Sphinx documentation and Python docstrings.
- `llms.txt`: concise project summary with a pointer to the full reference.
- `llms-full.txt`: complete API reference (all ~65 public functions organized by category) plus tutorial content extracted from the 15 existing guides.
- Integrate generation into the Sphinx docs build so the files are deployed alongside the documentation at `https://wooters.github.io/pyminidsp/`.

## Capabilities

### New Capabilities
- `llms-txt-generation`: A script that introspects pyminidsp's public API and parses RST guide files to produce `llms.txt` and `llms-full.txt`.

### Modified Capabilities
<!-- None — this is purely additive. -->

## Impact

- **New files**: `scripts/gen_llms_txt.py`
- **Modified files**: docs build step (Makefile or CI workflow) to call the generation script; output written to Sphinx build directory
- **Dependencies**: None beyond what the project already uses (Python stdlib `inspect`, `importlib`, plus `docutils` or direct RST parsing)
- **Risk**: Low — no changes to library code or public API
