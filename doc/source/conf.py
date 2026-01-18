# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
project = 'Turtle Python'
copyright = '2024-2026, Turtle Python'
author = 'Turtle Python'
version = '0.1.1'
release = '0.1.1'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',  # For Google/NumPy style docstrings
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for autodoc -----------------------------------------------------
# This is crucial for handling decorated functions properly
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Show both class and __init__ docstring
autoclass_content = 'both'

# Keep decorator metadata
autodoc_preserve_defaults = True

# Mock imports for Tkinter if needed
autodoc_mock_imports = []

# -- Options for intersphinx -------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
html_theme_options = {
    'description': 'Python implementation of the Oxford Turtle System',
    'github_user': 'turtleoxford',
    'github_repo': 'turtle-python',
    'github_banner': True,
}

# -- Options for LaTeX output ------------------------------------------------
latex_engine = 'pdflatex'
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
    'extraclassoptions': 'openany',
    'preamble': r'''
\usepackage{charter}
\usepackage[defaultsans]{lato}
\usepackage{inconsolata}
\setcounter{tocdepth}{2}
''',
    'fncychap': '\\usepackage[Bjornstrup]{fncychap}',
    'printindex': '\\footnotesize\\raggedright\\printindex',
}

latex_documents = [
    ('index', 'TurtlePython.tex', 'Turtle Python Documentation',
     'Turtle Python', 'manual'),
]

# Group member documentation by type
latex_use_modindex = True

# -- Options for manual page output ------------------------------------------
man_pages = [
    ('index', 'turtlepython', 'Turtle Python Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    ('index', 'TurtlePython', 'Turtle Python Documentation',
     author, 'TurtleOxford', 'Python implementation of the Oxford Turtle System.',
     'Miscellaneous'),
]

# -- Napoleon settings -------------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True
