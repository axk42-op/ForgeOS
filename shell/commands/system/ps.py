"""List running processes (virtual)."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.tables import ForgeTable


class PsCommand(BaseCommand):
    name = "ps"
    category = "system"
    description = "List running processes"
    syntax = "ps"
    examples = ("ps",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        users = context["users"]
        table = ForgeTable(title="Processes")
        table.add_column("PID", style="cyan")
        table.add_column("USER", style="green")
        table.add_column("CMD")

        processes = [
            ("1", "root", "forge-kernel"),
            ("42", users.whoami(), "forge-shell"),
            ("43", users.whoami(), "vfs-daemon"),
            ("44", users.whoami(), "forgepkgd"),
        ]
        for pid, user, cmd in processes:
            table.add_row(pid, user, cmd)

        return CommandResult(renderable=table.render())
