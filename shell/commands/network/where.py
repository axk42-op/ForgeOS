"""Locate a command (alias)."""

from typing import Any

from shell.commands.network.which import WhichCommand


class WhereCommand(WhichCommand):
    name = "where"
    category = "network"
    description = "Locate a command (alias)"
    syntax = "where COMMAND"
    examples = ("where ls",)

    def execute(self, args: list[str], context: dict[str, Any]):
        return super().execute(args, context)
