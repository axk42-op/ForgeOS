"""Terminate a process (virtual)."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class KillCommand(BaseCommand):
    name = "kill"
    category = "system"
    description = "Send signal to a process (virtual)"
    syntax = "kill PID"
    examples = ("kill 42",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if not args:
            return CommandResult(output="kill: usage: kill PID", exit_code=1)

        pid = args[0]
        if pid in ("1", "42"):
            return CommandResult(output=f"kill: cannot terminate protected process {pid}", exit_code=1)

        return CommandResult(output=f"Sent SIGTERM to process {pid} (simulated).")
