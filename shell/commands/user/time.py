"""Display current time."""

from datetime import datetime
from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class TimeCommand(BaseCommand):
    name = "time"
    category = "user"
    description = "Display current time"
    syntax = "time"
    examples = ("time",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        now = datetime.now()
        return CommandResult(output=now.strftime("%H:%M:%S"))
