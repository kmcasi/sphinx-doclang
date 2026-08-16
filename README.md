# Doc Lang – Sphinx extension

This Sphinx extension introduces **DocLang**, a lightweight domain‑specific language designed to generate structured, 
expressive and automation‑friendly documentation blocks inside Python docstrings.

---

## Why DocLang Exists

DocLang began as a simple keyword replacer — a lightweight way to inject small
pieces of text into docstrings. Over time, it evolved into a flexible inline
command system with templates, introspection, and automation features. Despite
this growth, the core idea has remained the same:

```
DocLang helps automate repetitive parts of documentation.
```

Most projects contain patterns that repeat across multiple classes. In UI/UX
libraries, this is especially common: attributes such as `text_color`, `font_size` or `font_name`
appear in many widgets and their descriptions often differ only by a few words.
DocLang allows you to define custom commands and templates that encapsulate these
repetitive descriptions, letting you focus on the actual implementation instead
of rewriting boilerplate documentation.

The same applies to event systems. For example, in a button or other behavior
class, events often follow predictable naming and implementation patterns. With
DocLang, you can create a command that scan a class for events, locate
their implementations, extract the docstring descriptions and automatically
generate an event list at the top of the page. This means you can add or remove
events without worrying about manually updating the documentation — DocLang
handles it for you.

DocLang is designed to be extended. Users are encouraged to define their own
commands based on the needs of their project, creating a documentation workflow
that is both expressive and maintainable.

---

## Features

- **New commands** ➜ Creating custom commands.
- **Overwrite commands** ➜ Override existing commands with your own implementations.
- **Default commands** ➜ Simple built‑in commands for generating *delimiters*, *titles*, *sections*, and *lists*.
- **Self‑introspection commands** ➜ Retrieve the object's *name*, *type*, *documentation*, and *signature*.
- **Templates** ➜ Eliminate repetitive content for a specific object name or type.

DocLang is designed to keep your docstrings readable while producing rich, structured documentation output.

---

## Requirements

- **Python** ➜ ***3.12+***
- **Sphinx** ➜ ***9.1.0+***

---

## Installation

```bash
pip install sphinx-doclang
```

---

## Usage

### Enable the extension
In your `conf.py`, add the extension to the `extensions` list.  
Below is some preview for what you need for this Sphinx configuration:

```python
extensions = [
    ...,
    
    "sphinx.ext.autodoc",           # pull in docstrings from code
    
    "sphinx_doclang"                # DSL for documentation language
]
```

### Example of usage

DocLang commands can be used directly inside docstrings:

```python
class Example:
    """
    A simple example class.
	
    § list : First item, Second item, Third item ¶

    § section : debug purpose only, style = camel ¶

    § debug object ¶
    """
```

DocLang commands always begin with ```§ command : arguments ¶```. 
The DSL is intentionally minimal and easy to read inside source code.

---

### Configuration options

The extension provides the following configuration variables, shown here with their default values:

```python
# Marks the beginning of a DocLang command.
doclang_command_start = "§"

# Marks the end of a DocLang command.
doclang_command_end = "¶"

# Separate the command name from its arguments.
doclang_command_splitter = ":"

# Separate multiple arguments inside a command.
# Each character acts as an independent argument separator.
doclang_argument_separator = ",;"

# Separate keywords from their assigned values.
doclang_keyword_separator = "="

# Marks comments inside DocLang command blocks.
# Each character acts as an independent comment marker.
doclang_comment_marker = "#"

# Characters used to escape DocLang syntax when literal text is required.
# Each character acts as an independent escape marker.
doclang_escape_marker = "/|"

# Whether unknown/unregistered commands should be preserved instead of removed.
doclang_keep_unknown = False
```
