"""Create directories."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class MkdirCommand(BaseCommand):
    name = "mkdir"
    category = "filesystem"
    description = "Create directories"
    syntax = "mkdir [-p] DIRECTORY..."
    examples = (
        "mkdir test",
        "mkdir -p a/b",
    )

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if not args:
            return CommandResult(output="mkdir: missing operand", exit_code=1)

        vfs = context["filesystem"]
        session = context["session"]
        parents = False
        paths = args

        if args[0] in ("-p", "--parents"):
            parents = True
            paths = args[1:]
            if not paths:
                return CommandResult(output="mkdir: missing operand", exit_code=1)

        created = []
        for path in paths:
            try:
                created.append(vfs.mkdir(path, cwd=session.cwd, parents=parents))
            except Exception as error:
                raise CommandExecutionError(str(error)) from error

        return CommandResult(output="\n".join(created) if len(created) > 1 else None)
