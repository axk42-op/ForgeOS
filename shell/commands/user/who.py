"""Display logged-in users."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class WhoCommand(BaseCommand):
    name = "who"
    category = "user"
    description = "Display logged-in users"
    syntax = "who"
    examples = ("who",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        users = context["users"]
        session = context["session"]
        return CommandResult(
            output=f"{users.whoami()} {users.hostname} {session.cwd} {session.environment.get('SHELL', '/bin/forge')}"
        )
