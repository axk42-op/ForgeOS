"""Fetch a URL (simulated)."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.panels import ForgePanel


class CurlCommand(BaseCommand):
    name = "curl"
    category = "network"
    description = "Transfer data from a URL (simulated)"
    syntax = "curl URL"
    examples = ("curl https://forge.os",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if not args:
            return CommandResult(output="curl: missing URL", exit_code=1)

        url = args[0]
        panel = ForgePanel(
            f"Simulated GET request to [cyan]{url}[/cyan]\n"
            "HTTP/1.1 200 OK\n"
            "Content-Type: text/plain\n\n"
            "Forge OS virtual network layer (placeholder).",
            title="curl",
            border_style="blue",
        )
        return CommandResult(renderable=panel.render())
