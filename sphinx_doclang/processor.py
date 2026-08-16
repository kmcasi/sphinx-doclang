#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 15 Feb 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
__all__ = ("setup_processor","validate_command_configuration_values")

#// IMPORT
import re, shlex
from typing import Any

from sphinx.application import Sphinx
from sphinx.ext.autodoc._directive_options import _AutoDocumenterOptions as AutoDocOptions

from .error import InvalidConfigError
from .manager import CommandManager, TemplateManager


class LineAssembler:
    """
    Accumulates and formats lines produced by the DSL command processor.

    It acts as a small state machine that receives one "computed" line at a time
    (plus an optional temporary buffer of additional lines) and decides how the final output should be structured.
    """

    def __init__(self) -> None:
        # Temporary buffers
        self.tmp_line: str = ""
        self.tmp_buffer: list[str] = []

        # Private variables
        self.__buffer: list[str] = []
        self.__used_tmp_buffer: bool = False
        self.__current_indentation: str = ""

    def compute_tmp_buffers(self) -> None:
        """
        Finalize the current temporary line and temporary buffer.

        This method applies spacing rules that ensure:
            - multi-line command output is separated cleanly
            - unnecessary blank lines are removed
            - indentation is preserved for appended lines
            - transitions between single-line and multi-line output remain consistent

        After processing, the temporary buffers are cleared and ready for the next line.
        """
        valid_line: bool = self.tmp_line.strip() != ""
        first_line: bool = len(self.__buffer) == 0

        # [Case 1] The current command produced multiple lines
        if self.tmp_buffer:
            self.__used_tmp_buffer = True

            # If the current line is not empty
            if valid_line:
                self.tmp_buffer.insert(0, "")

            # If both the current line and the last output line are empty, avoid duplicates
            elif not first_line and self.__buffer[-1].strip() == "":
                self.__buffer.pop()

        # [Case 2] The previous command produced multiple lines, but this one did not
        elif self.__used_tmp_buffer:
            self.__used_tmp_buffer = False

            # Insert a blank line before the next visible line
            if valid_line:
                self.__buffer.append("")

        # The first computed line should not be empty
        if not (first_line and not valid_line):
            self.tmp_buffer.insert(0, self.tmp_line)

        # Append multi-line output with preserved indentation
        for tmp_line_buffer in self.tmp_buffer:
            self.__buffer.append(self.__current_indentation + tmp_line_buffer)

    def clear_tmp_buffers(self) -> None:
        """Reset the temporary line and temporary buffer."""
        self.tmp_line = ""
        self.tmp_buffer.clear()

    def new_line(self, string: str) -> None:
        """
        Load a new source state, extract its indentation, and store the de-indented content into ``tmp_line``.

        .. note::
            This method reset all temporary buffers.
            It is intended to be called once per input line before command scanning begins.

        :param string:
            The string from which indentation and content are extracted.
        """
        # Reset temporary state for the next iteration
        self.clear_tmp_buffers()

        # Extract the indentation
        pattern: str = r"^[ \t]*"
        self.__current_indentation = re.match(pattern, string).group(0)

        # Prepare the temporary state for the next iteration
        self.tmp_line = string[len(self.__current_indentation):]
        self.tmp_buffer.clear()

    @property
    def buffer(self) -> list[str]:
        """
        Return a copy of the assembled output buffer.

        :return: A shallow copy of the internal buffer containing all finalized lines.
        """
        return self.__buffer.copy()


def _escape_command(app: Sphinx, string: str, undo: bool = False) -> str:
    """
    Escape or unescape command delimiters inside a string.

    This helper replaces the command tags with internal placeholder characters (from the Unicode Private Use Area)
    so that unknown or unprocessed commands can be preserved safely during parsing.

    .. note::
        If ``undo`` is False (default) and the input string does not contain any command tags,
        the function automatically wraps the entire string with ``doclang_command_start`` and ``doclang_command_end``.
        This ensures that the string is treated as a command during parsing.

    :param app:     The active Sphinx application instance.
    :param string:  The input string to transform.
    :param undo:    If True, escape markers are replaced with command tags.

    :return: The transformed ``string`` with tags escaped or restored.
    """
    # Configuration values
    tag_start: str = app.config["doclang_command_start"]
    tag_end: str = app.config["doclang_command_end"]
    tag_map: dict[str, str] = {tag_start: "\uE000", tag_end: "\uE001"}

    # Add the tags are omitted, only if escaping (undo = false)
    # [original author, 6 months later]
    # This look's useless, in fact look's wrong... Maybe is some adaptation from earlier version when the project
    # was named DSL (Documentation Scripting Language) and nested commands was not supported yet?
    if not undo and tag_start not in string and tag_end not in string:
        string = f"{tag_start}{string}{tag_end}"

    # Escape/Unescape the tags
    for tag, escape in tag_map.items():
        if undo:
            string = string.replace(escape, tag)
        else:
            string = string.replace(tag, escape)

    return string


def _split_command(app: Sphinx, string: str) -> tuple[str, str, str]:
    """
    Split a string into three logical parts based on the next command occurrence.

    This helper locates the *innermost* command and returns a tuple containing:
        - The text before the command
        - The command content (without tags)
        - The text after the command

    If no valid command pair is found, all returned values are empty strings.

    :param app:     The active Sphinx application instance.
    :param string:  The input string to search for a command.

    :return: A tuple of strings ``(before, command, after)``.
    """
    # Configuration values
    tag_start: str = app.config["doclang_command_start"]
    tag_end: str = app.config["doclang_command_end"]

    # Find the next logical command
    index_end: int = string.find(tag_end)
    index_start: int = string.rfind(tag_start, 0, index_end)

    # If either tag is missing, no valid command exists
    if index_end == -1 or index_start == -1:
        return "", "", ""

    return (
        string[:index_start],                               # text before the command
        string[index_start + len(tag_start):index_end],     # command content (no tags)
        string[index_end + len(tag_end):]                   # text after the command
    )


def _compute_command(app: Sphinx, string: str) -> str | list[str] | None:
    """
    Parse and execute a DSL command string.

    The return value is normalized:
        - sequences (list, tuple, set) ➜ converted to a list of strings
        - any other value ➜ converted to a string

    :param app:     The active Sphinx application instance.
    :param string:  The raw command string, without surrounding delimiters.

    :return: The normalized command output, or ``None`` if the command is unknown.
    """
    # Extract command name and arguments
    cmd_sections: list[str] = string.split(app.config["doclang_command_splitter"], 1)
    cmd_name: str = cmd_sections[0].strip()
    cmd_args: list[str] = []
    cmd_kwargs: dict[str, str] = {}

    # If arguments are provided
    if len(cmd_sections) == 2:
        lexer = shlex.shlex(cmd_sections[1], posix=True, punctuation_chars=False)
        lexer.escape = app.config["doclang_escape_marker"]
        lexer.commenters = app.config["doclang_comment_marker"]
        lexer.whitespace = app.config["doclang_argument_separator"]
        lexer.whitespace_split = True

        for token in lexer:
            token = token.strip()

            # Collect only valid arguments
            if token:
                cmd_kwargs_separator: str = app.config["doclang_keyword_separator"]

                # Collect keyword arguments
                if cmd_kwargs_separator in token:
                    token_sections: list[str] = token.split(cmd_kwargs_separator, 1)
                    token_kw: str = token_sections[0].strip()

                    # If no value is provided for the keyword
                    if len(token_sections) == 1:
                        # Treat the keyword as a normal positional argument
                        cmd_args.append(token_kw)

                    else:
                        cmd_kwargs[token_kw] = token_sections[1].strip()

                # Collect positional arguments
                else:
                    cmd_args.append(token)

    # Known command
    if CommandManager._is_registered(cmd_name):
        cmd_return: Any = CommandManager._execute(cmd_name, *cmd_args, **cmd_kwargs)

        # Normalize the output inside the list
        if isinstance(cmd_return, (list, tuple, set)):
            lines: list[str] = []

            for value in cmd_return:
                if isinstance(value, str):
                    lines.extend(value.split("\n"))     # split("\n") ➜ keeping the empty strings inside the list
                else:
                    lines.append(str(value))

            return lines

        # Check for multi-lines intention
        elif isinstance(cmd_return, str):
            check_return: list[str] = cmd_return.splitlines()   # splitlines ➜ removing the empty strings

            if len(check_return) == 1:
                return cmd_return
            else:
                return check_return

        # Otherwise, normalize the value
        else:
            return str(cmd_return)

    # Unknown command
    return None


def _compute_lines(app: Sphinx, original_lines: list[str]) -> None:
    """
    Transform a list of lines by resolving inline DSL commands.

    This function processes each line while preserving indentation and the original line order.

    The transformation is performed in-place:
        - ``original_lines`` is cleared and replaced with the computed result.

    :param app:
        The active Sphinx application instance.

    :param original_lines:
        The list of raw input lines extracted from a docstring.
        Each line may contain zero or more DSL command sections.

    :return: Nothing. The ``original_lines`` is modified directly.
    """
    # Configuration values
    keep_unknown: bool = app.config["doclang_keep_unknown"]

    # Local variables
    assembler: LineAssembler = LineAssembler()
    rendered_lines: list[str] = TemplateManager._render_template().splitlines()

    # If template can not be solved, fallback to the original lines
    if not rendered_lines:
        rendered_lines = original_lines

    # Iterate through each line
    for r_line in rendered_lines:
        assembler.new_line(r_line)

        while True:
            # Find the next logical command
            line_start, line_command, line_end = _split_command(app, assembler.tmp_line)

            # If no command was found, stop searching
            if line_command == "":
                break

            # Compute the command
            cmd_return: str | list[str] | None = _compute_command(app, line_command)

            # [Case 1] The command could not be solved
            if cmd_return is None:
                # [Case 1.1] Preserve unknown command by escaping delimiters
                if keep_unknown:
                    escaped_command: str = _escape_command(app, line_command)
                    assembler.tmp_line = f"{line_start}{escaped_command}{line_end}"

                # [Case 1.2] Remove unknown command entirely
                else:
                    assembler.tmp_line = f"{line_start.rstrip()} {line_end.lstrip()}"

            # [Case 2] The command returns a single string ➜ inline replacement
            elif isinstance(cmd_return, str):
                assembler.tmp_line = f"{line_start}{cmd_return}{line_end}"

            # [Case 3] The command returns multiple lines ➜ buffer them
            else:
                # Erase to block command
                assembler.tmp_line = f"{line_start.rstrip()} {line_end.lstrip()}"
                # Cache the lines
                assembler.tmp_buffer = cmd_return

        # Restore escaped delimiters back to real tags
        if keep_unknown:
            assembler.tmp_line = _escape_command(app, assembler.tmp_line, True)

        # Handle temporary buffers output and spacing rules
        assembler.compute_tmp_buffers()

    # Replace original lines with the computed result
    original_lines.clear()
    original_lines.extend(assembler.buffer)


def validate_command_configuration_values(app: Sphinx) -> None:
    """
    This function retrieves the values used by commands from the Sphinx configuration
    and performs a series of safety checks to ensure they are usable.

    Raises **InvalidConfigError** if any required configuration value:
        - is empty
        - contains whitespace characters
        - character already defined in another configuration value

    :param app: The active Sphinx application instance.

    :return: Nothing.
    """
    # Configuration values
    command_tags: list[str] = [
        "doclang_command_start", "doclang_command_end", "doclang_command_splitter",
        "doclang_argument_separator", "doclang_keyword_separator",
        "doclang_escape_marker", "doclang_comment_marker"
    ]

    # Characters in configuration values ➜ { character: config_value }
    seen: dict[str, str] = {}

    # Check every tag value
    for tag_name in command_tags:
        value: str = app.config[tag_name]

        # [Case 1] The tag value is empty
        if value == "":
            raise InvalidConfigError(f"{tag_name!r} cannot be empty.")

        # [Case 2] The character value is a whitespace or is duplicated
        for char in value:
            # Whitespace
            if char.isspace():
                raise InvalidConfigError(f"{tag_name!r} cannot contain whitespace characters.")

            # Duplicate
            if char in seen:
                other: str = seen[char]
                if tag_name != other:
                    error: InvalidConfigError = InvalidConfigError(
                        f"The character {char!r} in {tag_name!r} is already used in {other!r}."
                    )
                    error.note(
                        "Suggestion",
                        "Use distinct characters across all command tags, separators and markers."
                    )
                    raise error
            else:
                seen[char] = tag_name


#// LOGIC
def _process_docstring(app: Sphinx,
                       obj_type: str, obj_name: str, obj: object,
                       _options: AutoDocOptions, lines: list[str]
                       ) -> None:

    TemplateManager.set_multiple_items(
        name = obj_name,
        type = obj_type,
        obj = str(obj),
        doc = "\n".join(lines).strip()
    )

    _compute_lines(app, lines)

    if obj_name == "sphinx_doclang.debug.Debug":
        print("[_options]\n", _options, end="\n\n")
        print("[DEBUG lines]")
        line_number: int = 0
        line_number_template: str = "%{0}.{0}s |".format(len(str(len(lines))))
        for line in lines:
            line_number += 1
            print(line_number_template % line_number, line)


def setup_processor(app: Sphinx) -> None:
    app.add_config_value(
        name="doclang_command_start",
        default="§",
        rebuild="env",
        types=str
    )
    app.add_config_value(
        name="doclang_command_end",
        default="¶",
        rebuild="env",
        types=str
    )
    app.add_config_value(
        name="doclang_command_splitter",
        default=":",
        rebuild="env",
        types=str
    )
    app.add_config_value(
        name="doclang_argument_separator",
        default=",;",
        rebuild="env",
        types=str
    )
    app.add_config_value(
        name="doclang_keyword_separator",
        default="=",
        rebuild="env",
        types=str
    )
    app.add_config_value(
        name="doclang_comment_marker",
        default="#",
        rebuild="env",
        types=str
    )
    app.add_config_value(
        name="doclang_escape_marker",
        default="/|",
        rebuild="env",
        types=str
    )
    app.add_config_value(
        name="doclang_keep_unknown",
        default=False,
        rebuild="env",
        types=bool
    )

    app.connect("autodoc-process-docstring", _process_docstring)
