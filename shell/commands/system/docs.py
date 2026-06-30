"""Open Forge OS documentation on GitHub Wiki."""

import webbrowser
from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.links import GITHUB_WIKI_DOCS
from shell.ui.panels import ForgePanel


class DocsCommand(BaseCommand):
    name = "docs"
    category = "system"
    description = "Open Forge OS documentation (GitHub Wiki)"
    syntax = "docs"
    examples = ("docs",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        webbrowser.open(GITHUB_WIKI_DOCS)
        panel = ForgePanel(
            f"Opening Forge OS documentation in your browser.\n\n"
            f"[bold cyan]{GITHUB_WIKI_DOCS}[/bold cyan]",
            title="Documentation",
            border_style="cyan",
        )
        return CommandResult(renderable=panel.render())
