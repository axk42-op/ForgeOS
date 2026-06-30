"""Display network connections (virtual)."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.tables import ForgeTable


class NetstatCommand(BaseCommand):
    name = "netstat"
    category = "network"
    description = "Display network connections"
    syntax = "netstat"
    examples = ("netstat",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        table = ForgeTable(title="Active Connections")
        table.add_column("Proto", style="cyan")
        table.add_column("Local", style="green")
        table.add_column("Foreign")
        table.add_column("State")

        rows = [
            ("tcp", "127.0.0.1:7722", "0.0.0.0:*", "LISTEN"),
            ("tcp", "127.0.0.1:4422", "127.0.0.1:8811", "ESTABLISHED"),
            ("udp", "0.0.0.0:5353", "0.0.0.0:*", "OPEN"),
        ]
        for row in rows:
            table.add_row(*row)

        return CommandResult(renderable=table.render())
