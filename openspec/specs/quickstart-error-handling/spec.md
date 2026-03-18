### Requirement: Quick Start includes error handling section
The Quick Start guide (`docs/quickstart.rst`) SHALL contain an "Error handling" section placed after the "Basic usage" section and before the "Signal generation" section.

#### Scenario: Error handling section exists in Quick Start
- **WHEN** a user reads `docs/quickstart.rst`
- **THEN** there SHALL be a section titled "Error handling" between "Basic usage" and "Signal generation"

### Requirement: Basic error catching example
The error handling section SHALL include a code example showing how to catch `MiniDSPError` using a try/except block. The example SHALL demonstrate importing `MiniDSPError`, triggering an error with a function already shown in the Quick Start (e.g., `rms` with an empty array), and printing the exception's attributes (`code`, `func_name`, `message`).

#### Scenario: User sees how to catch and inspect MiniDSPError
- **WHEN** a user reads the basic error catching example
- **THEN** the example SHALL show `from pyminidsp import MiniDSPError`, a try/except block catching `MiniDSPError`, and access to `err.code`, `err.func_name`, and `err.message`

### Requirement: Error code matching example
The error handling section SHALL include a code example showing how to use the error code constants (`ERR_INVALID_SIZE`, `ERR_INVALID_RANGE`, etc.) to handle specific error types programmatically.

#### Scenario: User sees how to match on error codes
- **WHEN** a user reads the error code matching example
- **THEN** the example SHALL import at least two error code constants and use `err.code` in a conditional (e.g., if/elif) to take different actions based on the error type

### Requirement: Cross-reference to API docs
The error handling section SHALL include a cross-reference (using Sphinx `:class:` or `:const:` roles) pointing users to the full API documentation for `MiniDSPError` and the error code constants.

#### Scenario: User can navigate to full error handling API docs
- **WHEN** a user reads the error handling section
- **THEN** there SHALL be at least one Sphinx cross-reference linking to the API documentation for `MiniDSPError` or the error code constants
