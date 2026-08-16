Tutorials
=========

Overview
--------

The tutorials in this section provide a guided introduction to the core
concepts of DocLang. Each page focuses on one part of the system and explains
how it behaves, how it interacts with Sphinx and how you can extend it for
your own project.

DocLang is intentionally minimal. It provides only the essential building
blocks needed to structure documentation, while leaving all project‑specific
behavior to the user. Because of this design, the tutorials are organized
around the core features that every project will use:

- **Commands** – How projects can define their own commands and used.
- **Templates** – How DocLang loads template files from the filesystem, how
  ``type`` and ``name`` determine which template is used and how placeholders
  are substituted.

Each tutorial page explains the purpose of its topic, shows practical examples,
and describes how the feature fits into the overall DocLang workflow. Together,
these tutorials form a complete introduction to the DSL and provide the
foundation needed to build project‑specific commands, templates and
documentation structures.

~~~~

Contents
--------

.. toctree::
	:maxdepth: 1
	:glob:

	tutorials/*