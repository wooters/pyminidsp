## Why

The `type-check` CI job in `wheels.yml` runs `uvx ty check`, which launches `ty` in an isolated environment without project dependencies. Since `ty` can't resolve `numpy` (or any other project dependency), it fails with `unresolved-import` errors. This caused the v0.5.0 workflow to show as failed even though wheels built and published successfully.

## What Changes

- Replace `uvx ty check` with a command that runs `ty` within the project's virtual environment where dependencies are installed.

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
<!-- None — this is a CI config fix, not a behavior change -->

## Impact

- `.github/workflows/wheels.yml` — single line change in the `type-check` job.
