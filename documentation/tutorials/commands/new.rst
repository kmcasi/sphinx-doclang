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

    @Command.new("hello")
    def hello_command(name, *args, **kwargs):
        return f"Hello {name}!"

~~~~

Notes
-----

Before a command is registered, DocLang performs a validation step to ensure
that the command can safely accept any number of arguments. If the command
defines a return type hint and supports multiple arguments, it is considered
valid immediately. Otherwise, DocLang simulates the command call with a large
number of arguments (up to 100) to verify that the implementation does not
break when users provide more arguments than expected.

This check ensures that all commands behave consistently inside the DSL, where
arguments are always passed as plain strings and the number of arguments cannot
be restricted.

- Command names must be unique.
- Command names are not case sensitive.
- Commands may accept arguments, but they are always passed as plain strings.
- Commands run during documentation generation, so they should be fast and deterministic.
- Commands must accept any number of positional and keyword arguments.
- Commands must return either a single string or a list of strings.
