:hide-toc:

DocLang documentation
=====================

Overview
--------

DocLang is a lightweight documentation language designed to enhance Python
docstrings and generate structured output through Sphinx autodoc. It provides
a small set of inline commands that help you write clearer, richer and more
consistent documentation directly inside your code.

With DocLang, you can:

- Add structured sections inside docstrings
- Describe attributes and events in a uniform way
- Insert titles, lists and formatted blocks
- Build reusable documentation templates
- Reduce repetitive documentation work

DocLang works entirely through Sphinx autodoc, making it easy to integrate into
any existing documentation workflow.

~~~~

Quick Example
-------------

Below is a simple example showing how DocLang commands can enrich a docstring:

.. code-block:: python

   class Example:
    """
    A simple example class.

    § list : First item, Second item, Third item ¶

    § section : debug purpose only, style = camel ¶

    § debug object ¶
    """

DocLang commands always begin with ``§ command : arguments ¶``.
The DSL is intentionally minimal and easy to read inside source code.

~~~~

Contents
--------

DocLang is designed to stay small, simple and practical — giving you powerful
documentation tools without adding complexity to your project.

The following pages will guide you through installation, configuration and usage:

.. include:: contents.rst.inc
