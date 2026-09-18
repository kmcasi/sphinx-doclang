New
===

Overview
--------

DocLang allows projects to define their own commands to extend the DSL with
custom behavior. New commands are useful when you want to generate additional
documentation content, perform introspection or introduce project‑specific
features that are not part of the default command set.

~~~~

Example
-------

New commands are created using the ``@Command.new()`` decorator. The decorator
accepts the command name and the decorated function receives the current
DocLang context and the parsed arguments.

For example, a simple command that prints a greeting:

.. code-block:: Python3
    :linenos:

    from sphinx_doclang.commands import Command

    @Command.new("hi")
    def hello_command(name, *args, **kwargs):
        return f"Hello {name}!"

This command can be used in any documentation string:

.. code-block:: Python3
    :linenos:

    class MyClass:
        """
        Some class documentation.

        § hi : MyClass ¶
        """

