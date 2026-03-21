## Why

Docker containers on Apple Silicon Macs (M1–M4) default to `linux/aarch64`. PyPI currently has no `manylinux_aarch64` wheel for pyminidsp, so `pip install pyminidsp` inside these containers falls back to building from source — requiring FFTW3 headers, a C compiler, and a clone of the miniDSP repo. Adding a pre-built `linux/aarch64` wheel eliminates this friction.

## What Changes

- Add QEMU emulation setup to the GitHub Actions wheel-build workflow so cibuildwheel can cross-compile `linux/aarch64` wheels on the existing `ubuntu-latest` (x86_64) runners.
- Expand the build matrix or cibuildwheel arch config to include `aarch64` for Linux.
- Resulting wheels are published to PyPI alongside existing x86_64 and macOS arm64 wheels.

## Capabilities

### New Capabilities
- `linux-aarch64-wheel`: Build and publish `manylinux_aarch64` wheels via QEMU emulation in CI.

### Modified Capabilities

(none — no existing spec-level requirements change)

## Impact

- **CI workflow** (`.github/workflows/wheels.yml`): new QEMU setup step; possible matrix or arch config change.
- **pyproject.toml**: may need minor cibuildwheel config tweaks (arch list).
- **PyPI**: new wheel artifacts for `manylinux_2_17_aarch64` will be uploaded on the next tagged release.
- **Build time**: QEMU-emulated builds are slower (~3–5× vs native), but only affect CI, not end users.
