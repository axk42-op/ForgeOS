"""Print working directory."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class PwdCommand(BaseCommand):
    name = "pwd"
    category = "filesystem"
    description = "Print working directory"
    syntax = "pwd"
    examples = ("pwd",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        session = context["session"]
        return CommandResult(output=session.cwd)
