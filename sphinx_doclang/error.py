#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 18 Feb 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
__all__ = ("DocLangError","InvalidCommandError","InvalidConfigError")


#// LOGIC
class DocLangError(Exception):
    """Base exception for all DocLang‑related errors."""

    def __init__(self, message: str, *args) -> None:
        super().__init__(f"[DocLang Error] {message}", *args)

    def note(self, title: str, message: str|list[str], indent: int = 0) -> None:
        """
        Attach a formatted note to the current error.

        Notes provide additional context, suggestions or multi‑line guidance
        that appears alongside the main error message in Sphinx output.

        :param title:   A short label describing the purpose of the note.
        :param message: Either a single string or a list of strings.
        :param indent:  Number of spaces to indent multi‑line messages.

        :return: Nothing.
        """
        # Local variables
        formatted: str = ""

        # Single-line message
        if isinstance(message, str):
            formatted = message

        else:
            # One-line list ➜ treat as a normal string
            if len(message) == 1:
                formatted = message[0]

            # Multi-line list ➜ format with indentation
            else:
                prefix: str = f"\n\t{' ' * (len(title) + 3 + indent)}"

                for message_index in range(len(message)):
                    formatted = f"{formatted}{prefix if message_index else ''}{message[message_index]}"

        # Only add the note if the message contains meaningful content
        if formatted.strip():
            self.add_note(f"\t[{title}] {formatted}")


class InvalidCommandError(DocLangError):
    """Raised when a DSL command is invalid or cannot be registered."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidConfigError(DocLangError):
    """Raised when attempting to use a configuration value with an invalid signature."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
