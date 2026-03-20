## Context

pyminidsp is a Python CFFI wrapper around the miniDSP C library. It exposes ~65 public functions across 8 domain modules (analysis, effects, filters, spectral, generators, dtmf, gcc, resampling, steganography). The project already has comprehensive Sphinx documentation: 16 API reference pages and 15 tutorial guides.

The miniDSP C library recently added `llms.txt` and `llms-full.txt` via a Python script (`scripts/gen_llms_txt.py`) that parses Doxygen XML output and guide markdown files. pyminidsp needs equivalent files, but the source format differs — Python docstrings + RST instead of C headers + Doxygen XML.

## Goals / Non-Goals

**Goals:**
- Generate `llms.txt` (concise index) and `llms-full.txt` (full API + tutorials) for pyminidsp
- Use a standalone Python script that can run during the docs build
- Output files into the Sphinx build directory so they are deployed to GitHub Pages alongside the docs (e.g., `https://wooters.github.io/pyminidsp/llms.txt`)
- Mirror the structure and spirit of the miniDSP C library's llms.txt files

**Non-Goals:**
- Building a Sphinx extension — a standalone script is simpler and matches the miniDSP approach
- Auto-publishing to a separate llms.txt hosting service
- Generating docs for the underlying C API (that's miniDSP's job)
- Changing any existing documentation or API

## Decisions

### 1. Python introspection over RST parsing for API reference

**Choice**: Import pyminidsp and use `inspect` + docstrings to extract the API reference, rather than parsing RST files.

**Why**: The Python module's `__init__.py` already defines the exact public API surface via `__all__`. Introspection gives us accurate signatures, docstrings, and module organization with zero parsing fragility. RST parsing would require handling autodoc directives, cross-references, and Sphinx-specific markup.

**Alternative considered**: Parse `docs/api/*.rst` files directly. Rejected because those files mostly contain `.. autofunction::` directives — the real content lives in the Python source.

### 2. Direct RST-to-text conversion for guides

**Choice**: Parse `docs/guides/*.rst` files with lightweight RST stripping (remove directives, convert headers, strip role markup) rather than building through Sphinx.

**Why**: The guides contain rich tutorial content with code examples that are valuable for AI agents. A lightweight pass that strips RST directives (`.. code-block::`, `.. plot::`, `.. note::`) and converts to plain markdown/text is sufficient. The miniDSP script takes this same approach with its Doxygen markdown guides.

**Alternative considered**: Run Sphinx to produce text output (`sphinx-build -b text`). Rejected because it adds build complexity and requires the full Sphinx environment (including compiled C extension) just to generate text files.

### 3. Output files deployed via Sphinx docs, not committed to repo

**Choice**: Write `llms.txt` and `llms-full.txt` into the Sphinx build output directory (e.g., `docs/_build/html/`) so they are deployed to GitHub Pages alongside the documentation.

**Why**: This mirrors the miniDSP C library's approach — the files live at `https://wooters.github.io/miniDSP/llms-full.txt`, not in the repo. It avoids committing generated artifacts and ensures the files are always in sync with the deployed docs.

**Alternative considered**: Commit the files to the repo root. Rejected because it introduces staleness risk (files can drift from the actual docs) and clutters the repo with generated output.

### 4. Script location and invocation

**Choice**: Place the script at `scripts/gen_llms_txt.py` and add a docs build integration.

**Why**: Matches the miniDSP C library's script location. Can be run standalone (`python scripts/gen_llms_txt.py`) or as part of the docs build.

## Risks / Trade-offs

- **Staleness**: Not a concern — files are generated fresh during each docs build and never committed.
- **RST stripping fidelity**: Lightweight RST parsing won't handle every directive perfectly. → Mitigation: Focus on the directives actually used in the guides; imperfect formatting in edge cases is acceptable for AI consumption.
- **Import side effects**: The script must import pyminidsp, which requires the compiled C extension. → Mitigation: The script should be run in an environment where pyminidsp is installed (same as docs build). Document this requirement.
