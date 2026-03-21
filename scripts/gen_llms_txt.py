#!/usr/bin/env python3
"""Generate llms.txt and llms-full.txt for pyminidsp.

Introspects the pyminidsp public API and parses RST guide files to produce
AI-agent-friendly documentation files.

Usage:
    python scripts/gen_llms_txt.py [--output-dir DIR]
"""

from __future__ import annotations

import argparse
import inspect
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_NAME = "pyminidsp"
PROJECT_DESC = (
    "Python bindings to the miniDSP C library — a comprehensive DSP toolkit "
    "providing signal generation, spectral analysis, filtering, effects, and more. "
    "All functions accept and return NumPy arrays."
)
GITHUB_URL = "https://github.com/wooters/pyminidsp"
DOCS_BASE_URL = "https://wooters.github.io/pyminidsp"

# Maps source module name -> display category (in presentation order)
MODULE_CATEGORIES: list[tuple[str, str]] = [
    ("_helpers", "Constants & Error Handling"),
    ("_analysis", "Math Utilities, Signal Measurement, Analysis & Scaling"),
    ("_effects", "Effects"),
    ("_filters", "FIR / Convolution / Biquad"),
    ("_spectral", "Spectrum, FFT, Mel, MFCC & Windows"),
    ("_generators", "Signal Generators"),
    ("_dtmf", "DTMF"),
    ("_gcc", "GCC Delay Estimation"),
    ("_resampling", "Resampling"),
    ("_steganography", "Audio Steganography"),
    ("_vad", "Voice Activity Detection"),
]

# Guide ordering (matches docs/guides/index.rst toctree)
GUIDE_ORDER = [
    "signal-generators",
    "basic-signal-operations",
    "window-functions",
    "magnitude-spectrum",
    "power-spectral-density",
    "phase-spectrum",
    "stft-spectrogram",
    "mel-mfcc",
    "pitch-detection",
    "fir-convolution",
    "simple-effects",
    "dtmf",
    "shepard-tone",
    "spectrogram-text",
    "voice-activity-detection",
    "audio-steganography",
]

# ---------------------------------------------------------------------------
# API extraction
# ---------------------------------------------------------------------------


def _import_pyminidsp():
    """Import pyminidsp, failing with a clear message if unavailable."""
    try:
        import pyminidsp
        return pyminidsp
    except ImportError:
        print(
            "Error: pyminidsp is not installed in this environment.\n"
            "Install it first (e.g. `uv sync` or `pip install -e .`) "
            "before running this script.",
            file=sys.stderr,
        )
        sys.exit(1)


def _get_module_for_symbol(md, name: str) -> str:
    """Return the source submodule name for a public symbol."""
    obj = getattr(md, name)
    mod = getattr(obj, "__module__", "")
    # e.g. "pyminidsp._analysis" -> "_analysis"
    if mod.startswith("pyminidsp."):
        return mod.split(".")[-1]
    return "_helpers"


def _format_signature(name: str, obj) -> str:
    """Return a formatted function/class signature string."""
    if isinstance(obj, type):
        # Class — show __init__ signature
        try:
            sig = inspect.signature(obj.__init__)
            # Remove 'self' parameter
            params = [p for n, p in sig.parameters.items() if n != "self"]
            sig = sig.replace(parameters=params)
        except (ValueError, TypeError):
            sig = "(...)"
        return f"class {name}{sig}"
    elif callable(obj):
        try:
            sig = inspect.signature(obj)
        except (ValueError, TypeError):
            sig = "(...)"
        return f"{name}{sig}"
    else:
        # Constant
        return f"{name} = {obj!r}"


def _is_plain_constant(obj) -> bool:
    """Return True if obj is a plain builtin constant (int, float, str)."""
    return type(obj) in (int, float, str, bool)


def _format_docstring(obj, doc: str | None) -> str:
    """Clean up a docstring for plain-text output.

    Suppresses inherited builtin docstrings for plain constants.
    """
    if not doc or _is_plain_constant(obj):
        return ""
    return inspect.cleandoc(doc)


def extract_api(md) -> dict[str, list[tuple[str, str, str]]]:
    """Extract the public API grouped by category.

    Returns:
        dict mapping category display name to list of
        (formatted_signature, docstring, symbol_name) tuples.
    """
    all_names = set(md.__all__)
    module_map: dict[str, str] = {}
    for name in sorted(all_names):
        module_map[name] = _get_module_for_symbol(md, name)

    # Build category -> entries
    categories: dict[str, list[tuple[str, str, str]]] = {}
    for mod_key, cat_name in MODULE_CATEGORIES:
        entries = []
        for name in md.__all__:  # preserve __all__ order
            if name not in all_names:
                continue
            if module_map.get(name) != mod_key:
                continue
            obj = getattr(md, name)
            sig = _format_signature(name, obj)
            doc = _format_docstring(obj, getattr(obj, "__doc__", None))
            entries.append((sig, doc, name))
        if entries:
            categories[cat_name] = entries

    return categories


def render_api_reference(categories: dict[str, list[tuple[str, str, str]]]) -> str:
    """Render the API reference section as markdown text."""
    parts = ["# API Reference\n"]
    for cat_name, entries in categories.items():
        parts.append(f"## {cat_name}\n")
        for sig, doc, _name in entries:
            if doc:
                parts.append(f"\n### `{sig}`\n")
                parts.append(doc)
                parts.append("\n---\n")
            else:
                # Constants — compact, no divider bloat
                parts.append(f"- `{sig}`")
        parts.append("\n---\n")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# RST guide processing
# ---------------------------------------------------------------------------


def _strip_rst(text: str) -> str:
    """Convert RST text to plain markdown-ish text for AI consumption."""
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Convert RST underline-style headings to markdown
        if (
            i + 1 < len(lines)
            and lines[i + 1]
            and set(lines[i + 1].strip()) <= {"=", "-", "~", "^", '"'}
            and len(lines[i + 1].strip()) >= len(line.strip())
            and line.strip()
        ):
            char = lines[i + 1].strip()[0]
            level = {"=": "#", "-": "##", "~": "###", "^": "####", '"': "#####"}.get(
                char, "##"
            )
            out.append(f"{level} {line.strip()}\n")
            i += 2
            continue

        # Strip .. raw:: html blocks entirely
        if re.match(r"^\.\. raw::\s+html", line):
            i += 1
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                i += 1
                if i < len(lines) and not lines[i].startswith("   ") and lines[i].strip():
                    break
            continue

        # Convert .. math:: blocks
        if re.match(r"^\.\. math::", line):
            out.append("")
            i += 1
            # Skip blank lines
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            # Collect indented content
            math_lines = []
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                math_lines.append(lines[i].strip())
                i += 1
            out.append("$$")
            out.extend(math_lines)
            out.append("$$\n")
            continue

        # Convert .. code-block:: to fenced code blocks
        m = re.match(r"^\.\. code-block::\s*(\w+)?", line)
        if m:
            lang = m.group(1) or ""
            i += 1
            # Skip blank lines and options (like :linenos:)
            while i < len(lines) and (
                lines[i].strip() == "" or re.match(r"^\s+:\w+:", lines[i])
            ):
                i += 1
            # Collect indented code
            code_lines = []
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                code_lines.append(lines[i][3:] if lines[i].startswith("   ") else lines[i])
                i += 1
            # Strip trailing blank lines
            while code_lines and code_lines[-1].strip() == "":
                code_lines.pop()
            out.append(f"```{lang}")
            out.extend(code_lines)
            out.append("```\n")
            continue

        # Strip .. note::, .. warning::, .. tip:: etc. — keep content
        m_admonition = re.match(r"^\.\. (note|warning|tip|important|seealso)::", line)
        if m_admonition:
            admonition = m_admonition.group(1).upper()
            i += 1
            # Skip blank lines
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            out.append(f"**{admonition}**:")
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                content = lines[i][3:] if lines[i].startswith("   ") else lines[i]
                out.append(content)
                i += 1
            out.append("")
            continue

        # Strip .. plot:: directives entirely
        if re.match(r"^\.\. plot::", line):
            i += 1
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                i += 1
                if i < len(lines) and not lines[i].startswith("   ") and lines[i].strip():
                    break
            continue

        # Convert .. list-table:: to plain text rows
        if re.match(r"^\.\. list-table::", line):
            i += 1
            # Skip options (:header-rows:, :widths:, etc.) and blanks
            while i < len(lines) and (
                lines[i].strip() == "" or re.match(r"^\s+:\w", lines[i])
            ):
                i += 1
            # Parse rows: "   * - cell" starts a row, "     - cell" continues it
            rows: list[list[str]] = []
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                stripped = lines[i].strip()
                if stripped.startswith("* -"):
                    rows.append([stripped[3:].strip()])
                elif stripped.startswith("-") and rows:
                    rows[-1].append(stripped[1:].strip())
                i += 1
            # Render as markdown-ish table
            if rows:
                for row_idx, row in enumerate(rows):
                    out.append("| " + " | ".join(row) + " |")
                    if row_idx == 0:
                        out.append("|" + "|".join("---" for _ in row) + "|")
                out.append("")
            continue

        # Strip .. image:: and .. figure:: directives
        if re.match(r"^\.\. (image|figure)::", line):
            i += 1
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                i += 1
                if i < len(lines) and not lines[i].startswith("   ") and lines[i].strip():
                    break
            continue

        # Skip toctree directives
        if re.match(r"^\.\. toctree::", line):
            i += 1
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                i += 1
                if i < len(lines) and not lines[i].startswith("   ") and lines[i].strip():
                    break
            continue

        # Strip role markup: :func:`foo` -> foo, :math:`x` -> $x$
        line = re.sub(r":math:`([^`]+)`", r"$\1$", line)
        line = re.sub(r":(func|class|meth|attr|mod|data|const|exc|obj|ref|doc):`~?([^`]+)`", r"`\2`", line)

        out.append(line)
        i += 1

    return "\n".join(out)


def extract_guides(docs_dir: Path) -> list[tuple[str, str]]:
    """Extract guide content from RST files.

    Returns:
        list of (title, converted_content) tuples in presentation order.
    """
    guides_dir = docs_dir / "guides"
    guides = []
    for slug in GUIDE_ORDER:
        rst_path = guides_dir / f"{slug}.rst"
        if not rst_path.exists():
            print(f"Warning: guide not found: {rst_path}", file=sys.stderr)
            continue
        text = rst_path.read_text(encoding="utf-8")
        converted = _strip_rst(text)
        # Extract title from first line
        title_lines = converted.strip().split("\n", 1)
        title = title_lines[0].lstrip("#").strip() if title_lines else slug
        guides.append((title, converted))
    return guides


def render_tutorials(guides: list[tuple[str, str]]) -> str:
    """Render the tutorials section."""
    parts = ["# Tutorials\n"]
    for _title, content in guides:
        parts.append(content.strip())
        parts.append("\n---\n")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Output generation
# ---------------------------------------------------------------------------


def generate_llms_txt() -> str:
    """Generate the concise llms.txt content."""
    return f"""\
# {PROJECT_NAME}

> {PROJECT_DESC}

- [Full API & Tutorial Reference]({DOCS_BASE_URL}/llms-full.txt)
- [Documentation]({DOCS_BASE_URL}/)
- [GitHub Repository]({GITHUB_URL})
- [PyPI](https://pypi.org/project/pyminidsp/)
"""


def generate_llms_full_txt(api_ref: str, tutorials: str) -> str:
    """Generate the full llms-full.txt content."""
    header = f"""\
# {PROJECT_NAME}

> {PROJECT_DESC}

Source: {GITHUB_URL}
Documentation: {DOCS_BASE_URL}/
"""
    return f"{header}\n{api_ref}\n{tutorials}"


def generate(output_dir: str | Path) -> None:
    """Generate both llms.txt and llms-full.txt in the given directory."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find docs directory (relative to project root)
    project_root = Path(__file__).resolve().parent.parent
    docs_dir = project_root / "docs"

    md = _import_pyminidsp()

    # Extract API
    categories = extract_api(md)
    api_ref = render_api_reference(categories)

    # Extract tutorials
    guides = extract_guides(docs_dir)
    tutorials = render_tutorials(guides)

    # Write llms.txt
    llms_path = output_dir / "llms.txt"
    llms_path.write_text(generate_llms_txt(), encoding="utf-8")
    print(f"Wrote {llms_path}")

    # Write llms-full.txt
    full_path = output_dir / "llms-full.txt"
    full_path.write_text(generate_llms_full_txt(api_ref, tutorials), encoding="utf-8")
    print(f"Wrote {full_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Generate llms.txt and llms-full.txt for pyminidsp."
    )
    parser.add_argument(
        "--output-dir",
        default="docs/_build/html",
        help="Directory to write output files (default: docs/_build/html)",
    )
    args = parser.parse_args()
    generate(args.output_dir)


if __name__ == "__main__":
    main()
