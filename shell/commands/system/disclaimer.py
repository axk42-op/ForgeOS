"""Display Forge OS legal and data-storage disclaimer."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.panels import ForgePanel


class DisclaimerCommand(BaseCommand):
    name = "disclaimer"
    category = "system"
    description = "Display legal disclaimer and data-storage notice"
    syntax = "disclaimer"
    examples = ("disclaimer",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        storage = (
            "[bold]Account storage:[/bold] Credentials are stored locally on this "
            "machine only (`%LOCALAPPDATA%\\ForgeOS\\ForgeOS\\credentials.json` on "
            "Windows). Usernames and salted password hashes are saved — plain-text "
            "passwords are never stored."
        )

        panel = ForgePanel(
            "Forge OS is a [italic]virtual[/italic] operating system — not a real kernel "
            "or hardware OS. Commands, network tools, and processes are simulated for "
            "learning and development.\n\n"
            f"{storage}\n\n"
            "[bold]No warranty:[/bold] Forge OS is provided \"as is\" without warranty "
            "of any kind. Use at your own risk.",
            title="Disclaimer",
            border_style="yellow",
        )
        return CommandResult(renderable=panel.render())
