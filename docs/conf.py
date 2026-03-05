"""Sphinx configuration for pyminidsp documentation."""

import os
import sys

# -- Path setup ---------------------------------------------------------------
sys.path.insert(0, os.path.abspath(".."))

# -- Project information ------------------------------------------------------
project = "pyminidsp"
copyright = "2026, Chuck Wooters"
author = "Chuck Wooters"
release = "0.1.0"

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
    except Exception as exc:
        print(f"Warning: audio sample generation failed: {exc}")
        print("Audio previews will not be available in the built docs.")


def setup(app):
    app.connect("builder-inited", _generate_audio)

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
html_static_path = ["_static"]
html_title = "pyminidsp"
