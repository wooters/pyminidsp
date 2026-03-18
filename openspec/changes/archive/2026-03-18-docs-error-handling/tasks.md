## 1. Add error handling section to Quick Start

- [x] 1.1 Add "Error handling" section header to `docs/quickstart.rst` after the "Basic usage" note block and before the "Signal generation" section
- [x] 1.2 Write introductory sentence explaining that all pyminidsp functions raise `MiniDSPError` on invalid inputs
- [x] 1.3 Add basic try/except code example: catch `MiniDSPError` from `md.rms()` with an empty array, print `err.code`, `err.func_name`, `err.message`
- [x] 1.4 Add error code matching code example: import `ERR_INVALID_SIZE` and `ERR_INVALID_RANGE`, use `err.code` in if/elif to handle specific error types
- [x] 1.5 Add Sphinx cross-references (`:class:`, `:const:` roles) linking to `MiniDSPError` and error code constants in the API docs

## 2. Verify

- [x] 2.1 Build the Sphinx docs (`make html` in `docs/`) and confirm the new section renders correctly with no warnings
