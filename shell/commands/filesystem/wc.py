"""Word, line, and character counts."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class WcCommand(BaseCommand):
    name = "wc"
    category = "filesystem"
    description = "Print newline, word, and byte counts"
    syntax = "wc [FILE...]"
    examples = ("wc file.txt",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        vfs = context["filesystem"]
        session = context["session"]
        stdin = context.get("stdin", "")

        if not args:
            if not stdin:
                return CommandResult(output="0 0 0", exit_code=0)
            content = stdin
            lines = len(content.splitlines()) if content else 0
            words = len(content.split())
            chars = len(content)
            return CommandResult(output=f"{lines} {words} {chars}")

        rows: list[str] = []
        for path in args:
            try:
                content = vfs.read_file(path, cwd=session.cwd)
            except Exception as error:
                raise CommandExecutionError(str(error)) from error
            lines = len(content.splitlines()) if content else 0
            words = len(content.split())
            chars = len(content)
            rows.append(f"{lines} {words} {chars} {path}")

        return CommandResult(output="\n".join(rows))
