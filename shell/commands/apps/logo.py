"""Display Forge OS logo."""

from typing import Any

from shell.banner import FORGE_LOGO
from shell.commands.base import BaseCommand, CommandResult
from rich.text import Text


class LogoCommand(BaseCommand):
    name = "logo"
    category = "apps"
    description = "Display Forge OS logo"
    syntax = "logo"
    examples = ("logo",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        return CommandResult(renderable=Text(FORGE_LOGO, style="bold cyan"))
