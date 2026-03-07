## Core Engineering Principles

1. **Clarity over cleverness** — Write code that's maintainable, not impressive
2. **Explicit over implicit** — No magic. Make behavior obvious
3. **Composition over inheritance** — Small units that combine
4. **Fail fast, fail loud** — Surface errors at the source
5. **Delete code** — Less code = fewer bugs. Question every addition
6. **Verify, don't assume** — Run it. Test it. Prove it works

## Build

- `MINIDSP_SRC` env var must point to a clone of the [miniDSP](https://github.com/wooters/miniDSP) C library. Build fails without it.
- Example: `MINIDSP_SRC=./miniDSP uv sync`

## Architecture

- CFFI **API mode** (not ABI) — `_build_minidsp.py` compiles C source and generates `_minidsp_cffi` extension at install time.
- Every Python function is a thin wrapper around a `lib.MD_*` C call. The pattern:
  1. Convert inputs with `_as_double_ptr()` (from `_helpers.py`)
  2. Allocate output with `_new_double_array()`
  3. Call `lib.MD_<function>()`
  4. Return the NumPy array
- All arrays are float64. Inputs auto-convert via `np.ascontiguousarray(arr, dtype=np.float64)`.
