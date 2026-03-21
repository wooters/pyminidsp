"""Sphinx configuration for pyminidsp documentation."""

import os
import sys

# -- Path setup ---------------------------------------------------------------
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(".."))

# -- Project information ------------------------------------------------------
project = "pyminidsp"
copyright = "2026, Chuck Wooters"
author = "Chuck Wooters"
release = "0.6.1"

# -- General configuration ----------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Generate audio samples at build time ------------------------------------
def _generate_audio(app):
    """Generate WAV audio samples before the build reads source files."""
    audio_dir = os.path.join(app.srcdir, "_static", "audio")
    marker = os.path.join(audio_dir, ".generated")
    if os.path.exists(marker):
        return  # already generated this build
    try:
        from gen_audio_samples import generate
        print("Generating audio samples for documentation...")
        generate(audio_dir)
        # Write marker so we don't regenerate on every rebuild
        with open(marker, "w") as f:
            f.write("ok\n")
    except ImportError as exc:
        print(f"Warning: audio sample generation skipped: {exc}")
        print("Audio previews will not be available in the built docs.")


def _generate_plots(app):
    """Generate interactive Plotly HTML plots before the build."""
    plots_dir = os.path.join(app.srcdir, "_static", "plots")
    marker = os.path.join(plots_dir, ".generated")
    if os.path.exists(marker):
        return
    try:
        from gen_signal_plots import generate
        print("Generating interactive plots for documentation...")
        generate(plots_dir)
        with open(marker, "w") as f:
            f.write("ok\n")
    except ImportError as exc:
        print(f"Warning: plot generation skipped: {exc}")
        print("Interactive plots will not be available in the built docs.")


def _generate_llms_txt(app, exception):
    """Generate llms.txt and llms-full.txt into the build output directory."""
    if exception:
        return
    try:
        # Add scripts/ to path so we can import the generator
        scripts_dir = os.path.join(os.path.dirname(app.srcdir), "scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        from gen_llms_txt import generate
        print("Generating llms.txt and llms-full.txt...")
        generate(app.outdir)
    except ImportError as exc:
        print(f"Warning: llms.txt generation skipped: {exc}")


def setup(app):
    app.connect("builder-inited", _generate_audio)
    app.connect("builder-inited", _generate_plots)
    app.connect("build-finished", _generate_llms_txt)

# -- Autodoc ------------------------------------------------------------------
autodoc_mock_imports = ["pyminidsp._minidsp_cffi"]
autodoc_member_order = "bysource"
autodoc_typehints = "description"

# -- Napoleon (Google-style docstrings) ---------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_use_rtype = False

# -- Intersphinx --------------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# -- HTML output --------------------------------------------------------------
html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/wooters/pyminidsp",
    "source_branch": "main",
    "source_directory": "docs/",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/wooters/pyminidsp",
            "html": (
                '<svg stroke="currentColor" fill="currentColor" stroke-width="0"'
                ' viewBox="0 0 16 16">'
                '<path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54'
                " 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38"
                " 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13"
                "-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87"
                " 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95"
                " 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21"
                " 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04"
                " 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82"
                " 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0"
                ' 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0'
                ' 16 8c0-4.42-3.58-8-8-8z"></path>'
                "</svg>"
            ),
            "class": "",
        },
    ],
}
html_static_path = ["_static"]
html_title = "pyminidsp"
