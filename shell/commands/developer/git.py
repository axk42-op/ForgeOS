"""Git version control (placeholder)."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.panels import ForgePanel


class GitCommand(BaseCommand):
    name = "git"
    category = "developer"
    description = "Git version control (placeholder)"
    syntax = "git [ARGS...]"
    examples = ("git status",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        subcommand = args[0] if args else "help"
        panel = ForgePanel(
            f"Git integration placeholder.\n"
            f"Requested: [bold cyan]git {' '.join(args)}[/bold cyan]\n\n"
            "Full git wrapper support is planned for a future release.",
            title="Developer Tool",
            border_style="yellow",
        )
        return CommandResult(renderable=panel.render(), data={"subcommand": subcommand})
