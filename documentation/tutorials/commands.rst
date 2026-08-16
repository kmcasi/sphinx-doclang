Commands
========

Overview
--------

DocLang allows projects to define their own commands or overwrite existing ones.
All commands are implemented in Python and must be registered before Sphinx
builds the documentation. This section explains the common workflow required for
both new commands and overwrite commands.

~~~~

[Step 1] Create a Python file
+++++++++++++++++++++++++++++

Commands may be placed anywhere inside your project, as long as the file is
importable by Sphinx. A common layout is::

    my_project/
        ...
    docs/
        conf.py
        doclang_commands.py
        ...

The file name and location are not important; only the import path matters.

[Step 2] Import the Command
+++++++++++++++++++++++++++

Inside the newly created file, import the ``Command`` class:

.. code-block:: Python3

    from sphinx_doclang.commands import Command

This class provides the decorator used to register new commands or overwrite existing ones.

[Step 3] Import your file
+++++++++++++++++++++++++

Sphinx must import your command file so that the command is registered before
the documentation is processed. Add an import statement to ``conf.py``:

.. code-block:: Python3

    import docs.doclang_commands

The import has no side effects other than registering the commands.

~~~~

Next Steps
----------

The following subsections explain how to create new commands and how to
overwrite existing ones:

- **New Commands** – How to define project-specific commands that extend DocLang's behavior.
- **Overwrite Commands** – How to replace or modify default commands.

Both types of commands follow the same registration workflow described above.

.. toctree::
    :maxdepth: 1
    :glob:

    commands/*