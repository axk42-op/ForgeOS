"""Node.js runtime (placeholder)."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.panels import ForgePanel


class NodeCommand(BaseCommand):
    name = "node"
    category = "developer"
    description = "Node.js runtime (placeholder)"
    syntax = "node [ARGS...]"
    examples = ("node --version",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        panel = ForgePanel(
            "Node.js integration is a placeholder in Forge OS v0.1.",
            title="Developer Tool",
            border_style="yellow",
        )
        return CommandResult(renderable=panel.render())
