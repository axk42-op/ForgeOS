"""Sort lines of text."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class SortCommand(BaseCommand):
    name = "sort"
    category = "filesystem"
    description = "Sort lines of text"
    syntax = "sort [FILE]"
    examples = ("sort file.txt",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        vfs = context["filesystem"]
        session = context["session"]
        stdin = context.get("stdin", "")

        if args:
            try:
                content = vfs.read_file(args[0], cwd=session.cwd)
            except Exception as error:
                raise CommandExecutionError(str(error)) from error
        else:
            content = stdin

        lines = content.splitlines()
        return CommandResult(output="\n".join(sorted(lines)))
