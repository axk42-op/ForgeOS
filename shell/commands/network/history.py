"""Display command history."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class HistoryCommand(BaseCommand):
    name = "history"
    category = "network"
    description = "Display command history"
    syntax = "history"
    examples = ("history",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        session = context["session"]
        lines = [f"  {index:4d}  {entry}" for index, entry in enumerate(session.history.entries(), 1)]
        return CommandResult(output="\n".join(lines) if lines else "No history entries.")
