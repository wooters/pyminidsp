## ADDED Requirements

### Requirement: CI builds linux/aarch64 wheels
The CI pipeline SHALL build `manylinux_aarch64` wheels for CPython 3.9–3.13 using QEMU emulation on `ubuntu-latest` runners.

#### Scenario: Tagged release produces aarch64 wheels
- **WHEN** a version tag (e.g., `v0.7.0`) is pushed to the repository
- **THEN** the build-wheels job SHALL produce `manylinux_2_17_aarch64` `.whl` files for each supported CPython version and upload them as artifacts

#### Scenario: aarch64 wheels are published to PyPI
- **WHEN** a stable version tag is pushed (no `rc`, `alpha`, or `beta` suffix)
- **THEN** the `manylinux_aarch64` wheels SHALL be included in the PyPI publish step alongside existing x86_64 and macOS wheels

### Requirement: QEMU emulation is configured before Linux wheel builds
The GitHub Actions workflow SHALL set up QEMU user-space emulation before invoking cibuildwheel on Linux, so that aarch64 containers can run on x86_64 runners.

#### Scenario: QEMU setup step present
- **WHEN** the build-wheels job runs on `ubuntu-latest`
- **THEN** a `docker/setup-qemu-action` step SHALL execute before the cibuildwheel build step

### Requirement: cibuildwheel arch config includes aarch64
The `pyproject.toml` cibuildwheel Linux config SHALL specify both `x86_64` and `aarch64` as target architectures.

#### Scenario: pyproject.toml declares both architectures
- **WHEN** cibuildwheel reads `[tool.cibuildwheel.linux]` from `pyproject.toml`
- **THEN** the `archs` field SHALL contain `"x86_64 aarch64"`
