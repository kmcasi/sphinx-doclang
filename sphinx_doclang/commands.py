#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 27 Feb 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
__all__ = ("Command",)

#// IMPORT
from .manager import CommandManager as Command
from .manager import TemplateManager as _Template


#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| DocLang Default Commands
#//|>-----------------------------------------------------------------------------------------------------------------<|
# noinspection PyUnusedLocal
@Command.new("delimiter")
def cmd_delimiter(*args, decorator: str = "~", **kwargs) -> str:
    """
    Generates a small decorative delimiter line.

    The ``decorator`` character is just a preference repeated four times to form the output.

    Usage:
        - ``§ delimiter ¶``
        - ``§ delimiter : decorator = * ¶``
    """
    return decorator * 4


# noinspection PyUnusedLocal
@Command.new("title")
def cmd_title(name: str, *args, style: str = "Az", decorator: str = "=", **kwargs) -> str:
    """
    Generates a formatted title with an underline.

    The ``style`` option controls how the title text is transformed:
        - ``AZ`` or ``upper``       ➜ UPPERCASE
        - ``az`` or ``lower``       ➜ lowercase
        - ``Az`` or ``capitalize``  ➜ Capitalized
        - ``Az Az`` or ``camel``    ➜ Camel Case (capitalize each word)

    The underline is created by repeating the ``decorator`` character to match the length of the final title.

    Usage:
        - ``§ title : My Title ¶``
        - ``§ title : my title, style = upper, decorator = - ¶``
    """
    style_name: str = style.lower()
    print(f"[ TITLE ][ {name} ]", args, style)

    if style == "AZ" or style_name == "upper":
        name = name.upper()
    elif style == "az" or style_name == "lower":
        name = name.lower()
    elif style == "Az" or style_name == "capitalize":
        name = name.capitalize()
    elif style == "Az Az" or style_name == "camel":
        name = " ".join([word.capitalize() for word in name.split(" ")])

    return f"{name}\n{decorator * len(name)}"


# noinspection PyUnusedLocal
@Command.new("section")
def cmd_section(title: str, *args, style: str = "Az", decorator: str = "-", **kwargs) -> list[str]:
    """
    Creates a section block consisting of:
        - a delimiter line
        - an empty line
        - a formatted title

    The ``style`` and ``decorator`` options are passed directly to the ``title`` command.

    Usage:
        - ``§ section : My Section ¶``
        - ``§ section : utilities, style = upper, decorator = ~ ¶``
    """
    return [
        cmd_delimiter(),
        "",
        cmd_title(title, style=style, decorator=decorator)
    ]


#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| DocLang Debug Commands ➜ Debug Purpose Only
#//|>-----------------------------------------------------------------------------------------------------------------<|
# noinspection PyUnusedLocal
@Command.new("debug object")
def cmd_debug_object(*args, **kwargs) -> list[str]:
    """
    Displays debugging information for the current DocLang object.

    Usage:
        - ``§ debug object ¶``
    """
    return [
        cmd_delimiter(),
        "",
        cmd_title("DocLang ➜ Debug Object", decorator="-"),
        "",
        f"- DOC ➜ \"{_Template['DOC'][:21]}{'' if len(_Template['DOC']) < 22 else '...'}\"",
        *[f"- {' ➜ '.join(registry)}" for registry in _Template.items if registry[0] != "DOC"],
        "",
        cmd_delimiter()
    ]


# noinspection PyUnusedLocal
@Command.new("self name")
def cmd_self_name(*args, **kwargs) -> str:
    """
    Returns the name of the current object.

    By default, the short name (without module path) is returned.

    If any argument is provided, the full dotted name is returned instead.
    The actual value or number of arguments does not matter.
    Providing an argument simply acts as a flag to request the full name.

    Usage:
        - ``§ self name ¶``
        - ``§ self name : _ ¶``
    """
    if args:
        return _Template["name"]

    obj_name: list[str] = _Template["name"].rsplit(".", 1)
    return obj_name[len(obj_name) - 1]


# noinspection PyUnusedLocal
@Command.new("self type")
def cmd_self_type(*args, **kwargs) -> str:
    """
    Returns the type of the current object.

    The value corresponds to the internal ``type`` field stored in the DocLang template context, for example:
        - ``class``
        - ``function``
        - ``method``
        - ``module``

    Usage:
        - ``§ self type ¶``
    """
    return _Template["type"]


# noinspection PyUnusedLocal
@Command.new("self doc")
def cmd_self_doc(*args, **kwargs) -> str:
    """
    Returns the full documentation string of the current object.

    The content corresponds to the original docstring written by the developer,
    cleaned only for indentation and formatting consistency.

    Usage:
        - ``§ self doc ¶``
    """
    return _Template["doc"]


# noinspection PyUnusedLocal
@Command.new("self obj")
def cmd_self_obj(*args, **kwargs) -> str:
    """
    Returns the string representation of the current object.

    The surrounding angle brackets are removed to provide a cleaner output.

    Usage:
        - ``§ self obj ¶``
    """
    return _Template["obj"][1:-1]
