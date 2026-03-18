## Context

The `README.md` currently has no status badges. The project is published on PyPI (v0.5.0), has two GitHub Actions workflows (`Build wheels`, `Deploy Documentation`), is MIT-licensed, and supports Python 3.9–3.13.

## Goals / Non-Goals

**Goals:**
- Add informative badges that reflect project health and metadata at a glance
- Use shields.io for static metadata badges and GitHub's native badge URLs for workflow status

**Non-Goals:**
- Adding dynamic badges (coverage, downloads) — these require additional infrastructure not yet in place
- Changing any other part of the README

## Decisions

1. **Badge service**: Use shields.io for PyPI version, Python versions, and license. Use GitHub's built-in workflow status badges for CI. Shields.io is the de facto standard and requires no configuration. GitHub's native badges (`github.com/<owner>/<repo>/actions/workflows/<file>/badge.svg`) are always in sync with actual workflow state.

2. **Badge placement**: Insert badges on the line immediately after `# pyminidsp`, before the documentation link. This is the most common convention in Python open-source projects.

3. **Badge set**: PyPI version, Python versions, License, Build wheels status, Docs status. This covers the most important signals for a library consumer without clutter.

## Risks / Trade-offs

- [Shields.io outage] → Badges show "unavailable" placeholder; no impact on repo functionality. This is a widely accepted trade-off.
