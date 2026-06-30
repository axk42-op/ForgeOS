"""Reboot Forge OS."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class RebootCommand(BaseCommand):
    name = "reboot"
    category = "system"
    description = "Reboot Forge OS"
    syntax = "reboot"
    examples = ("reboot",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        return CommandResult(
            output="Forge OS rebooting... (session ended)",
            should_exit=True,
        )
