"""Move or rename files."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class MvCommand(BaseCommand):
    name = "mv"
    category = "filesystem"
    description = "Move or rename files"
    syntax = "mv SOURCE DEST"
    examples = ("mv old.txt new.txt",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if len(args) != 2:
            return CommandResult(output="mv: usage: mv SOURCE DEST", exit_code=1)

        vfs = context["filesystem"]
        session = context["session"]

        try:
            source, dest = vfs.move(args[0], args[1], cwd=session.cwd)
            return CommandResult(output=f"moved {source} -> {dest}")
        except Exception as error:
            raise CommandExecutionError(str(error)) from error
