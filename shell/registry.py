"""Command registry with automatic discovery."""

import importlib
import inspect
import pkgutil
from collections.abc import Iterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shell.commands.base import BaseCommand


class CommandRegistry:
    """Central registry for shell commands."""

    def __init__(self) -> None:
        self._commands: dict[str, type["BaseCommand"]] = {}
        self._aliases: dict[str, str] = {}

    def register(self, command_class: type["BaseCommand"]) -> type["BaseCommand"]:
        self._commands[command_class.name] = command_class
        for alias in command_class.aliases:
            self._aliases[alias] = command_class.name
        return command_class

    def get(self, name: str) -> type["BaseCommand"] | None:
        resolved = self._aliases.get(name, name)
        return self._commands.get(resolved)

    def has(self, name: str) -> bool:
        return self.get(name) is not None

    def names(self) -> list[str]:
        return sorted(self._commands.keys())

    def by_category(self) -> dict[str, list[type["BaseCommand"]]]:
        grouped: dict[str, list[type["BaseCommand"]]] = {}
        for command_class in self._commands.values():
            grouped.setdefault(command_class.category, []).append(command_class)
        for commands in grouped.values():
            commands.sort(key=lambda cls: cls.name)
        return grouped

    def all_commands(self) -> Iterator[type["BaseCommand"]]:
        return iter(self._commands.values())

    def discover(self) -> None:
        """Import all command modules and register BaseCommand subclasses."""
        import shell.commands as commands_package

        for module_info in pkgutil.walk_packages(
            commands_package.__path__,
            prefix=f"{commands_package.__name__}.",
        ):
            if module_info.name.endswith(".base"):
                continue
            module = importlib.import_module(module_info.name)
            for _, obj in inspect.getmembers(module, inspect.isclass):
                from shell.commands.base import BaseCommand

                if (
                    issubclass(obj, BaseCommand)
                    and obj is not BaseCommand
                    and getattr(obj, "name", "")
                ):
                    self.register(obj)
