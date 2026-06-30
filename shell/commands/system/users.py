"""List logged-in users."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class UsersCommand(BaseCommand):
    name = "users"
    category = "system"
    description = "List active Forge OS users"
    syntax = "users"
    examples = ("users",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        users = context["users"]
        info = users.info()
        return CommandResult(output=f"{info['username']} {info['hostname']} forge shell")
