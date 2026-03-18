## Why

miniDSP C library v0.4.0 replaced all `assert()` calls with a configurable error handler. The library no longer aborts on precondition violations — it reports errors via a callback and returns safe defaults. The Python wrapper currently has no way to detect or surface these C-level errors, meaning invalid inputs silently produce wrong results (zeros, -1s) instead of raising exceptions.

## What Changes

- **Bind the new error-handling API**: Add `MD_set_error_handler()` and the `MD_ErrorCode` enum (`MD_ERR_NULL_POINTER`, `MD_ERR_INVALID_SIZE`, `MD_ERR_INVALID_RANGE`, `MD_ERR_ALLOC_FAILED`) to the CFFI `cdef` declarations.
- **Custom error exception**: Introduce a `MiniDSPError` exception class (subclass of `RuntimeError`) that carries the error code, function name, and message from the C callback.
- **Install a Python-aware error handler**: Register a CFFI callback as the C error handler at module load time. When the C library calls it, the handler stores the error info so the Python wrapper can raise `MiniDSPError` after the C function returns.
- **Expose `MiniDSPError` in the public API**: Add it to `__init__.py` and `__all__` so users can catch it.

## Capabilities

### New Capabilities
- `error-handling`: Bind the miniDSP v0.4.0 error handler API and convert C-level errors into Python exceptions via a custom `MiniDSPError` class.

### Modified Capabilities
<!-- None — existing function signatures and behavior are unchanged. The error handling is purely additive. -->

## Impact

- **`_build_minidsp.py`**: New `cdef` declarations for `MD_set_error_handler`, `MD_ErrorHandler` callback type, and `MD_ErrorCode` enum.
- **`_helpers.py`**: New `MiniDSPError` exception class, CFFI extern callback, error handler registration, and a helper to check/raise after each C call.
- **`__init__.py` / `_core.py`**: Export `MiniDSPError`.
- **All wrapper modules** (`_analysis.py`, `_effects.py`, `_filters.py`, `_spectral.py`, `_generators.py`, `_dtmf.py`, `_gcc.py`, `_resampling.py`, `_steganography.py`): Each C call site gains an error check after the `lib.MD_*()` call.
- **Tests**: New tests for error propagation; existing tests should continue to pass unchanged.
- **miniDSP C library dependency**: Must be updated to v0.4.0 (currently pinned to v0.3.1).
