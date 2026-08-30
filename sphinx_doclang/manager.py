#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 15 Feb 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
__all__ = ("CommandManager","TemplateManager")

#// IMPORT
from inspect import Parameter
from inspect import signature as get_signature
from pathlib import Path
from typing import Any, Callable, get_type_hints, get_origin, get_args

from sphinx.application import Sphinx

from .error import InvalidCommandError


#// LOGIC
class BaseCommandManager:
    """ Manager responsible for registering, validating, and executing doc-string commands. """

    def __init__(self) -> None:
        # Private variables
        self.__registry: dict[str, Callable] = {}

        # Variables
        self.validate_command: bool = True

    def new(self, name: str) -> Callable:
        """
        Decorator used to register a new DSL command.

        This method is normalizing ``name`` to lowercase.

        :param name: The name under which the command will be registered.
        :return: The original function, after registration.

        :raises InvalidCommandError:
            If a command with the same name already exists.
        """
        return self._make_decorator(name, must_exist=False)

    def overwrite(self, name: str) -> Callable:
        """
        Decorator used to replace an existing DSL command.

        This method is normalizing ``name`` to lowercase.

        :param name: The name of the command to overwrite.
        :return: The original function, after replacement.

        :raises InvalidCommandError:
            If the command does not already exist.
        """
        return self._make_decorator(name, must_exist=True)

    def _is_registered(self, name: str) -> bool:
        """
        Check whether a command with the given name is registered.

        :param name: The command name to check.

        :return: ``True`` if the command exists, otherwise ``False``.
        """
        return name.lower() in self.__registry

    def _execute(self, name: str, *args, **kwargs) -> Any:
        """
        Execute a registered command by name.

        :param name:    The name of the command to execute.
        :param args:    Positional arguments passed to the command.
        :param kwargs:  Keyword arguments passed to the command.

        :return: The result returned by the command function.

        :raises KeyError:
            If the command name is not registered.
            Use ``_is_registered()`` to check for existence before calling this method.
        """
        return self.__registry[name.lower()](*args, **kwargs)

    def _make_decorator(self, name: str, must_exist: bool) -> Callable:
        """
        Internal helper that builds decorator's.

        This method is normalizing ``name`` to lowercase.

        :param name: The command name to register or overwrite. The name is normalized to lowercase.
        :param must_exist: If True, the command must already be present in the registry.

        :return: A decorator that registers the provided function under the given command name.

        :raises InvalidCommandError:
            If the existence condition is violated or if the subclass hook raises an error.
        """
        def decorator(func: Callable) -> Callable:
            # Local variables
            key: str = name.lower()
            error: InvalidCommandError = InvalidCommandError(
                "Cannot {trying} command {command_name!r} because {reason}.".format(
                    command_name=key,
                    trying="overwrite" if must_exist else "register",
                    reason="it does not exist" if must_exist else "is already registered"
                )
            )

            # Existence checks
            if must_exist and key not in self.__registry:
                error.note(
                    "Suggestion",
                    "Make shore the command name is correct or register a new command under this name."
                )
                raise error

            if not must_exist and key in self.__registry:
                error.note(
                    "Suggestion",
                    "Use a different name or overwrite the existing command if it does not satisfy your needs."
                )
                raise error

            # Validate the command before registration
            if self.validate_command:
                self._validate_command(key, func)

            # Register the command
            self.__registry[key] = func
            return func

        return decorator

    @staticmethod
    def _validate_command(name: str, func: Callable) -> None:
        """
        Validate that a command function can safely receive arguments from the DSL processor.

        A valid command must accept both:
        - ``*args``  (var‑positional arguments)
        - ``**kwargs`` (var‑keyword arguments)

        This ensures that the DSL can pass any combination of positional and keyword arguments
        without causing runtime errors.

        :param name: The command name being validated.
        :param func: The function associated with the command.

        :raises InvalidCommandError:
            If the function does not accept ``*args`` or ``**kwargs``.
        """
        # Local variables
        missing_args: str = ""
        suggested_args: list[list[str]] = [["*args"], ["**kwargs"]]

        # Validate the required arguments
        params: list[Parameter] = list(get_signature(func).parameters.values())
        accepts_args: bool = any(p.kind == Parameter.VAR_POSITIONAL for p in params)
        accepts_kwargs: bool = any(p.kind == Parameter.VAR_KEYWORD for p in params)

        # If var‑positional arguments is missing
        if not accepts_args:
            missing_args = missing_args[0][0]

        # If var‑keyword arguments is missing
        if not accepts_kwargs:
            missing_args = f"{missing_args}{"' and '" if missing_args else ""}{suggested_args[1][0]}"

        # If arguments are missing, generate a helpful error message
        if missing_args:
            # Build a corrected signature suggestion
            for p in params:
                # If one of required arguments is provided, replace the suggested name with the existing one
                if p.kind == Parameter.VAR_POSITIONAL:
                    suggested_args[0][0] = f"*{p.name}"

                elif p.kind == Parameter.VAR_KEYWORD:
                    suggested_args[1][0] = f"**{p.name}"

                # Group the existing arguments
                elif p.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD):
                    # If a default value is provided, collect it as keyword argument along with the default value
                    if p.default is not Parameter.empty:
                        suggested_args[1].append("=".join([p.name, str(p.default)]))

                    # Otherwise, collect it as positional argument
                    else:
                        suggested_args[0].append(p.name)

            # Move *args / **kwargs to the end of each group
            for group in suggested_args:
                first: str = group.pop(0)
                group.append(first)

            # Raise the error with a suggestion ready for copy‑paste
            error: InvalidCommandError = InvalidCommandError(
                f"Command {name!r} must accept {missing_args!r} to handle all provided arguments."
            )
            error.note(
                "Suggestion",
                [
                    f"Update the function signature for command {name!r} to:",
                    f"def {func.__name__}({', '.join([arg for group in suggested_args for arg in group])}): ..."
                ],
                4
            )
            raise error

        # [Case 1] The annotation exists
        hints: dict[str, Any] = get_type_hints(func)
        msg_err_return: str = f"Command {name!r} must return a string or a list of strings only."
        error_return: InvalidCommandError = InvalidCommandError(f"{msg_err_return}")
        need_simulation: bool = False

        if "return" in hints:
            return_type = hints["return"]
            return_origin = get_origin(return_type)
            return_args = get_args(return_type)

            # Accept ➜ str
            if (return_type is str) or (return_origin is str): return

            # Accept ➜ list[str]
            if (return_type is list) or (return_origin is list):
                # List with no type args ➜ simulate
                if not return_args:
                    need_simulation = True

                # Accept only list with all type args as str
                elif all(arg_type is str for arg_type in return_args): return

                # Raise an error if list have other type args then accepted one
                else:
                    error_return.note("Found", f"Annotation {return_type}", 4)
                    raise error_return

            # Anything else ➜ Raise an error
            else:
                error_return.note("Found", f"Annotation {return_type}", 4)
                raise error_return

        if not need_simulation: return

        # [Case 2] No annotation OR annotation incomplete
        simulate: Any = func(*[f"debug arg {index}" for index in range(100)])
        simulate_type = type(simulate)

        if simulate_type is str: return
        elif simulate_type is list and all(isinstance(arg, str) for arg in simulate_type): return

        else:
            error_return.note("Simulated", f"Annotation {simulate_type}", 4)
            raise error_return


class BaseTemplateManager:
    """ Manager responsible for locating, loading and rendering template files. """

    def __init__(self) -> None:
        super().__init__()

        # Private variables
        self.__template_paths: list[Path] = []
        self.__map: dict[str, str] = {}

    @property
    def names(self) -> list[str]:
        """ A list-like string providing a view on the mapped names. """
        return [name for name in self.__map.keys()]

    @property
    def values(self) -> list[str]:
        """ A list-like string providing a view on the mapped values. """
        return [value for value in self.__map.values()]

    @property
    def items(self) -> list[tuple[str, str]]:
        """ A list-like tuple providing a view on the mapped names and values. """
        return [(name, value) for name, value in self.__map.items()]

    def set_multiple_items(self, **kwargs: str) -> None:
        """
        Set multiple mapping items at once.

        Equivalent to calling ``self[name] = value`` for each provided keyword.
        """
        for key, value in kwargs.items():
            self[key] = value

    def __contains__(self, name: str) -> bool:
        """ Return True if the ``name`` is mapped, otherwise False. """
        return name.upper() in self.__map

    def __delitem__(self, name: str) -> None:
        """ Delete the mapped entry for the given name. """
        key: str = name.upper()

        if key in self.__map:
            del self.__map[key]

    def __getitem__(self, name: str) -> str:
        """
        Retrieve the value associated with the given name.

        Returns an empty string if the key is not present.
        """
        return self.__map.get(name.upper(), "")

    def __setitem__(self, name: str, value: str) -> None:
        """ Mapping the given name to the provided value. """
        self.__map[name.upper()] = value.strip()

    def _clear_map(self) -> None:
        """ Clear the map. """
        self.__map.clear()

    def _init_app(self, app: Sphinx) -> None:
        """
        Initialize template search paths based on the active Sphinx application.

        This method scans all directories listed in ``templates_path`` and collects those that contain a
        ``doclang`` subdirectory. Only these directories are considered valid template roots.

        :param app: The active Sphinx application instance.
        """
        self.__template_paths.clear()

        for path in app.config["templates_path"]:
            directory: Path = Path(app.confdir) / path / "doclang"

            if directory.exists():
                self.__template_paths.append(directory)

    def _get_file_content(self, *file_path: str, extension: str = "dlt") -> str:
        """
        Retrieve the raw text content of a template by name.

        The method searches all registered template directories for a file named ``<name>.dlt``.
        If found, the file is read and returned as a UTF‑8 string.

        :param file_path: The file path without extension.
        :param extension: The file extension.

        :return: The file content, or an empty string if the file does not exist.
        """
        if not file_path:
            return ""

        file_dir: list[str] = [*file_path]
        file_name: str = f"{file_dir.pop()}.{extension}"

        for root in self.__template_paths:
            file: Path = Path(root, *file_dir, file_name)

            if file.is_file():
                return file.read_text(encoding="UTF-8")

        return ""

    def _render_content(self, content: str) -> str:
        """
        Render a template content by performing simple variable substitution.

        This method replaces all occurrences of ``{{ NAME }}`` with the corresponding stored mapped values.

        :param content: The template content to render.

        :return: The rendered content, or an empty string if the template could not be found.
        """
        for name, value in self.items:
            content = content.replace(f"{{{{ {name} }}}}", value)

        return content

    def _render_template(self) -> str:
        """
        Render the current template by performing simple variable substitution.

        This method loads the template content using ``_get_file_content`` and render it using ``_render_content``.

        :return: The rendered template content, or an empty string if the template could not be found.
        """
        obj_name: str = self["name"].rsplit(".", 1).pop()
        template: str = TemplateManager._get_file_content(self["type"], obj_name)

        # If the template content is empty try the fallback name
        if template == "":
            template = TemplateManager._get_file_content(self["type"])

        return self._render_content(template)


#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Global instances
#//|>-----------------------------------------------------------------------------------------------------------------<|
#: Main command manager
CommandManager: BaseCommandManager = BaseCommandManager()

#: Main template manager
TemplateManager: BaseTemplateManager = BaseTemplateManager()
