"""Clear the terminal screen."""

from typing import Any, ClassVar

from shell.commands.base import BaseCommand, CommandResult


class ClearCommand(BaseCommand):
    name = "clear"
    category = "system"
    aliases: ClassVar[tuple[str, ...]] = ()
    description = "Clear the terminal screen"
    syntax = "clear"
    examples = ("clear",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        return CommandResult(clear_screen=True)
