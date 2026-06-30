"""Display system information."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class UnameCommand(BaseCommand):
    name = "uname"
    category = "system"
    description = "Display system information"
    syntax = "uname [-a]"
    examples = ("uname", "uname -a")

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        kernel = context["kernel"]
        session = context["session"]
        users = context["users"]

        if "-a" in args or "--all" in args:
            return CommandResult(
                output=(
                    f"ForgeOS {kernel.version} "
                    f"{users.hostname} "
                    f"{kernel.name} "
                    f"{session.environment.get('FORGE_VERSION', kernel.version)} "
                    f"x86_64 Forge/Virtual"
                )
            )

        return CommandResult(output="ForgeOS")
