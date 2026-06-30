"""Display system hostname."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class HostnameCommand(BaseCommand):
    name = "hostname"
    category = "user"
    description = "Display system hostname"
    syntax = "hostname"
    examples = ("hostname",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        users = context["users"]
        return CommandResult(output=users.hostname)
