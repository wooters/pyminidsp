## 1. Build Script

- [x] 1.1 Change `-std=c2x` to `-std=c17` in `pyminidsp/_build_minidsp.py` `extra_compile_args`

## 2. cibuildwheel Config (pyproject.toml)

- [x] 2.1 Add `--branch v0.1.0` to the top-level `before-all` git clone command
- [x] 2.2 Add `--branch v0.1.0` to the Linux `before-all` git clone command
- [x] 2.3 Add `--branch v0.1.0` to the macOS `before-all` git clone command
- [x] 2.4 Add `--branch v0.1.0` to the Windows `before-all` git clone command
- [x] 2.5 Remove `manylinux-x86_64-image` and `manylinux-aarch64-image` overrides from `[tool.cibuildwheel.linux]`
- [x] 2.6 Update the Linux section comment from C23 to C17

## 3. CI Workflow (wheels.yml)

- [x] 3.1 Add `--branch v0.1.0` to the git clone in the `build-sdist` job

## 4. Verification

- [x] 4.1 Run local build with `MINIDSP_SRC` to confirm C17 compilation works
