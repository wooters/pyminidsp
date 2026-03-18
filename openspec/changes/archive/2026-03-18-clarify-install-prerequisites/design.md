## Context

`docs/installation.rst` currently opens with a "Prerequisites" section listing Python, FFTW3 dev headers, and a C compiler. The next section ("Installing from PyPI") then says none of those are needed for wheel installs. This is misleading: pre-built wheels eliminate the need for a C compiler and FFTW3 *dev headers*, but FFTW3 is dynamically linked and the runtime library (`libfftw3.so` / `libfftw3.dylib`) **is** still required on the user's system.

The `README.md` already separates "Installation" from "Building from Source" but doesn't clarify the FFTW3 runtime dependency for wheel users.

## Goals / Non-Goals

**Goals:**

- Make the wheel-install path the prominent default in both `docs/installation.rst` and `README.md`, clearly stating that only the FFTW3 runtime library is needed (no compiler, no dev headers).
- Keep all source-build instructions intact, scoped clearly under their own section with the full prerequisite list.

**Non-Goals:**

- Rewriting the development install instructions.
- Adding new content (e.g., Windows support notes, troubleshooting).
- Changing any code or build configuration.

## Decisions

**1. Replace the top-level "Prerequisites" section in `installation.rst`**

The current section lumps build-time and runtime dependencies together. Replace it with a streamlined section that lists only what wheel users need: Python 3.9+ and the FFTW3 runtime library. Move FFTW3 dev headers and C compiler into "Building from Source".

*Alternative considered*: Remove prerequisites entirely and just say `pip install pyminidsp`. Rejected because FFTW3 is dynamically linked and genuinely required at runtime — hiding it would cause confusing import errors.

**2. Lead with the happy path in `installation.rst`**

The page should open with FFTW3 runtime install instructions (just `apt install libfftw3-3` or `brew install fftw`), then `pip install pyminidsp`, list supported platforms/versions, and note that no C compiler is needed. Source-build instructions follow for users who need them.

**3. Clarify README.md**

Update the note under the "Installation" heading to say that pre-built wheels need FFTW3 but not a C compiler.

## Risks / Trade-offs

- [Users on unsupported platforms may miss that they need source-build steps] → Mitigated by listing supported wheel platforms prominently and linking to the source-build section.
- [Existing doc links to anchors may break if section names change] → Low risk for a project this size; grep for internal references before merging.
- [Future: FFTW3 could be bundled into wheels via `auditwheel`/`delocate`] → Out of scope for this change; if done later, the docs can be simplified further to truly have no prerequisites.
