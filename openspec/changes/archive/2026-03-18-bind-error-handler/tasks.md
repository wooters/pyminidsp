## 1. Update miniDSP C library dependency

- [x] 1.1 Update miniDSP C library pin from v0.3.1 to v0.4.0 (vendor submodule, CI config, any version references)

## 2. CFFI declarations

- [x] 2.1 Add `MD_ErrorCode` enum (`MD_ERR_NULL_POINTER=1`, `MD_ERR_INVALID_SIZE=2`, `MD_ERR_INVALID_RANGE=3`, `MD_ERR_ALLOC_FAILED=4`) to `cdef` in `_build_minidsp.py`
- [x] 2.2 Add `MD_ErrorHandler` callback type and `MD_set_error_handler()` function to `cdef` in `_build_minidsp.py`

## 3. Error infrastructure in `_helpers.py`

- [x] 3.1 Add `MiniDSPError` exception class (subclass of `RuntimeError`) with `code`, `func_name`, and `message` attributes
- [x] 3.2 Add error code constants (`ERR_NULL_POINTER`, `ERR_INVALID_SIZE`, `ERR_INVALID_RANGE`, `ERR_ALLOC_FAILED`)
- [x] 3.3 Implement thread-local error storage and CFFI `extern "Python"` error handler callback
- [x] 3.4 Register the error handler via `lib.MD_set_error_handler()` at module load
- [x] 3.5 Implement `_check_error()` helper that reads thread-local, clears it, and raises `MiniDSPError` if an error was recorded

## 4. Add `_check_error()` calls to all wrapper modules

- [x] 4.1 Add `_check_error()` after every `lib.MD_*()` call in `_analysis.py`
- [x] 4.2 Add `_check_error()` after every `lib.MD_*()` call in `_effects.py`
- [x] 4.3 Add `_check_error()` after every `lib.MD_*()` call in `_filters.py`
- [x] 4.4 Add `_check_error()` after every `lib.MD_*()` call in `_spectral.py`
- [x] 4.5 Add `_check_error()` after every `lib.MD_*()` call in `_generators.py`
- [x] 4.6 Add `_check_error()` after every `lib.MD_*()` call in `_dtmf.py`
- [x] 4.7 Add `_check_error()` after every `lib.MD_*()` call in `_gcc.py`
- [x] 4.8 Add `_check_error()` after every `lib.MD_*()` call in `_resampling.py`
- [x] 4.9 Add `_check_error()` after every `lib.MD_*()` call in `_steganography.py`

## 5. Public API exports

- [x] 5.1 Export `MiniDSPError` and error code constants from `_core.py`
- [x] 5.2 Export `MiniDSPError` and error code constants from `__init__.py` and add to `__all__`

## 6. Tests

- [x] 6.1 Test that `MiniDSPError` is importable and is a subclass of `RuntimeError`
- [x] 6.2 Test that error code constants have correct values (1–4)
- [x] 6.3 Test that a C-level error (e.g., invalid size) raises `MiniDSPError` with correct `code`, `func_name`, and `message`
- [x] 6.4 Test that error state is cleared after a raised exception (subsequent valid call succeeds)
- [x] 6.5 Test thread safety — concurrent calls from separate threads get independent error state
- [x] 6.6 Verify existing tests still pass (no regressions)

## 7. Documentation and version bump

- [x] 7.1 Update CLAUDE.md or CHANGELOG if needed to note the new error handling capability
- [x] 7.2 Bump pyminidsp version to reflect the new miniDSP v0.4.0 dependency
