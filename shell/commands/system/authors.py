"""Display project authors."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class AuthorsCommand(BaseCommand):
    name = "authors"
    category = "system"
    description = "Display project authors"
    syntax = "authors"
    examples = ("authors",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        return CommandResult(output="Forge OS Project Contributors")
