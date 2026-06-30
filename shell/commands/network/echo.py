"""Print text to stdout."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class EchoCommand(BaseCommand):
    name = "echo"
    category = "network"
    description = "Print text to stdout"
    syntax = "echo [TEXT...]"
    examples = ("echo Hello",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        session = context["session"]
        stdin = context.get("stdin", "")

        if args:
            text = " ".join(args)
            expanded = session.environment.expand(text)
            return CommandResult(output=expanded)

        if stdin:
            return CommandResult(output=stdin)

        return CommandResult(output="")
