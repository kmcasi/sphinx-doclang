#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Configuration file for the Sphinx documentation builder.
#//| https://www.sphinx-doc.org/en/master/usage/configuration.html
#//|>-----------------------------------------------------------------------------------------------------------------<|
import os
import sys
from sphinx.application import Sphinx


sys.path.insert(0, os.path.abspath(".."))
# sys.path.insert(0, os.path.abspath("_extensions"))

# import documentation.doclang_cmd


#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Global variables
#//|>-----------------------------------------------------------------------------------------------------------------<|
root_conf: str = os.path.abspath(os.path.dirname(__file__))
root_project: str = os.path.abspath(os.path.join(root_conf, ".."))


#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Project information
#//| https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
#//|>-----------------------------------------------------------------------------------------------------------------<|
# The documented project’s name.
project = "DocLang"

# The project’s author(s).
author = "ASI"

# A copyright statement.
project_copyright = f"%Y. All rights are reserved by {author}."

# The major project version.
# If project does not draw a meaningful distinction between a ‘full’ and ‘major’ version, set both to the same value.
version = "26.7.12"

# The full project version, used also in the HTML templates.
# If project does not draw a meaningful distinction between a ‘full’ and ‘major’ version, set both to the same value.
release = version


#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| General configuration
#//| https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
#//|>-----------------------------------------------------------------------------------------------------------------<|
# Set a minimum supported version of Sphinx required to build the project.
needs_sphinx = "9.1.0"

# These values determine how to format the current date.
today = "%d %b %Y"

# The default language to highlight source code in. The value should be a valid Pygments lexer name.
# highlight_language = "default"

# Dictionary that maps Pygments lexer names to their options.
highlight_options = {"default": {"linenos": True}}

# The style name to use for Pygments highlighting of source code.
# pygments_style = "sphinx"

# The style name to use for Pygments highlighting of source code. (Furo-specific at this time)
# pygments_dark_style = "monokai"

# A list of glob-style patterns that should be excluded when looking for source files.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**/.git"]

# A list of paths that contain extra templates.
templates_path = ["_templates"]

# Whether module names are prepended to all object names
# Most noticeable in generated content (e.g.: `.. automodule::`)
add_module_names = False

# Whether parentheses are appended to function and method role text
# Most noticeable in local toc
add_function_parentheses = False

# How domain objects (functions, classes, attributes, etc.) are displayed in local toc
# values: "domain", "hide" and "all"
toc_object_entries_show_parents = "hide"

# A list of strings that are module names of Sphinx extensions.
extensions = [
    # "sphinx.ext.autodoc",           # pull in docstrings from code
    "sphinx.ext.napoleon",          # support Google/NumPy-style docstrings
    "sphinx.ext.intersphinx",       # link to external docs (Python, etc.)

    "sphinx_copybutton",            # small “copy” button at the right of all `.. code-block::` directives
    "sphinx_design",                # screen-size responsive web-components

    # Custom extensions
    "sphinx_localtoc",              # [pip sphinx_localtoc] stylizing the local ToC
    # "sphinx_doclang"                # DSL for documentation language (this project)
]


#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Extensions settings
#//| Sphinx:            https://www.sphinx-doc.org/en/master/usage/extensions/index.html#builtin-extensions
#//| Sphinx CopyButton: https://sphinx-extensions.readthedocs.io/en/latest/sphinx-copybutton.html
#//| Sphinx Design:     https://sphinx-design.readthedocs.io/en/furo-theme/get_started.html
#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| sphinx.ext.autodoc
#//|>--------------------------------------------------------<|
# Define the order in which automodule and autoclass members are listed.
# values: "alphabetical", "groupwise" and "bysource"
autodoc_member_order = "bysource"

# A dictionary of options that influence the generated documentation.
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

#//| sphinx.ext.intersphinx
#//|>--------------------------------------------------------<|
# Names and locations of other projects that should be linked to in this documentation.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

#//| sphinx_copybutton
#//|>--------------------------------------------------------<|
# Skip all prompt characters generated by pygments.
copybutton_exclude = ".linenos, .gp"

# Input prompts for code cells.
copybutton_prompt_text = r">>> |\.\.\. |\$ |^[A-Z]:\\(?:[\w\-]+\\)*[\w\-]*> ?"

# If `copybutton_prompt_text` is regexp in a raw string (r"")
copybutton_prompt_is_regexp = True

# Whether the input prompts should be stripped
copybutton_remove_prompts = True

# Keep empty lines.
copybutton_copy_empty_lines = True

# Prevent copybuttons from being added to code blocks, by adding >> :class: no-copybutton << to the code block.
copybutton_selector = "div:not(.no-copybutton) > div.highlight > pre"

# Use a different image for copy buttons
# https://fontawesome.com/search#icongrid
copybutton_image_svg = """
<svg xmlns="http://www.w3.org/2000/svg" 
    class="icon icon-tabler icon-tabler-copy" 
    width="44" 
    height="44" 
    viewBox="0 0 448 512" 
    fill="currentColor"
>
    <title>${messages[locale]['copy_to_clipboard']}</title>
    <path d="M384 336l-192 0c-8.8 0-16-7.2-16-16l0-256c0-8.8 7.2-16 16-16l140.1 0 L400 115.9 400 320c0 8.8-7.2 16-16 
        16z M192 384l192 0c35.3 0 64-28.7 64-64l0-204.1c0-12.7-5.1-24.9-14.1-33.9 L366.1 14.1c-9-9-21.2-14.1-33.9-14.1 
        L192 0c-35.3 0-64 28.7-64 64l0 256c0 35.3 28.7 64 64 64z"
    />
    <path d="M64 128c-35.3 0-64 28.7-64 64 L0 448c0 35.3 28.7 64 64 64l192 0c35.3 0 64-28.7 64-64l0-32-48 0 0 32c0 
        8.8-7.2 16-16 16 L64 464c-8.8 0-16-7.2-16-16l0-256c0-8.8 7.2-16 16-16l32 0 0-48-32 0z"
    />
</svg>
"""

#//| sphinx_design
#//|>--------------------------------------------------------<|
# Output FontAwesome icons on LaTeX (LaTex not configured yet...)
sd_fontawesome_latex = True

#//| sphinx_localtoc
#//|>--------------------------------------------------------<|
# Number of initial ToC depth levels to skip before applying dropdown logic.
localtoc_dropdown_depth = 2


#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Options for HTML output
#//| Sphinx:    https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
#//| Furo:      https://pradyunsg.me/furo/quickstart/
#//|>-----------------------------------------------------------------------------------------------------------------<|
# The theme for HTML output.
html_theme = "furo"

# A dictionary of options that influence the look and feel of the selected theme. These are theme-specific.
html_theme_options = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/kmcasi/sphinx-doclang",
            "html": "",
            "class": "fa-brands fa-solid fa-github fa-2x",
        },
    ],
}

# Title for the navigation bar. If None, it defaults to "<project> <release> documentation".
html_title = f"{project} {release} doc"

# A shorter title for the navigation bar. Default is the same as html_title.
html_short_title = f"{project} doc"

# A list of paths that contain custom static files (such as style sheets or script files).
html_static_path = ["_static"]

# Logo used at the top of the sidebar. Must not exceed 200 pixels.
html_logo = f"{html_static_path[0]}/logo_doclang.png"

# Webpage icon. Should be a 16x16 pixels (PNG, SVG, GIF, or ICO).
html_favicon = f"{html_static_path[0]}/icon_doclang.png"

# A list of CSS files. The entry must be a filename or a tuple containing the filename and the attribute's dictionary.
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    # "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",

    "styles/custom_furo.css",
    "styles/custom_sphinx-design.css",
    "styles/doclang.css",
]

# A list of JS files. The entry must be a filename or a tuple containing the filename and the attribute's dictionary.
html_js_files = ["scripts/doclang.js"]

# Text for link anchors for each heading and description environment. HTML entities and Unicode are allowed.
html_permalinks_icon = "&#10070;"

# If true, the reST sources are included in the HTML build as ``_sources/<docname>``.
html_copy_source = False

# If True (and html_copy_source is true as well), links to the reStructuredText sources will be added to the sidebar.
html_show_sourcelink = False
