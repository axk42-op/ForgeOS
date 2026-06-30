"""Display environment variables."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class EnvCommand(BaseCommand):
    name = "env"
    category = "user"
    description = "Display environment variables"
    syntax = "env"
    examples = ("env",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        session = context["session"]
        lines = [f"{key}={value}" for key, value in session.environment.items()]
        return CommandResult(output="\n".join(lines))
