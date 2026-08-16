Configuration
=============

Overview
--------

DocLang provides several configuration variables that control how commands are detected, parsed and interpreted.
This page describes each option and explains the syntax rules that depend on them.

All configuration variables are optional. If not specified, DocLang uses the default values shown below.

~~~~

Variables
---------

The following variables can be added to your ``conf.py`` file:

.. code-block:: python

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

~~~~

Syntax Rules
------------

DocLang commands follow a simple pattern based on the configuration variables defined above.
Understanding these rules will help you write correct and predictable command blocks inside your docstrings.

The sections below explain how each part of the syntax works.

.. important::

    When customizing any syntax, be careful to avoid reusing characters.
    Even if the sequences appear visually distinct, DocLang checks each character individually.
    If any character is used more than once across all delimiters, splitters, separators or markers,
    DocLang will raise an ``InvalidConfigError``.

    .. code-block:: python
        :caption: Invalid configuration example

        doclang_command_start = "<<"
        doclang_command_end = ">>"
        doclang_command_splitter = ">:<"

    .. code-block:: text
        :caption: Usage

        << title >:< example splitter >>

    .. code-block:: console
        :class: no-copybutton
        :caption: Terminal output

        Traceback
        =========

              File "E:\Python\PublicWork\sphinx-doclang\sphinx_doclang\processor.py", line 399, in validate_command_configuration_values
                raise error
            sphinx_doclang.error.InvalidConfigError: [DocLang Error] The character '>' in 'doclang_command_splitter' is already used in 'doclang_command_end'.
                [Suggestion] Use distinct characters across all command tags, separators and markers.

~~~~

Command Delimiters
++++++++++++++++++

.. code-block:: python
    :caption: Configuration variables

    # Marks the beginning of a DocLang command.
    doclang_command_start = "§"

    # Marks the end of a DocLang command.
    doclang_command_end = "¶"

A command is always wrapped between the start and end markers:

.. code-block:: text

    § command ¶

.. code-block:: text
    :caption: Example

    § debug object ¶

.. dropdown:: Customization
    :icon: alert

    The start and end markers are treated as complete units.
    If you configure them using multiple characters, the entire sequence must be used exactly as defined.

    .. code-block:: python
        :caption: Modified configuration variables

        doclang_command_start = "<<"
        doclang_command_end = ">>"

    .. code-block:: text
        :caption: Usage

        << debug object >>

    .. code-block:: text
        :class: no-copybutton
        :caption: Output

        ~~~~

        Doclang ➜ debug object
        ----------------------

        - DOC ➜ (the object documentation)
        - NAME ➜ sphinx_doclang.debug.Debug
        - TYPE ➜ class
        - OBJ ➜ <class 'sphinx_doclang.debug.Debug'>

        ~~~~

    .. note::

       The default command delimiters ``§`` and ``¶`` were chosen not only for their
       visual clarity but also for their typing convenience. Both characters can be
       entered easily on a standard keyboard with a numeric keypad:

       - ``§`` ➜ ALT + 21
       - ``¶`` ➜ ALT + 20

       This makes the default configuration comfortable to use even in workflows
       where DocLang commands are typed frequently.

~~~~

Command Splitter
++++++++++++++++

.. code-block:: python
    :caption: Configuration variable

    # Characters used to separate the command name from its arguments.
    doclang_command_splitter = ":"

Most commands require one or more arguments.
The splitter separates the command name from its arguments:

.. code-block:: text

    § command : arguments ¶

.. code-block:: text
    :caption: Example

    § title : example command ¶

.. dropdown:: Customization
    :icon: alert

    The splitter marker is treated as a complete unit.
    If you configure it using multiple characters, the entire sequence must be used exactly as defined.

    .. code-block:: python
        :caption: Modified configuration variable

        doclang_command_splitter = ">:<"

    .. code-block:: text
        :caption: Usage

        § title >:< example splitter ¶

    .. code-block:: text
        :class: no-copybutton
        :caption: Output

        Example splitter
        ================

~~~~

Argument Separator
++++++++++++++++++

.. code-block:: python
    :caption: Configuration variables

    # Characters used to separate multiple arguments inside a command.
    # Each character acts as a valid separator.
    doclang_argument_separator = ",;"

Multiple arguments inside a command can be separated using any of the characters
defined in ``doclang_argument_separator``. Each character is interpreted as an
independent separator.

.. code-block:: text
    :caption: Example

    § list : width, height; depth ¶

.. dropdown:: Customization
    :icon: alert

    DocLang does not interpret the sequence as a complete unit.
    Instead, every character becomes a valid separator on its own.

    .. code-block:: python
        :caption: Modified configuration variable

        doclang_argument_separator = "|/"

    .. code-block:: text
        :caption: Usage

        § list : width | height / depth ¶

    .. code-block:: text
        :class: no-copybutton
        :caption: Output

        - width
        - height
        - depth

~~~~

Keyword Separator
+++++++++++++++++

.. code-block:: python
    :caption: Configuration variable

    # Character used to separate keywords from their assigned values.
    doclang_keyword_separator = "="

Some commands support keyword/value pairs. The keyword separator defines the
character used to assign a value to a keyword inside the argument block.

.. code-block:: text
    :caption: Example

    § section : title = overview ¶

In this example, ``title`` is the keyword and ``Overview`` is the assigned value.
The keyword separator ``=`` makes the relationship explicit and easy to parse.

.. dropdown:: Customization
    :icon: alert

    The keyword separator is treated as a complete unit.
    If you configure it using multiple characters, the entire sequence must be used exactly as defined.

    .. code-block:: python
        :caption: Modified configuration variable

        doclang_keyword_separator = "=+"

    .. code-block:: text
        :caption: Usage

        § section : title =+ overview ¶

    .. code-block:: text
        :class: no-copybutton
        :caption: Output

        ~~~~

        Overview
        --------

~~~~

Comments
++++++++

.. code-block:: python
    :caption: Configuration variable

    # Character used to mark comments inside DocLang command blocks.
    doclang_comment_marker = "#"

DocLang allows comments inside command blocks. A comment begins with the
configured marker and continues until the end of the command block. Comments are
ignored during processing and do not affect the command output.

.. code-block:: text
    :caption: Example

    § list : item 1, item 2, # item 3 ¶

In this example, everything after ``#`` is treated as a comment and removed
before the command is evaluated.

.. dropdown:: Customization
    :icon: alert

    The comment marker configuration accepts multiple characters.
    Each character in the sequence is treated as a valid separator on its own.

    .. code-block:: python
        :caption: Modified configuration variable

        doclang_comment_marker = "#@"

    .. code-block:: text
        :caption: Usage

        § list : item 1, item 2, @ item 3 ¶

    .. code-block:: text
        :class: no-copybutton
        :caption: Output

        - item 1
        - item 2

~~~~

Escaping
++++++++

.. code-block:: python
    :caption: Configuration variable

    # Characters used to escape DocLang syntax when literal text is required.
    # Each character acts as an independent escape marker.
    doclang_escape_marker = "/|"

DocLang provides an escape mechanism for situations where you need to include
characters that would normally be interpreted as part of a command. Any
character defined in ``doclang_escape_marker`` can be used to escape DocLang
syntax, allowing literal text to appear inside command blocks.

.. code-block:: text
    :caption: Example

    § list : item 1, item 2/, item 3|, item 4 ¶

In this example, the last two commas are treated as literal text because they are prefixed with escape markers.

.. dropdown:: Customization
    :icon: alert

    The escape marker configuration accepts multiple characters.
    Each character in the sequence is treated as an independent escape marker.

    .. code-block:: python
        :caption: Modified configuration variable

        doclang_escape_marker = "!?"

    .. code-block:: text
        :caption: Usage

        § list : item 1, item 2?, item 3!, item 4 ¶

    .. code-block:: text
        :class: no-copybutton
        :caption: Output

        - item 1
        - item 2, item 3, item 4

    .. dropdown:: Info
        :icon: comment

        Characters can also be escaped by enclosing them in double quotes ``"`` or single quotes ``'``.

        .. code-block:: text
            :caption: Example

            § list : item A, "item B," item C',' item D ¶

        .. code-block:: text
            :class: no-copybutton
            :caption: Output

            - item A
            - item B, item C, item D

~~~~

Unknown Commands
++++++++++++++++

.. code-block:: python
    :caption: Configuration variable

    # Whether unknown/unregistered commands should be preserved instead of removed.
    doclang_keep_unknown = False

By default, DocLang removes any command that is not registered or recognized by
the processor. This ensures that accidental typos, incomplete commands or
unsupported syntax do not appear in the generated documentation.

.. code-block:: text
    :caption: Example (default behavior)

    One § unknown command ¶ is here

.. code-block:: text
    :class: no-copybutton
    :caption: Output

    One is here

.. dropdown:: Customization
    :icon: alert

    When ``doclang_keep_unknown`` is set to ``True``, unknown commands are preserved
    exactly as written. This can be useful when experimenting with new command
    patterns, integrating custom extensions or debugging command behavior.

    .. code-block:: python
        :caption: Modified configuration variable

        doclang_keep_unknown = True

    .. code-block:: text
        :caption: Example (keep unknown)

        Other § unknown command ¶ is here

    .. code-block:: text
        :class: no-copybutton
        :caption: Output

        Other § unknown command ¶ is here
