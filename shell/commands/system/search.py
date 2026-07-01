"""Search Forge OS commands."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.tables import ForgeTable


class SearchCommand(BaseCommand):
    name = "search"
    category = "system"
    description = "Search available commands"
    syntax = "search QUERY"
    examples = ("search file", "search user")

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if not args:
            return CommandResult(
                output="search: usage: search QUERY",
                exit_code=1,
            )

        query = " ".join(args).lower()
        registry = context["registry"]
        matches: list[tuple[str, str, str]] = []

        for command_class in registry.all_commands():
            haystack = " ".join(
                (
                    command_class.name,
                    command_class.category,
                    command_class.description,
                    " ".join(command_class.aliases),
                )
            ).lower()
            if query in haystack:
                matches.append(
                    (command_class.name, command_class.category, command_class.description)
                )

        if not matches:
            return CommandResult(output=f"search: no results for '{query}'", exit_code=1)

        table = ForgeTable(title=f"Search: {query}")
        table.add_column("Command", style="cyan")
        table.add_column("Category", style="magenta")
        table.add_column("Description")
        for name, category, description in sorted(matches):
            table.add_row(name, category, description)
        return CommandResult(renderable=table.render())
