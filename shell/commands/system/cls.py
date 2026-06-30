"""Clear the terminal screen (alias)."""

from typing import Any

from shell.commands.system.clear import ClearCommand


class ClsCommand(ClearCommand):
    name = "cls"
    category = "system"
    description = "Clear the terminal screen (alias)"
    syntax = "cls"
    examples = ("cls",)

    def execute(self, args: list[str], context: dict[str, Any]):
        return super().execute(args, context)
