## Why

pyminidsp v0.5.0 introduced proper error handling — C-level errors now raise `MiniDSPError` exceptions instead of silently returning default values. The API reference documents the exception class and error codes, but the Quick Start guide has no mention of error handling. Users following the Quick Start don't learn how to catch or respond to errors, which defeats the purpose of the new error reporting.

## What Changes

- Add an **Error handling** section to `docs/quickstart.rst` that shows how to catch `MiniDSPError`, inspect its attributes (`code`, `func_name`, `message`), and use the error code constants for programmatic handling.
- Include practical examples that demonstrate real error scenarios users are likely to encounter (e.g., empty arrays, out-of-range parameters).

## Capabilities

### New Capabilities
- `quickstart-error-handling`: Documentation section in the Quick Start guide showing how to handle errors from the miniDSP library, with practical code examples.

### Modified Capabilities
- `error-handling`: No requirement changes — the existing spec is correct. This change only adds documentation for the existing behavior.

## Impact

- `docs/quickstart.rst` — new section added
- No code changes, no API changes, no dependency changes
