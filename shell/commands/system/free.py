"""Display memory usage."""

from typing import Any

import psutil

from shell.commands.base import BaseCommand, CommandResult


class FreeCommand(BaseCommand):
    name = "free"
    category = "system"
    description = "Display memory usage"
    syntax = "free"
    examples = ("free",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        mem = psutil.virtual_memory()
        total = mem.total // (1024 * 1024)
        used = mem.used // (1024 * 1024)
        free = mem.available // (1024 * 1024)
        return CommandResult(
            output=(
                "              total        used        free\n"
                f"Mem:        {total:>8} {used:>8} {free:>8}\n"
                "Swap:              0          0          0"
            )
        )
