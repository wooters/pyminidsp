## ADDED Requirements

### Requirement: MiniDSPError exception class
The package SHALL expose a `MiniDSPError` exception class (subclass of `RuntimeError`) in the public API. The exception SHALL have the following attributes:
- `code` (int): The `MD_ErrorCode` enum value from the C library.
- `func_name` (str): The name of the C function that reported the error.
- `message` (str): The human-readable error description from the C library.

#### Scenario: MiniDSPError is importable from the package
- **WHEN** a user writes `from pyminidsp import MiniDSPError`
- **THEN** the import SHALL succeed and `MiniDSPError` SHALL be a subclass of `RuntimeError`

#### Scenario: MiniDSPError carries error details
- **WHEN** a `MiniDSPError` is raised
- **THEN** `err.code` SHALL be an integer matching one of the `MD_ErrorCode` values (1–4), `err.func_name` SHALL be a non-empty string, and `err.message` SHALL be a non-empty string

### Requirement: Error code constants
The package SHALL expose the following integer constants matching the C `MD_ErrorCode` enum:
- `ERR_NULL_POINTER` = 1
- `ERR_INVALID_SIZE` = 2
- `ERR_INVALID_RANGE` = 3
- `ERR_ALLOC_FAILED` = 4

#### Scenario: Error code constants are importable
- **WHEN** a user writes `from pyminidsp import ERR_NULL_POINTER, ERR_INVALID_SIZE, ERR_INVALID_RANGE, ERR_ALLOC_FAILED`
- **THEN** the imports SHALL succeed and the values SHALL be 1, 2, 3, and 4 respectively

#### Scenario: Error code matches exception
- **WHEN** a C function reports `MD_ERR_INVALID_SIZE`
- **THEN** the raised `MiniDSPError` SHALL have `code == ERR_INVALID_SIZE` (2)

### Requirement: C error handler registration
The package SHALL register a CFFI callback as the miniDSP C error handler (`MD_set_error_handler`) at module import time. This registration SHALL occur before any wrapper function can be called.

#### Scenario: Handler is active at import
- **WHEN** the `pyminidsp` package is imported
- **THEN** `MD_set_error_handler` SHALL have been called with a valid callback

### Requirement: C errors raise Python exceptions
When any `lib.MD_*()` C function triggers the error handler, the corresponding Python wrapper function SHALL raise `MiniDSPError` with the error details from the callback.

#### Scenario: Null pointer error raises MiniDSPError
- **WHEN** a wrapper function calls a C function that reports `MD_ERR_NULL_POINTER`
- **THEN** the wrapper SHALL raise `MiniDSPError` with `code == 1`

#### Scenario: Invalid size error raises MiniDSPError
- **WHEN** a wrapper function calls a C function that reports `MD_ERR_INVALID_SIZE`
- **THEN** the wrapper SHALL raise `MiniDSPError` with `code == 2`

#### Scenario: Invalid range error raises MiniDSPError
- **WHEN** a wrapper function calls a C function that reports `MD_ERR_INVALID_RANGE`
- **THEN** the wrapper SHALL raise `MiniDSPError` with `code == 3`

#### Scenario: Allocation failure raises MiniDSPError
- **WHEN** a wrapper function calls a C function that reports `MD_ERR_ALLOC_FAILED`
- **THEN** the wrapper SHALL raise `MiniDSPError` with `code == 4`

### Requirement: Thread safety
The error handler SHALL use thread-local storage so that concurrent calls from different threads do not interfere with each other's error state.

#### Scenario: Concurrent threads get independent errors
- **WHEN** two threads concurrently call wrapper functions and one triggers a C error
- **THEN** only the thread whose call triggered the error SHALL raise `MiniDSPError`; the other thread SHALL return normally

### Requirement: Error state is cleared after check
After a `MiniDSPError` is raised (or after a successful call), the stored error state SHALL be cleared so that subsequent calls are not affected by prior errors.

#### Scenario: Successful call after error
- **WHEN** a wrapper function raises `MiniDSPError` and the user catches it, then calls another wrapper function with valid inputs
- **THEN** the second call SHALL succeed without raising

### Requirement: CFFI cdef includes error handler API
The CFFI build script SHALL declare the `MD_ErrorCode` enum, the `MD_ErrorHandler` callback type, and the `MD_set_error_handler` function so they are available to the Python bindings.

#### Scenario: Error handler API is accessible via lib
- **WHEN** the CFFI extension is compiled
- **THEN** `lib.MD_set_error_handler` SHALL be callable and the enum values `lib.MD_ERR_NULL_POINTER`, `lib.MD_ERR_INVALID_SIZE`, `lib.MD_ERR_INVALID_RANGE`, `lib.MD_ERR_ALLOC_FAILED` SHALL be defined
