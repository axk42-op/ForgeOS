"""Display manual for a command."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.panels import ForgePanel


class ManCommand(BaseCommand):
    name = "man"
    category = "network"
    description = "Display manual for a command"
    syntax = "man COMMAND"
    examples = ("man ls",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if not args:
            return CommandResult(output="What manual page do you want?", exit_code=1)

        registry = context["registry"]
        command_class = registry.get(args[0])
        if command_class is None:
            return CommandResult(output=f"No manual entry for {args[0]}", exit_code=1)

        instance = command_class()
        panel = ForgePanel(instance.help_text(), title=f"Manual: {instance.name}", border_style="blue")
        return CommandResult(renderable=panel.render())
