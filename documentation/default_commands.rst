Default Commands
================

.. code-block::
    :caption: Module path

    sphinx_doclang.commands

~~~~

Overview
--------

DocLang includes a very small set of built‑in commands that form the core of the language.
These commands are intentionally minimal: they provide only the essential building blocks required
for formatting titles, creating sections, generating delimiters and inspecting internal DocLang state
during development.

The default commands are not meant to cover every documentation pattern.
Most projects define their own commands because documentation needs differ widely between users, domains and codebases.
DocLang treats commands as project‑level features, not global standards, which means that custom commands can freely
override or replace the defaults without restriction.

This page documents the commands that DocLang provides out of the box.
They are intended primarily as examples of how commands behave, how arguments are parsed and how output is generated.
Debug and introspection commands are also included to help developers understand the current object context
and verify template values during command development.

For real‑world documentation, users are expected to extend DocLang with their own commands
tailored to their project’s structure, style and requirements.

~~~~

Reference
---------

.. automodule:: sphinx_doclang.commands
    :ignore-module-all: