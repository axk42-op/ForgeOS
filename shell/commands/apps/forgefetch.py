"""Display system information."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.neofetch import build_neofetch


class ForgefetchCommand(BaseCommand):
    name = "forgefetch"
    category = "apps"
    description = "Display system information"
    syntax = "forgefetch"
    examples = ("forgefetch",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        return CommandResult(
            renderable=build_neofetch(
                kernel=context["kernel"],
                users=context["users"],
                packages=context["packages"],
                session=context["session"],
            )
        )
