"""Display Forge OS logos."""

from typing import Any

from rich.columns import Columns
from rich.text import Text

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.branding import FORGE_LOGO, FORGE_SIG


class LogoCommand(BaseCommand):
    name = "logo"
    category = "apps"
    description = "Display Forge OS logos"
    syntax = "logo"
    examples = ("logo",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        sig = Text(FORGE_SIG, style="bold #FF8C00")
        block = Text(FORGE_LOGO, style="bold cyan")
        return CommandResult(renderable=Columns([sig, block], padding=(0, 4)))
