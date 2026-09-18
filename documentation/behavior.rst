Command Behavior
================

DocLang commands follow a defined set of rules that govern how they are parsed,
executed and assembled into the final documentation output. Understanding these
rules is essential when creating custom commands or working with nested command
structures.

Output Formatting
-----------------

DocLang commands are designed primarily for generating content in
reStructuredText (RST) format. The default commands, their return values and
their formatting conventions were created with RST syntax in mind, as DocLang
was built to integrate directly with Sphinx and its documentation pipeline.

DocLang’s flexibility allows users to automate content generation in any
format, but the responsibility for correct formatting lies with the command
implementation.

General Rules
-------------

- Command names must be unique. They are **not** case sensitive.
- Commands may accept positional and keyword arguments, but all arguments are always passed as **plain strings**.
- Commands execute during documentation generation, so they should be fast, deterministic and free of side effects.
- Commands must accept any number of positional and keyword arguments.
- Commands must return either:

  - a **single string**
  - a **list of strings**

Nested Commands
---------------

DocLang supports nested commands. A command may appear inside the arguments of
another command, for example:

.. code-block:: Text

    § command A : § command B ¶ ¶

The processor evaluates nested commands in logical order:

    1. The inner command (``command B``) is executed first.
    2. Its **string result** is passed as the argument to the outer command (``command A``).
    3. The outer command is then executed with the resolved argument.

.. note::
    Nested commands only work when the inner command returns a **single string**.
    If the inner command returns a **list of strings**, the expected behavior
    breaks. This limitation exists because DocLang processes commands line by line
    and list-returning commands are handled through a separate assembly mechanism.

Assembler Behavior
------------------

DocLang’s assembler processes output in two distinct modes depending on the
command’s return type.

Single-String Output
~~~~~~~~~~~~~~~~~~~~

- The returned string is inserted directly into the current line.
- If the string contains newline characters (``\n``), multiple lines are produced.
- Lines created via ``\n`` **do not inherit indentation** from the invocation line.

List-of-Strings Output
~~~~~~~~~~~~~~~~~~~~~~

- Each element in the list is treated as an independent output line.
- Each line **inherits the indentation** of the line where the command was invoked.
- This mechanism enables multi-line constructs such as dropdowns, usage blocks and other structured output.

Double Buffer Mechanism
-----------------------

DocLang uses a double-buffer assembly strategy:

    - The **primary buffer** handles normal line assembly.
    - The **secondary buffer** handles multi-line output from commands that return lists of strings.

Lines generated in the secondary buffer are:

    1. Constructed independently.
    2. Indented according to the invocation line.
    3. Appended immediately after the processed line.

This mechanism was originally introduced to prevent accidental list injection
from corrupting output. As DocLang evolved, it became essential for supporting
multi-line command output. A future version of DocLang may introduce a redesigned
assembler to unify these behaviors more cleanly.
