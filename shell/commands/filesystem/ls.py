"""List directory contents."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class LsCommand(BaseCommand):
    name = "ls"
    category = "filesystem"
    description = "List directory contents"
    syntax = "ls [PATH]"
    examples = (
        "ls",
        "ls /home",
    )

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        vfs = context["filesystem"]
        session = context["session"]
        path = "."
        for arg in args:
            if not arg.startswith("-"):
                path = arg
                break

        try:
            entries = vfs.list_dir(path, cwd=session.cwd)
        except Exception as error:
            raise CommandExecutionError(str(error)) from error

        if not entries:
            return CommandResult()

        lines = []
        for entry in entries:
            suffix = "/" if entry.is_dir else ""
            style = "[bold blue]" if entry.is_dir else ""
            end_style = "[/bold blue]" if entry.is_dir else ""
            lines.append(f"{style}{entry.name}{suffix}{end_style}")

        return CommandResult(output="\n".join(lines))
