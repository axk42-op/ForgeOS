"""Forge OS settings (taskbar gear icon)."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class SettingsCommand(BaseCommand):
    name = "settings"
    category = "system"
    description = "Open Settings (password, environment, sign out)"
    syntax = "settings"
    examples = ("settings",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        from shell.commands.system.menu import MenuCommand

        return MenuCommand().execute(["settings"], context)
