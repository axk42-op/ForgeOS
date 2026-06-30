"""Display software license."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.errors import CommandExecutionError


class LicenseCommand(BaseCommand):
    name = "license"
    category = "system"
    description = "Display software license"
    syntax = "license"
    examples = ("license",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        vfs = context["filesystem"]
        session = context["session"]

        try:
            content = vfs.read_file("/etc/LICENSE", cwd=session.cwd)
            return CommandResult(output=content)
        except Exception as error:
            raise CommandExecutionError(str(error)) from error
