"""Display information about Forge OS."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.panels import ForgePanel


class AboutCommand(BaseCommand):
    name = "about"
    category = "system"
    description = "Display information about Forge OS"
    syntax = "about"
    examples = ("about",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        panel = ForgePanel(
            "[bold cyan]Forge OS[/bold cyan] is a Python-based virtual operating system.\n\n"
            "It provides a complete developer environment with its own shell,\n"
            "virtual filesystem, package manager, and application ecosystem.\n\n"
            "This is [italic]not[/italic] a real operating system or kernel.",
            title="About Forge OS",
            border_style="cyan",
        )
        return CommandResult(renderable=panel.render())
