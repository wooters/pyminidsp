## Context

pyminidsp compiles the miniDSP C library from source using CFFI API mode. The build script (`_build_minidsp.py`) passes `-std=c2x` to the compiler and CI clones the miniDSP repo at HEAD. The upstream miniDSP library has been updated to use C17 instead of C23, tagged as v0.1.0, and CI is currently failing because manylinux containers and some compilers don't fully support C23.

## Goals / Non-Goals

**Goals:**
- Fix CI wheel builds by aligning compiler flags with the C17 standard used by miniDSP
- Pin miniDSP dependency to the v0.1.0 tag for reproducible builds
- Use the most compatible manylinux image now that C23 is no longer required

**Non-Goals:**
- Using `make install` to build miniDSP as a static library (current source-compilation approach works fine)
- Reading the miniDSP VERSION file to set pyminidsp's version (versions are independent)
- Compile-time version checks using MINIDSP_VERSION macros (not needed currently)

## Decisions

### 1. Compiler flag: `-std=c17`
Change `extra_compile_args` from `["-std=c2x", "-O2"]` to `["-std=c17", "-O2"]` in `_build_minidsp.py`.

**Rationale**: Matches the C standard the miniDSP library now targets. C17 is widely supported across all target platforms (GCC 8+, Clang 6+, MSVC 2019+).

### 2. Pin git clone to tag v0.1.0
All `git clone` commands (in `pyproject.toml` cibuildwheel config and `wheels.yml` sdist job) will use `--branch v0.1.0` to pin to the tagged release.

**Rationale**: Cloning HEAD is fragile — any breaking change upstream could break pyminidsp builds. Pinning to a tag gives reproducible builds. Future miniDSP releases will require an explicit version bump.

### 3. Revert manylinux image to default
Remove the explicit `manylinux_2_28` image pins. The default `manylinux2014` image is sufficient now that C23 support isn't needed, and provides broader compatibility (RHEL 7+).

**Rationale**: `manylinux_2_28` was chosen specifically for C23/GCC 12+ support. With C17, even GCC 4.9 (manylinux2014's default) works fine. Wider compatibility is better.

## Risks / Trade-offs

- [Pinned tag gets stale] → Acceptable trade-off for build stability. Update the tag when miniDSP releases a new version.
- [manylinux2014 default may change] → Low risk; cibuildwheel manages this well and manylinux2014 is the current default.
