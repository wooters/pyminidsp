## Context

Sphinx/docutils interprets `|text|` as a substitution reference. When these appear in prose (e.g., "RMS = |c|" meaning absolute value), the build emits errors. The fix is to use `:math:` directives or escape the pipes.

## Goals / Non-Goals

**Goals:**
- Fix all 7 Sphinx warnings so `sphinx-build -W` passes on a clean build

**Non-Goals:**
- Changing any code logic
- Restructuring documentation

## Decisions

**Decision**: Use `:math:` directives for mathematical notation (e.g., `:math:`|c|`` for absolute value, `:math:`|X(k)|`` for magnitude). This is semantically correct and renders nicely in HTML.

For the title underline, simply extend it to match the title width.
