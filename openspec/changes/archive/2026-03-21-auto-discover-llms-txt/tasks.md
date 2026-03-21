## 1. Module Auto-Discovery

- [x] 1.1 Add `_discover_modules()` function that globs `pyminidsp/_*.py`, excludes `__init__`, `_build_minidsp`, and `_core`, and returns a sorted list of module names
- [x] 1.2 Add `_category_name_from_module()` function that imports a module and returns its docstring first line, falling back to title-cased filename with a stderr warning
- [x] 1.3 Replace `MODULE_CATEGORIES` usage in `extract_api()` with calls to the new discovery functions
- [x] 1.4 Remove the `MODULE_CATEGORIES` constant

## 2. Guide Auto-Discovery

- [x] 2.1 Add `_parse_toctree()` function that reads `docs/guides/index.rst` and returns the ordered list of guide slugs from the toctree directive
- [x] 2.2 Replace `GUIDE_ORDER` usage in `extract_guides()` with a call to `_parse_toctree()`
- [x] 2.3 Remove the `GUIDE_ORDER` constant

## 3. Verification

- [x] 3.1 Run `gen_llms_txt.py` and diff the output against the current generated files to confirm identical results
- [x] 3.2 Update the memory file `feedback_llms_txt_new_modules.md` to reflect that manual registration is no longer required
