## Context

The `type-check` job currently runs `uvx ty check`. `uvx` creates a temporary isolated environment with only `ty` installed — no project dependencies. `ty` needs numpy's type stubs to resolve imports in pyminidsp source files.

## Goals / Non-Goals

**Goals:**
- Make `ty check` run with project dependencies available so imports resolve.

**Non-Goals:**
- Changing the type checker or its configuration.

## Decisions

**Decision**: Use `uv run --extra dev ty check` instead of `uvx ty check`.

**Why**: `uv run` executes within the project's virtual environment (creating it if needed via `uv sync`). The `--extra dev` flag ensures dev dependencies (pytest, etc.) are installed, and the base dependencies (numpy, cffi) are always present. This matches how the type checker is run locally during development.

**Alternative considered**: `uv sync && uvx --with numpy ty check`. Rejected — fragile, duplicates the dependency list, and doesn't match local workflow.
