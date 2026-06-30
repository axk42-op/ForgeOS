"""Shut down Forge OS."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class ShutdownCommand(BaseCommand):
    name = "shutdown"
    category = "system"
    description = "Shut down Forge OS"
    syntax = "shutdown"
    examples = ("shutdown",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        return CommandResult(
            output="Forge OS is shutting down... Goodbye.",
            should_exit=True,
        )
