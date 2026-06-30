"""Copy files."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class CpCommand(BaseCommand):
    name = "cp"
    category = "filesystem"
    description = "Copy files"
    syntax = "cp SOURCE DEST"
    examples = ("cp a.txt b.txt",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if len(args) != 2:
            return CommandResult(output="cp: usage: cp SOURCE DEST", exit_code=1)

        vfs = context["filesystem"]
        session = context["session"]

        try:
            source, dest = vfs.copy(args[0], args[1], cwd=session.cwd)
            return CommandResult(output=f"copied {source} -> {dest}")
        except Exception as error:
            raise CommandExecutionError(str(error)) from error
