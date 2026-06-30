"""Remove files or directories."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class RmCommand(BaseCommand):
    name = "rm"
    category = "filesystem"
    description = "Remove files or directories"
    syntax = "rm [-r] PATH..."
    examples = (
        "rm file.txt",
        "rm -r dir",
    )

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if not args:
            return CommandResult(output="rm: missing operand", exit_code=1)

        vfs = context["filesystem"]
        session = context["session"]
        recursive = False
        paths = args

        if args[0] in ("-r", "-R", "--recursive"):
            recursive = True
            paths = args[1:]
            if not paths:
                return CommandResult(output="rm: missing operand", exit_code=1)

        removed = []
        for path in paths:
            try:
                removed.append(vfs.remove(path, cwd=session.cwd, recursive=recursive))
            except Exception as error:
                raise CommandExecutionError(str(error)) from error

        return CommandResult(output="\n".join(f"removed {item}" for item in removed) if removed else None)
