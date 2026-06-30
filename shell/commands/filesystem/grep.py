"""Search file contents."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class GrepCommand(BaseCommand):
    name = "grep"
    category = "filesystem"
    description = "Search for patterns in files"
    syntax = "grep PATTERN FILE..."
    examples = ("grep forge /etc/forge-release",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if len(args) < 2:
            return CommandResult(output="grep: usage: grep PATTERN FILE...", exit_code=1)

        pattern = args[0]
        vfs = context["filesystem"]
        session = context["session"]
        matches: list[str] = []

        for path in args[1:]:
            try:
                content = vfs.read_file(path, cwd=session.cwd)
            except Exception as error:
                raise CommandExecutionError(str(error)) from error

            for line_no, line in enumerate(content.splitlines(), start=1):
                if pattern in line:
                    matches.append(f"{path}:{line_no}:{line}")

        return CommandResult(output="\n".join(matches) if matches else None)
