## Context

pyminidsp wraps the miniDSP C library via CFFI (API mode). Every Python function is a thin wrapper: convert inputs → call `lib.MD_*()` → return NumPy array. The C library previously used `assert()` for precondition checks, which would `abort()` the entire Python process on violations — a hard crash with no recovery.

miniDSP v0.4.0 replaces all asserts with a configurable error handler. Errors are now reported via a callback (`MD_ErrorHandler`) and functions return safe defaults. The Python wrapper currently ignores these errors entirely, silently returning zero-filled arrays or sentinel values.

## Goals / Non-Goals

**Goals:**
- Surface C-level errors as Python exceptions so users get clear diagnostics instead of silent wrong results.
- Provide a typed `MiniDSPError` exception carrying the error code, C function name, and message.
- Require zero changes to existing user code that passes valid inputs — this is purely additive.

**Non-Goals:**
- Allowing Python users to install custom C-level error handlers (the Python handler is fixed at module load).
- Wrapping every possible future error code — we bind what v0.4.0 defines and extend later.
- Changing the Python API signatures or return types.

## Decisions

### 1. Thread-local error storage instead of raising inside the callback

**Decision**: The CFFI `extern "Python"` callback stores the error in a thread-local variable. After each `lib.MD_*()` call returns, a helper checks the thread-local and raises `MiniDSPError` if set.

**Why not raise directly in the callback?** CFFI callbacks invoked from C cannot propagate Python exceptions back through the C stack. Raising inside the callback would be swallowed. The store-and-check pattern is the standard approach for CFFI/ctypes interop.

**Alternative considered**: Use `ffi.new_handle()` to pass a Python object into C. Rejected — `MD_set_error_handler` takes a simple function pointer, not a user-data pair.

### 2. Single `MiniDSPError` exception class (subclass of `RuntimeError`)

**Decision**: One exception class with a `code` attribute (the `MD_ErrorCode` enum value), rather than a hierarchy of exception subclasses.

**Why**: Four error codes don't warrant four exception classes. Users can branch on `err.code` if needed. A single class keeps the API surface small.

**Alternative considered**: Map `MD_ERR_NULL_POINTER` → `ValueError`, `MD_ERR_ALLOC_FAILED` → `MemoryError`, etc. Rejected — mixing built-in types makes it hard to catch "any miniDSP error" generically, and the C error codes don't map cleanly to Python's exception taxonomy.

### 3. Centralized `_check_error()` helper in `_helpers.py`

**Decision**: Add a `_check_error()` function that checks the thread-local, clears it, and raises. Each wrapper function calls `_check_error()` after its `lib.MD_*()` call.

**Why**: Keeps error-checking logic in one place. The alternative — inline checks at every call site — duplicates logic and is error-prone.

### 4. Handler installed at import time via `_helpers.py` module init

**Decision**: `_helpers.py` calls `lib.MD_set_error_handler(callback)` at module load. Since `_helpers.py` is imported before any wrapper module, the handler is always active.

**Why**: Simplest approach. No lazy init, no race conditions. The atexit handler for `MD_shutdown()` already follows this pattern.

### 5. Bump miniDSP C library pin from v0.3.1 to v0.4.0

**Decision**: Update the vendored/pinned version of the C library to v0.4.0 to get the error handler API.

**Why**: The new API doesn't exist in v0.3.1.

## Risks / Trade-offs

- **Performance**: Every C call now has a thread-local check on return. Cost is negligible (one Python dict lookup per call) — DSP functions process thousands of samples per call.
- **Thread safety**: Thread-local storage (`threading.local()`) ensures concurrent calls from different threads don't interfere. Within a single thread, errors are checked immediately after each call, so no stale state accumulates.
- **Broad code touch**: Every wrapper module needs a `_check_error()` call after each `lib.MD_*()` invocation. Risk of missing a site. Mitigation: grep for `lib.MD_` and verify each has a corresponding `_check_error()`.
- **CFFI callback GC**: The callback object must remain alive. Mitigation: store it as a module-level variable in `_helpers.py`.
