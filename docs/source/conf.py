# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# For ideas:

# https://github.com/pradyunsg/furo/blob/main/docs/conf.py
# https://github.com/sphinx-gallery/sphinx-gallery/blob/master/doc/conf.py

# --------------------------------------------------------------------------

import sys
import os
from datetime import date

import sigmaepsilon.deepdict as library

from sphinx.config import Config

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../../src"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = library.__pkg_name__
copyright = "2014-%s, Bence Balogh" % date.today().year
author = "Bence Balogh"
version = library.__version__
release = "v" + library.__version__


def setup(app: Config):
    app.add_config_value("project_name", project, "html")


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",  # allows to work with markdown files
    "sphinx.ext.duration",  # to plot summary about durations of file generations
    "sphinx.ext.doctest",  # to test code snippets in docstrings
    "sphinx.ext.autodoc",  # for automatic exploration of the source files
    "sphinx.ext.intersphinx",  # to enable cross referencing other documents on the internet
    "sphinx.ext.napoleon",  # enables Sphinx to parse both NumPy and Google style docstrings
    "nbsphinx",  # to handle jupyter notebooks
    "sphinx_copybutton",  # for "copy to clipboard" buttons
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.extlinks",
    "sphinx_design",
    "sphinx_inline_tabs",
]

autosummary_generate = True

templates_path = ["_templates"]

exclude_patterns = ["_build"]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# The master toctree document.
master_doc = "index"

language = "EN"

# See warnings about bad links
nitpicky = True
nitpick_ignore = [
    ("", "Pygments lexer name 'ipython' is not known"),
    ("", "Pygments lexer name 'ipython3' is not known"),
]

# Pygments
pygments_style = "sphinx"
pygments_dark_style = "github-dark"
highlight_language = "python3"

intersphinx_mapping = {
    "python": (r"https://docs.python.org/{.major}".format(sys.version_info), None),
    "numpy": (r"https://numpy.org/doc/stable/", None),
    "scipy": (r"http://docs.scipy.org/doc/scipy/reference", None),
    "matplotlib": (r"https://matplotlib.org/stable", None),
    "sphinx": (r"https://www.sphinx-doc.org/en/master", None),
    "pandas": (r"https://pandas.pydata.org/pandas-docs/stable/", None),
    "sigmaepsilon.core": (r"https://sigmaepsiloncore.readthedocs.io/en/latest/", None),
    "sigmaepsilon.mesh": (r"https://sigmaepsilonmesh.readthedocs.io/en/latest/", None),
    "sigmaepsilon.solid.fourier": (r"https://sigmaepsilonsolidfourier.readthedocs.io/en/latest/", None),
}

# sphinx_copybutton configuration --------------------------------------------

copybutton_exclude = '.linenos, .gp, .go'
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = True

# napoleon config ---------------------------------------------------------

napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_ivar = True

# -- bibtex configuration -------------------------------------------------
# https://sphinxcontrib-bibtex.readthedocs.io/en/latest/usage.html

bibtex_bibfiles = ["references.bib"]
bibtex_default_style = "unsrt"

# If no encoding is specified, utf-8-sig is assumed.
# bibtex_encoding = 'latin'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "show_prev_next": True,
    "back_to_top_button": True,
    "icon_links": [
        {
            "name": "GitHub",
            "url": f"https://github.com/sigma-epsilon/{project}",
            "icon": "fab fa-github",
            "type": "fontawesome",
        },
        {
            "name": "PyPi",
            "url": f"https://pypi.org/project/{project}/",
            "icon": "fas fa-box-open",
            "type": "fontawesome",
        },
    ],
    "logo": {
        # Because the logo is also a homepage link, including "home" in the alt text is good practice
        "text": "SigmaEpsilon.DeepDict",
    },
}
html_js_files = [
    "require.min.js",
    "custom.js",
]
html_css_files = ["custom.css"]
html_context = {"default_mode": "light"}
html_static_path = ["_static"]

# -- nbsphinx configuration -------------------------------------------------

# This is processed by Jinja2 and inserted before each notebook
nbsphinx_prolog = r"""
{% set docname = "docs\\source\\" + env.doc2path(env.docname, base=None) %}

.. raw:: html

    <style>
        .nbinput .prompt,
        .nboutput .prompt {
            display: none;
        }
    </style>

    <div class="admonition note">
      This page was generated from
      <a class="reference external" href="https://github.com/sigma-epsilon/{{ env.config.project_name }}/blob/{{ env.config.release|e }}/{{ docname|e }}">{{ docname|e }}</a>.
    </div>

.. raw:: latex

    \nbsphinxstartnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{The following section was generated from
    \sphinxcode{\sphinxupquote{\strut {{ docname | escape_latex }}}} \dotfill}}
"""

# This is processed by Jinja2 and inserted after each notebook
nbsphinx_epilog = r"""
{% set docname = 'docs/source/' + env.doc2path(env.docname, base=None) %}
.. raw:: latex

    \nbsphinxstopnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{\dotfill\ \sphinxcode{\sphinxupquote{\strut
    {{ docname | escape_latex }}}} ends here.}}
"""
