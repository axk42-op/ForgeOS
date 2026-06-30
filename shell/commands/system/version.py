"""Display Forge OS version."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class VersionCommand(BaseCommand):
    name = "version"
    category = "system"
    description = "Display Forge OS version"
    syntax = "version"
    examples = ("version",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        kernel = context["kernel"]
        session = context["session"]
        version = session.environment.get("FORGE_VERSION", kernel.version)
        return CommandResult(output=f"Forge OS v{version}")
