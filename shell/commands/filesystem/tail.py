"""Display last lines of a file."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class TailCommand(BaseCommand):
    name = "tail"
    category = "filesystem"
    description = "Display last lines of a file"
    syntax = "tail [-n NUM] FILE"
    examples = ("tail file.txt", "tail -n 5 file.txt")

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if not args:
            return CommandResult(output="tail: missing file operand", exit_code=1)

        lines = 10
        paths = args
        if args[0] == "-n" and len(args) >= 3:
            lines = int(args[1])
            paths = args[2:]
        elif args[0].startswith("-n") and len(args) >= 2:
            lines = int(args[0][2:])
            paths = args[1:]

        vfs = context["filesystem"]
        session = context["session"]
        output_lines: list[str] = []

        for path in paths:
            try:
                content = vfs.read_file(path, cwd=session.cwd)
            except Exception as error:
                raise CommandExecutionError(str(error)) from error
            output_lines.extend(content.splitlines()[-lines:])

        return CommandResult(output="\n".join(output_lines))
