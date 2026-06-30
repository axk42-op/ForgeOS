"""Display Forge OS legal and data-storage disclaimer."""

from typing import Any

from auth.config import is_supabase_configured
from shell.commands.base import BaseCommand, CommandResult
from shell.ui.panels import ForgePanel


class DisclaimerCommand(BaseCommand):
    name = "disclaimer"
    category = "system"
    description = "Display legal disclaimer and data-storage notice"
    syntax = "disclaimer"
    examples = ("disclaimer",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        supabase_notice = (
            "[bold]Database:[/bold] Forge OS uses [cyan]Supabase[/cyan] "
            "(PostgreSQL) for account storage. Usernames and salted password "
            "hashes are stored in the `forge_users` table — plain-text passwords "
            "are never saved.\n\n"
        )

        if is_supabase_configured():
            storage = (
                f"{supabase_notice}"
                "[bold]Status:[/bold] Supabase is [green]active[/green] for this install.\n\n"
                "By creating an account, you acknowledge that your username and "
                "hashed credentials are stored in our Supabase database."
            )
        else:
            storage = (
                f"{supabase_notice}"
                "[bold]Status:[/bold] Supabase is not configured on this machine yet "
                "(credentials are stored locally until `.env` is set up).\n\n"
                "Configure `FORGEOS_SUPABASE_URL` and `FORGEOS_SUPABASE_KEY` in `.env` "
                "to use cloud storage."
            )

        panel = ForgePanel(
            "Forge OS is a [italic]virtual[/italic] operating system — not a real kernel "
            "or hardware OS. Commands, network tools, and processes are simulated for "
            "learning and development.\n\n"
            f"{storage}\n\n"
            "[bold]No warranty:[/bold] Forge OS is provided \"as is\" without warranty "
            "of any kind. Use at your own risk.",
            title="Disclaimer",
            border_style="yellow",
        )
        return CommandResult(renderable=panel.render())
