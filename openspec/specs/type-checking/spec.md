## ADDED Requirements

### Requirement: ty configuration in pyproject.toml
The project SHALL have a `[tool.ty]` section in `pyproject.toml` that configures `ty` for the `pyminidsp` package with Python 3.9 as the minimum target version.

#### Scenario: ty check runs with project config
- **WHEN** a developer runs `ty check` from the project root
- **THEN** `ty` reads its configuration from `pyproject.toml` and checks the `pyminidsp/` package

### Requirement: CFFI extension type stub
The project SHALL include a `pyminidsp/_minidsp_cffi.pyi` stub file that declares types for the `ffi` and `lib` objects imported by all modules.

#### Scenario: Modules importing ffi and lib pass type checking
- **WHEN** `ty check` runs on any module that imports `from pyminidsp._minidsp_cffi import ffi, lib`
- **THEN** the import resolves without type errors and `ffi.cast()`, `ffi.new()`, and all `lib.MD_*` / `lib.BiQuad_*` functions have known signatures

#### Scenario: Stub covers all C functions used by Python wrappers
- **WHEN** a Python wrapper calls `lib.MD_<name>(...)` or `lib.BiQuad_<name>(...)`
- **THEN** the stub declares a matching function signature so `ty` can validate argument types

### Requirement: Public API type annotations
All public functions and the `BiquadFilter` class SHALL have complete type annotations (parameter types and return types).

#### Scenario: Functions accepting array inputs
- **WHEN** a public function accepts a signal or array parameter
- **THEN** the parameter is annotated as `npt.ArrayLike` and the implementation converts it internally

#### Scenario: Functions returning arrays
- **WHEN** a public function returns a NumPy array
- **THEN** the return type is annotated as `npt.NDArray[np.float64]`

#### Scenario: Functions returning scalars
- **WHEN** a public function returns a scalar value from a C `double` function (e.g., `dot`, `energy`, `power`)
- **THEN** the return type is annotated as `float`

#### Scenario: Functions returning tuples
- **WHEN** a public function returns multiple values (e.g., `steg_encode` returns an array and a count)
- **THEN** the return type is annotated as an explicit `tuple` type

#### Scenario: BiquadFilter class
- **WHEN** the `BiquadFilter` class is type-checked
- **THEN** `__init__`, `process`, and `process_array` all have complete annotations

### Requirement: Internal helper annotations
The internal helper functions `_as_double_ptr` and `_new_double_array` in `_helpers.py` SHALL have type annotations.

#### Scenario: _as_double_ptr annotation
- **WHEN** `_as_double_ptr` is type-checked
- **THEN** it accepts `npt.ArrayLike` and returns a tuple of the CFFI pointer and the contiguous array

#### Scenario: _new_double_array annotation
- **WHEN** `_new_double_array` is type-checked
- **THEN** it accepts `int` and returns a tuple of `npt.NDArray[np.float64]` and a CFFI pointer

### Requirement: py.typed marker
The project SHALL include a `pyminidsp/py.typed` marker file per PEP 561, and this file SHALL be included in built distributions.

#### Scenario: py.typed marker exists
- **WHEN** a consumer installs pyminidsp
- **THEN** a `py.typed` file is present in the installed package directory

#### Scenario: py.typed included in wheel
- **WHEN** a wheel is built
- **THEN** the `py.typed` file is included in the wheel's `pyminidsp/` directory

### Requirement: ty check passes cleanly
Running `ty check` from the project root SHALL produce zero errors on the `pyminidsp/` package (excluding tests and `_build_minidsp.py`).

#### Scenario: Clean type check on all modules
- **WHEN** a developer runs `ty check`
- **THEN** the exit code is 0 and no errors are reported for `pyminidsp/` source files

#### Scenario: CI type check gate
- **WHEN** a PR is opened or code is pushed
- **THEN** a CI job runs `ty check` and the workflow fails if type errors are found

### Requirement: CI type-check job
The `wheels.yml` GitHub Actions workflow SHALL include a type-check job that runs `ty check` on every push and pull request.

#### Scenario: Type check runs in CI
- **WHEN** the `wheels.yml` workflow is triggered
- **THEN** a `type-check` job installs `ty` via `uv tool install ty` and runs `ty check`

#### Scenario: Type check job does not block wheel builds
- **WHEN** the type-check job runs
- **THEN** it runs in parallel with `build-wheels` and `build-sdist` (no `needs` dependency)
