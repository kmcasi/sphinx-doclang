Overwrite
=========

Overview
--------

DocLang allows projects to replace any commands with their own implementation.
Overwriting a command is useful when you want to change the behavior of an
built‑in commands such as ``title``, ``section``, ``delimiter`` or any custom commands.

The workflow for overwriting a command is identical to creating a new one: you
place the command in a Python file inside your project and import that file in
``conf.py`` so that Sphinx loads it during the build.

~~~~

Example
-------

To overwrite a command, use the ``@Command.overwrite()`` decorator and specify
the exact name of the command you want to replace. For example, to overwrite the
built‑in ``title`` command:

.. code-block:: Python3
    :linenos:

    from sphinx_doclang.commands import Command

    @Command.overwrite("title")
    def custom_title(context, *args, decorator="=", **kwargs):
        title = f"[ {context} ]"
        underline = decorator * len(title)
        return f"{title}\n{underline}"

The new implementation completely replaces the default ``title`` command. Any
docstring using ``§ title : ... ¶`` will now execute this version instead of the
original.
