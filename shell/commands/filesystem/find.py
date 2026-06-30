"""Search for files."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class FindCommand(BaseCommand):
    name = "find"
    category = "filesystem"
    description = "Search for files"
    syntax = "find [PATH] [PATTERN]"
    examples = (
        "find . *",
        "find /home forge",
    )

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        vfs = context["filesystem"]
        session = context["session"]
        path = "."
        pattern = "*"

        if len(args) == 1:
            pattern = args[0]
        elif len(args) >= 2:
            path = args[0]
            pattern = args[1]

        try:
            matches = vfs.find(pattern, path=path, cwd=session.cwd)
        except Exception as error:
            raise CommandExecutionError(str(error)) from error

        if not matches:
            return CommandResult()
        return CommandResult(output="\n".join(matches))
