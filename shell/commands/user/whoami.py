"""Display current user."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class WhoamiCommand(BaseCommand):
    name = "whoami"
    category = "user"
    description = "Display current user"
    syntax = "whoami"
    examples = ("whoami",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        users = context["users"]
        return CommandResult(output=users.whoami())
