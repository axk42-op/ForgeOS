"""Change directory."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class CdCommand(BaseCommand):
    name = "cd"
    category = "filesystem"
    description = "Change directory"
    syntax = "cd [PATH]"
    examples = (
        "cd /home",
        "cd ..",
    )

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        vfs = context["filesystem"]
        session = context["session"]
        target = args[0] if args else session.environment.get("HOME", "/")

        try:
            resolved = vfs.resolve(target, cwd=session.cwd)
            if not vfs.exists(resolved):
                raise CommandExecutionError(f"cd: no such file or directory: {target}")
            if not vfs.is_dir(resolved):
                raise CommandExecutionError(f"cd: not a directory: {target}")
            session.set_cwd(resolved)
        except CommandExecutionError:
            raise
        except Exception as error:
            raise CommandExecutionError(str(error)) from error

        return CommandResult()
