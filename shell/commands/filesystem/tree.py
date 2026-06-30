"""Display directory tree."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class TreeCommand(BaseCommand):
    name = "tree"
    category = "filesystem"
    description = "Display directory tree"
    syntax = "tree [PATH]"
    examples = (
        "tree",
        "tree /home",
    )

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        vfs = context["filesystem"]
        session = context["session"]
        path = args[0] if args else "."

        try:
            lines = vfs.tree(path, cwd=session.cwd)
        except Exception as error:
            raise CommandExecutionError(str(error)) from error

        return CommandResult(output="\n".join(lines))
