"""Display file contents."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class CatCommand(BaseCommand):
    name = "cat"
    category = "filesystem"
    description = "Display file contents"
    syntax = "cat FILE..."
    examples = ("cat file.txt",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        stdin = context.get("stdin", "")
        if not args:
            if stdin:
                return CommandResult(output=stdin)
            return CommandResult(output="cat: missing file operand", exit_code=1)

        vfs = context["filesystem"]
        session = context["session"]
        parts: list[str] = []

        for path in args:
            try:
                parts.append(vfs.read_file(path, cwd=session.cwd))
            except Exception as error:
                raise CommandExecutionError(str(error)) from error

        return CommandResult(output="\n".join(parts))
