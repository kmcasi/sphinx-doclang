Getting Started
===============

This page guides you through installation, activation and the basic syntax rules
you need to start using DocLang immediately.

Prerequisites
-------------

DocLang works as an extension on top of
`Sphinx’s autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_ system.
Before continuing, ensure you have a working ``conf.py`` file and you are familiar with:

- Standard Sphinx build commands (``make html`` or ``sphinx-build``)
- How Sphinx loads and processes docstrings
- How to use `Sphinx autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#usage>`_

~~~~

Installation
------------

DocLang can be installed either from PyPI or directly from GitHub.

.. tab-set::

    .. tab-item:: PyPI

        .. code-block:: doscon

            C:\> pip install sphinx-doclang

        This installs the latest stable release published on `PyPI <https://pypi.org/project/sphinx-doclang/>`_.

    .. tab-item:: GitHub

        If you want to install the development version from `GitHub <https://github.com/kmcasi/sphinx-doclang>`_
        use the ZIP archive:

        .. code-block:: doscon

            C:\> pip install https://github.com/kmcasi/sphinx-doclang/archive/master.zip

~~~~

Activate the Extension
----------------------

Enable DocLang by adding it to the ``extensions`` list in your ``conf.py``:

.. code-block:: python

    extensions = [
        "sphinx.ext.autodoc",           # required: pull in docstrings from code
        ...,
        "sphinx_doclang"                # DSL for documentation language
    ]

Once added, Sphinx will automatically detect and process DocLang commands inside docstrings.

~~~~

Basic Syntax Rules
------------------

The DocLang commands follow the ``§ command : arguments ¶`` pattern.
Depending on the command, the arguments may be omitted entirely resulting in a minimal form such as ``§ command ¶``.

.. important::

     - Command names may contain multiple words separated by spaces.
     - Command names must be unique and they are not case-sensitive.
     - Commands always return strings (either a single string or a list of strings).
     - All arguments are provided as plain strings.
     - Depending on the command implementation, arguments may be optional.
