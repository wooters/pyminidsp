## Context

pyminidsp v0.5.0 added `MiniDSPError` exceptions and error code constants. The API reference (`docs/api/constants.rst`) documents these, but the Quick Start guide (`docs/quickstart.rst`) — the primary entry point for new users — has no error handling examples. Users need to see error handling in context alongside the functions they're already learning.

## Goals / Non-Goals

**Goals:**
- Add an "Error handling" section to `docs/quickstart.rst` that teaches users how to catch and inspect `MiniDSPError`
- Show practical examples using functions already demonstrated in the Quick Start (e.g., `rms`, `scale_vec`)
- Cross-reference the API docs for complete error code details

**Non-Goals:**
- Adding `Raises` docstrings to every wrapper function (separate effort)
- Creating a standalone error handling guide in `docs/guides/`
- Documenting thread safety or the internal callback mechanism
- Modifying any Python source code

## Decisions

**1. Place the error handling section after "Basic usage" and before "Signal generation"**

Error handling is a fundamental concept that applies to every function. Placing it early — right after the user's first working example — ensures they see it before diving into specific feature areas. Alternative: placing it at the end, but that risks users never reaching it and treats error handling as an afterthought.

**2. Use two code examples: basic try/except and error-code matching**

The first example shows the simplest case (catch `MiniDSPError`, print the message). The second shows programmatic handling with error code constants. This progression matches how users actually adopt error handling — first they just want to see the error, then they want to react to specific error types.

**3. Use `rms()` with an empty array as the primary error example**

This function is already used in the "Basic usage" section, so users are familiar with it. Passing an empty array is a natural mistake that triggers `ERR_INVALID_SIZE`. Alternative: using a contrived example with an unfamiliar function, but that adds cognitive load.

## Risks / Trade-offs

- [Risk: Examples become stale if error messages change in the C library] → Examples show the pattern, not exact message text. The `.. code-block::` output uses illustrative values, not doctest-verified output.
- [Trade-off: Adding content to Quick Start makes it longer] → The section is ~30 lines of RST. The Quick Start is a reference-style page, so additional sections are expected.
