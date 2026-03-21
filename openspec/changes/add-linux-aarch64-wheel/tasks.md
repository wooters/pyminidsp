## 1. cibuildwheel config

- [x] 1.1 Add `archs = "x86_64 aarch64"` to `[tool.cibuildwheel.linux]` in `pyproject.toml`

## 2. GitHub Actions workflow

- [x] 2.1 Add `docker/setup-qemu-action@v3` step in `wheels.yml` before the cibuildwheel build step (Linux only, via `if: runner.os == 'Linux'`)

## 3. Validation

- [ ] 3.1 Trigger a manual workflow run and verify both `x86_64` and `aarch64` wheels are produced in the build artifacts
