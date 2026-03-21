## Context

pyminidsp publishes pre-built wheels for `manylinux_x86_64` and `macosx_arm64` via cibuildwheel on GitHub Actions. The CI runs on `ubuntu-latest` (x86_64) and `macos-latest` (arm64). There is no `linux/aarch64` wheel, so users running Docker on Apple Silicon Macs must build from source — a painful process requiring FFTW3 headers, a C compiler, and a clone of the miniDSP C library.

cibuildwheel natively supports cross-architecture Linux builds via QEMU user-space emulation. GitHub provides the `docker/setup-qemu-action` to register QEMU interpreters, after which cibuildwheel can build inside `aarch64` manylinux containers transparently.

## Goals / Non-Goals

**Goals:**
- Publish `manylinux_2_17_aarch64` wheels to PyPI for CPython 3.9–3.13.
- Keep the change minimal — reuse existing cibuildwheel config; only add QEMU setup and an arch directive.

**Non-Goals:**
- Windows wheels (no demand, significant effort).
- musl/Alpine wheels (FFTW3 packaging is problematic; already skipped).
- Native aarch64 runners (GitHub doesn't offer free arm64 Linux runners; QEMU is sufficient for this project's build size).

## Decisions

### 1. QEMU emulation via `docker/setup-qemu-action`

**Choice**: Add a step using `docker/setup-qemu-action@v3` before the cibuildwheel invocation on Linux.

**Rationale**: This is the approach recommended by the cibuildwheel docs. It registers binfmt_misc handlers so Docker can run `aarch64` containers on `x86_64` hosts. Zero config beyond the action itself.

**Alternative considered**: Using a self-hosted arm64 runner. Rejected — adds infrastructure burden for a small project; QEMU build times (~5–10 min) are acceptable.

### 2. Expand `CIBW_ARCHS_LINUX` to include `aarch64`

**Choice**: Set `archs` under `[tool.cibuildwheel.linux]` in `pyproject.toml` to `"x86_64 aarch64"`.

**Rationale**: cibuildwheel defaults to native arch only. Explicitly listing both architectures keeps the config declarative and visible in `pyproject.toml`.

**Alternative considered**: Setting the `CIBW_ARCHS_LINUX` environment variable in the workflow YAML. Rejected — pyproject.toml is the canonical config location for this project.

### 3. Keep a single `ubuntu-latest` job (no matrix split by arch)

**Choice**: The existing `ubuntu-latest` matrix entry builds both x86_64 and aarch64 wheels in one job.

**Rationale**: cibuildwheel handles the arch iteration internally. A single job is simpler and avoids duplicating the Linux config. Build time increase is acceptable (~5 extra minutes for the emulated builds).

## Risks / Trade-offs

- **[Slower CI]** → QEMU-emulated builds are 3–5× slower than native. Mitigated by: this only affects CI, not users; total pipeline time stays under 15 min.
- **[QEMU flakiness]** → Rare QEMU segfaults can cause spurious failures. Mitigated by: GitHub's QEMU action is well-maintained; failures are retryable.
- **[FFTW3 on aarch64]** → The existing `before-all` yum/dnf/apt install command already handles multi-arch containers since manylinux images ship with the correct arch's package repos. No change needed.
