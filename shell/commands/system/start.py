"""Forge OS Start button."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class StartCommand(BaseCommand):
    name = "start"
    category = "system"
    description = "Open the Start menu"
    syntax = "start"
    examples = ("start",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        from shell.commands.system.menu import MenuCommand

        menu = MenuCommand()
        return menu.execute(["start"], context)
