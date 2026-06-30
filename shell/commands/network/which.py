"""Locate a command."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class WhichCommand(BaseCommand):
    name = "which"
    category = "network"
    description = "Locate a command"
    syntax = "which COMMAND"
    examples = ("which ls",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if not args:
            return CommandResult(output="which: missing command name", exit_code=1)

        registry = context["registry"]
        name = args[0]
        if registry.has(name):
            return CommandResult(output=f"/usr/bin/{name}")
        return CommandResult(output=f"which: no {name} in PATH", exit_code=1)
