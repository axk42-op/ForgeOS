"""Display copyright notice."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class CopyrightCommand(BaseCommand):
    name = "copyright"
    category = "system"
    description = "Display copyright notice"
    syntax = "copyright"
    examples = ("copyright",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        return CommandResult(output="Copyright (c) 2026 Forge OS Project. All rights reserved.")
