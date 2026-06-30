"""Display disk usage (virtual)."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.tables import ForgeTable


class DfCommand(BaseCommand):
    name = "df"
    category = "system"
    description = "Display filesystem disk usage"
    syntax = "df"
    examples = ("df",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        table = ForgeTable(title="Filesystem Usage")
        table.add_column("Filesystem", style="cyan")
        table.add_column("Size", style="green")
        table.add_column("Used")
        table.add_column("Avail")
        table.add_column("Use%")
        table.add_column("Mounted on")

        mounts = [
            ("forgefs", "16G", "2.1G", "13G", "14%", "/"),
            ("forgefs", "8G", "512M", "7.5G", "6%", "/home"),
            ("tmpfs", "2G", "12M", "2G", "1%", "/tmp"),
        ]
        for row in mounts:
            table.add_row(*row)

        return CommandResult(renderable=table.render())
