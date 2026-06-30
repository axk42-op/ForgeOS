"""Display current date."""

from datetime import datetime
from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class DateCommand(BaseCommand):
    name = "date"
    category = "user"
    description = "Display current date"
    syntax = "date"
    examples = ("date",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        now = datetime.now()
        return CommandResult(output=now.strftime("%A, %B %d, %Y"))
