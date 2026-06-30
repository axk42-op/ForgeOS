"""Node package manager (placeholder)."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.panels import ForgePanel


class NpmCommand(BaseCommand):
    name = "npm"
    category = "developer"
    description = "Node package manager (placeholder)"
    syntax = "npm [ARGS...]"
    examples = ("npm --version",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        panel = ForgePanel(
            "npm integration is a placeholder in Forge OS v0.1.",
            title="Developer Tool",
            border_style="yellow",
        )
        return CommandResult(renderable=panel.render())
