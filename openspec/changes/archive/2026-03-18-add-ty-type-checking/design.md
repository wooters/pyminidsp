## Context

pyminidsp is a CFFI-based Python wrapper around the miniDSP C library. Every public function is a thin wrapper that converts NumPy arrays to CFFI pointers, calls a `lib.MD_*` C function, and returns a NumPy array. The codebase currently has zero type annotations, no type checker, and no `py.typed` marker.

The project already uses `uv` for package management and `ruff` for linting. The Astral team (behind both tools) has released `ty`, a fast type checker for Python that integrates naturally into this toolchain.

The CFFI-generated `_minidsp_cffi` extension module is the main challenge — it's built at install time from C source, so no `.pyi` stub exists for the `ffi` and `lib` objects that every module imports.

## Goals / Non-Goals

**Goals:**
- Get `ty check` passing on the entire `pyminidsp/` package
- Add type annotations to all public API functions and `BiquadFilter`
- Create a CFFI stub so `ty` can resolve `ffi` and `lib` references
- Add `py.typed` marker for PEP 561 compliance
- Add type checking to CI so regressions are caught automatically

**Non-Goals:**
- Annotating test files — tests can remain untyped for now
- Annotating `_build_minidsp.py` — the CFFI build script is build-time only
- Achieving full generic `numpy.ndarray` shape/dtype typing (use `npt.NDArray[np.float64]` where possible, but don't fight NumPy's type system)
- Migrating away from CFFI or changing any runtime behavior

## Decisions

### 1. Type checker: `ty` (not mypy or pyright)

**Rationale:** `ty` is from the same Astral team behind `uv` and `ruff`, which this project already uses. It's fast, has good defaults, and keeps the toolchain consistent. It's installed as a standalone tool via `uv tool install ty`, not as a project dependency.

**Alternatives considered:**
- **mypy**: Mature but slower, requires plugins for CFFI, heavier configuration
- **pyright**: Excellent but a Node.js dependency, doesn't fit the pure-Python/uv toolchain

### 2. CFFI stub: hand-written `_minidsp_cffi.pyi`

**Rationale:** The `_minidsp_cffi` module is generated at build time by CFFI's API mode. `ty` cannot inspect it statically. A hand-written `.pyi` stub file provides the necessary type information for `ffi` and `lib`. The stub only needs to declare what the Python code actually uses: `ffi.cast()`, `ffi.new()`, and the `lib.MD_*` / `lib.BiQuad_*` functions.

**Alternatives considered:**
- **Auto-generate stubs from built extension**: Fragile, requires the extension to be built before type checking, complicates CI
- **`# type: ignore` on all CFFI imports**: Defeats the purpose — hides real errors

### 3. Annotation style: inline annotations (not separate `.pyi` stubs for public API)

**Rationale:** Inline annotations in the source `.py` files serve as documentation and are maintained alongside the code. Since Python >=3.9 is required, we can use modern syntax (`list[int]`, `X | None`) everywhere.

### 4. Array types: `npt.NDArray[np.float64]`

**Rationale:** All arrays in pyminidsp are float64. Using `numpy.typing.NDArray[np.float64]` documents this contract clearly. Input parameters that accept "array-like" values use `npt.ArrayLike`.

### 5. CI integration: separate job in `wheels.yml`

**Rationale:** Type checking is fast (no build required beyond stub availability) and should run on every PR and push, alongside the existing wheel builds. A separate job keeps it independent so it doesn't slow down or block wheel builds.

### 6. `ty` configuration: `[tool.ty]` section in `pyproject.toml`

**Rationale:** Keeps all tool configuration in one place. The config will set the Python target version and any necessary exclusions.

## Risks / Trade-offs

- **`ty` is young** — It may have gaps in numpy/CFFI support. → Mitigation: use `type: ignore[...]` comments sparingly for genuine tool limitations; revisit as `ty` matures.
- **CFFI stub maintenance** — The stub must be updated when new C functions are added to miniDSP. → Mitigation: the stub is small and changes infrequently (tied to miniDSP version bumps). Add a note in CLAUDE.md.
- **`npt.ArrayLike` acceptance** — `ty` may not fully resolve `ArrayLike` in all positions. → Mitigation: fall back to `np.ndarray` for inputs if needed.
- **No Windows CI** — Type checking only runs on Linux in CI, but this is fine since type checking is platform-independent.
