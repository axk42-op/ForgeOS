"""Display system information."""

from typing import Any

from shell.banner import FORGE_LOGO
from shell.commands.base import BaseCommand, CommandResult
from rich.columns import Columns
from rich.text import Text


class ForgefetchCommand(BaseCommand):
    name = "forgefetch"
    category = "apps"
    description = "Display system information"
    syntax = "forgefetch"
    examples = ("forgefetch",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        kernel = context["kernel"]
        users = context["users"]
        packages = context["packages"]
        session = context["session"]

        logo = Text(FORGE_LOGO, style="bold cyan")
        info_lines = [
            f"[bold cyan]OS[/bold cyan]: Forge OS {session.environment.get('FORGE_VERSION', '0.1')}",
            f"[bold cyan]Host[/bold cyan]: {users.hostname}",
            f"[bold cyan]User[/bold cyan]: {users.whoami()}",
            f"[bold cyan]Shell[/bold cyan]: Forge Shell",
            f"[bold cyan]Kernel[/bold cyan]: {kernel.name} {kernel.version}",
            f"[bold cyan]Uptime[/bold cyan]: {kernel.uptime()}",
            f"[bold cyan]Packages[/bold cyan]: {len(packages.list_packages())} (forgepkg)",
            f"[bold cyan]Directory[/bold cyan]: {session.cwd}",
        ]
        info = Text.from_markup("\n".join(info_lines))

        return CommandResult(renderable=Columns([logo, info], padding=(0, 2)))
