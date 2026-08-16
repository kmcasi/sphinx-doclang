Templates
=========

Overview
--------

DocLang templates provide a simple mechanism for reusing documentation fragments
that appear repeatedly across a project. Unlike commands, which perform logic or
transform input, templates are static text blocks that can be inserted anywhere a
DocLang command is allowed.

Templates are intentionally minimal. They do not include formatting rules,
conditional logic or dynamic behavior. Their purpose is to eliminate copy‑paste
patterns in documentation and to keep repeated descriptions consistent across
multiple classes, functions or modules.

Because documentation needs differ from project to project, DocLang does not
ship with predefined templates. Each project defines its own templates based on
its domain, naming conventions and documentation style. This ensures that
templates remain relevant and do not impose any global structure on users.

This page explains how templates are defined, how they are registered and how
they are inserted into docstrings using the standard DocLang syntax.

~~~~

Files and Directory
-------------------

DocLang templates are stored as plain text files on disk. To make them
discoverable, DocLang follows a strict directory rule: templates must be placed
inside a ``doclang`` subdirectory located under any directory listed in
``templates_path`` in ``conf.py``.

For example, if ``templates_path`` contains ``["_templates"]``, DocLang will look
for templates inside:

    _templates/doclang/

Only directories that contain a ``doclang`` folder are considered valid template
roots.

Template files use the ``.dlt`` extension. The file name and directory structure
are determined by the template type and name. A template referenced as
``type/name`` is loaded from:

    doclang/<type>/<name>.dlt

If the file does not exist, DocLang falls back to:

    doclang/<type>.dlt

This allows both nested and flat template layouts.

DocLang discovers template directories during Sphinx initialization by scanning
all paths listed in ``templates_path`` and collecting those that contain a
``doclang`` subdirectory. All template lookups search these directories in the
order they appear in ``templates_path``.

~~~~

Placeholders
------------

DocLang templates support simple placeholder substitution. A placeholder is
written using the ``{{ KEYWORD }}`` syntax and is replaced with the value of the
corresponding keyword when the template is rendered.

Placeholders do not execute logic and do not behave like commands. They are
purely textual substitutions performed inside the template body. This keeps
templates lightweight and predictable, while still allowing them to adapt to
the current documentation context.

Example::

    {{ DOC }}

In this example, ``{{ DOC }}`` is replaced with the value stored under the
``DOC`` keyword at render time. If the keyword is not defined, the placeholder
is left unchanged.

.. dropdown:: All placeholders
    :class-container: dl-code-item

    Using the ``§ debug object ¶`` command inside any docstring will generate a list of
    all available template placeholders and their current values.
    The ``DOC`` placeholder is shown only in a shortened form during debugging to
    prevent very large documentation blocks from cluttering the output.

    .. list-table::
        :header-rows: 0

        * - DOC
          - The current documentation object represented as a string.
        * - NAME
          - The name of the current object.
        * - TYPE
          - The type of the current object (for example: module, class, function).
        * - OBJ
          - The raw object reference used internally by DocLang.

~~~~

Creating First Template
-----------------------

This example shows the complete workflow for creating a template for a Python
class. Following this example you can create a template for any object.

Consider the following Python file:

.. code-block:: Python3

    class MyClass:
        """Some class description."""

        my_attribute = "Some value"
        """Some attribute description."""

[Step 1] Create a directory
+++++++++++++++++++++++++++

DocLang determines which template file to load based on two values extracted
from the current Python object being documented:

- **type** – the category of the object (for example: ``module``, ``class``,
  ``function``, ``method``, ``attribute``)
- **name** – the short identifier of the object as written in Python code

These two values map directly to the filesystem structure inside the
``doclang`` template directory.

    - for the class ``MyClass``:

      - ``type = "class"``
      - ``name = "MyClass"``

    - for the attribute ``my_attribute``:

      - ``type = "attribute"``
      - ``name = "my_attribute"``

Using these values, DocLang searches for template files inside any directory
listed in ``templates_path`` that contains a ``doclang`` subdirectory.

Assuming your ``conf.py`` contains:

.. code-block:: Python3

    templates_path = ["_templates"]

The expected file locations are:

    For the class example above, DocLang will first try::

        _templates/doclang/class/MyClass.dlt

    If the file does not exist, it falls back to::

        _templates/doclang/class.dlt

    For the attribute example, DocLang will first try::

        _templates/doclang/attribute/my_attribute.dlt

    And if missing, it falls back to::

        _templates/doclang/attribute.dlt

This mechanism allows projects to define highly specific templates for
individual objects, while also providing generic templates that apply to all
objects of a given type. The ``type`` directory may contain any number of
specific templates, each named after the corresponding Python object.

[Step 2] Create a template
++++++++++++++++++++++++++

To define a template specifically for ``MyClass``, create the file::

    _templates/doclang/class/MyClass.dlt

Inside this file, you may use any text and any placeholders supported by
DocLang. For example::

    {{ DOC }}

    Some repetitive information specifically for all classes named "MyClass".

    § debug object ¶

When DocLang processes ``MyClass``, this file is loaded and all placeholders are
substituted with the current values.

If the file ``doclang/class/MyClass.dlt`` does not exist, DocLang falls back to::

    _templates/doclang/class.dlt

which applies to all classes.

.. note::

    Depending on the operating system, file names may not be case-sensitive.
    For example, on Windows the following file name is also accepted::

        _templates/doclang/class/myclass.dlt

    On case-sensitive file systems (such as most Linux distributions), the file
    name must match the exact class or attribute name, including uppercase and
    lowercase letters.

[Step 3] Build the documentation
++++++++++++++++++++++++++++++++

Once the template files are in place, run the Sphinx build. DocLang will:

1. detect the object type (``class``)
2. detect the object name (``MyClass``)
3. load ``class/MyClass.dlt`` if it exists
4. otherwise load ``class.dlt`` if it exists
5. substitute all placeholders (``{{ DOC }}``)
6. insert the rendered template into the final documentation

This completes the template workflow.
No additional commands or configuration are required.