"""Display system uptime."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class UptimeCommand(BaseCommand):
    name = "uptime"
    category = "user"
    description = "Display system uptime"
    syntax = "uptime"
    examples = ("uptime",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        kernel = context["kernel"]
        users = context["users"]
        return CommandResult(
            output=f"up {kernel.uptime()}, 1 user, load average: 0.00, 0.00, 0.00 "
            f"({users.hostname})"
        )
