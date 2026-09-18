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

Note
----

Overwriting a command does not validate whether the new implementation matches
the original command’s argument count, argument names or return type.
The overwrite mechanism exists solely to prevent users from accidentally defining
multiple commands with the same name.

If a second command with an identical name is created without using the
overwrite flag, Sphinx will fail during the documentation build. The overwrite
feature ensures that users are explicitly aware they are redefining an existing
command and that the new behavior intentionally differs from the original
implementation.

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
        return [title, underline]

The new implementation completely replaces the default ``title`` command. Any
docstring using ``§ title : ... ¶`` will now execute this version instead of the
original.

