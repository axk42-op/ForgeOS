"""Create empty files."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class TouchCommand(BaseCommand):
    name = "touch"
    category = "filesystem"
    description = "Create empty files"
    syntax = "touch FILE..."
    examples = ("touch file.txt",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if not args:
            return CommandResult(output="touch: missing file operand", exit_code=1)

        vfs = context["filesystem"]
        session = context["session"]

        for path in args:
            try:
                vfs.touch(path, cwd=session.cwd)
            except Exception as error:
                raise CommandExecutionError(str(error)) from error

        return CommandResult()
