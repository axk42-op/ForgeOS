"""Display project credits."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class CreditsCommand(BaseCommand):
    name = "credits"
    category = "system"
    description = "Display project credits"
    syntax = "credits"
    examples = ("credits",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        lines = [
            "Forge OS Credits",
            "",
            "Built with Python, Rich, prompt_toolkit, and colorama.",
            "Inspired by Linux shells: bash, zsh, fish, and nushell.",
        ]
        return CommandResult(output="\n".join(lines))
