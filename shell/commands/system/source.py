"""Open the Forge OS source repository on GitHub."""

import webbrowser
from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.links import GITHUB_REPO
from shell.ui.panels import ForgePanel


class SourceCommand(BaseCommand):
    name = "source"
    category = "system"
    description = "Open Forge OS source code on GitHub"
    syntax = "source"
    examples = ("source",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        webbrowser.open(GITHUB_REPO)
        panel = ForgePanel(
            f"Opening Forge OS source repository in your browser.\n\n"
            f"[bold cyan]{GITHUB_REPO}[/bold cyan]",
            title="Source",
            border_style="cyan",
        )
        return CommandResult(renderable=panel.render())
