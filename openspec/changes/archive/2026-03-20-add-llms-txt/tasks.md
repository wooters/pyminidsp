## 1. Script Scaffolding

- [x] 1.1 Create `scripts/gen_llms_txt.py` with argument parsing (including `--output-dir`, default `docs/_build/html/`) and main entry point
- [x] 1.2 Add import-time check for pyminidsp with clear error message on failure

## 2. API Reference Generation

- [x] 2.1 Introspect `pyminidsp.__all__` to collect all public symbols
- [x] 2.2 Map each symbol to its source module category (analysis, effects, filters, spectral, generators, dtmf, gcc, resampling, steganography, helpers)
- [x] 2.3 Extract function signatures using `inspect.signature()`
- [x] 2.4 Extract and format docstrings for each function (description, parameters, return values)
- [x] 2.5 Render the API reference section with category headings, `---` dividers, and fenced code blocks

## 3. Tutorial Content Extraction

- [x] 3.1 Discover and order all `docs/guides/*.rst` files
- [x] 3.2 Implement RST-to-text converter: strip directives (`.. code-block::`, `.. plot::`, `.. note::`, etc.), convert role markup (`:func:`, `:math:`), and preserve code block content as fenced blocks
- [x] 3.3 Render the tutorials section with guide titles and converted content

## 4. Output Assembly

- [x] 4.1 Generate `llms.txt` (project name, description, GitHub URL, link to llms-full.txt on deployed docs site)
- [x] 4.2 Assemble `llms-full.txt` from header + API reference + tutorials sections
- [x] 4.3 Write both files to the output directory (default `docs/_build/html/`)

## 5. Integration & Verification

- [x] 5.1 Run the script and verify `llms.txt` is concise (<20 lines) with correct links to deployed docs site
- [x] 5.2 Verify `llms-full.txt` contains all `__all__` symbols and all guide content
- [x] 5.3 Integrate generation into the Sphinx docs build so files are included in GitHub Pages deployment
