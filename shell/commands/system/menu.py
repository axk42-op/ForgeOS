"""Forge OS taskbar menus — File, View, Terminal, Help, Settings."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class MenuCommand(BaseCommand):
    name = "menu"
    category = "system"
    description = "Open a taskbar menu (start, file, view, terminal, help, settings)"
    syntax = "menu [CATEGORY]"
    examples = ("menu", "menu file", "menu view", "menu help")

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        from desktop.menus import MENU_LABELS, MENUS
        from desktop.picker import pick_item
        from desktop.runner import run_shell_line

        session = context["session"]
        console = context["console"]

        category = args[0].lower() if args else "start"
        if category not in MENUS:
            names = ", ".join(sorted(MENUS))
            return CommandResult(
                output=f"menu: unknown category '{category}'. Try: {names}",
                exit_code=1,
            )

        title = MENU_LABELS.get(category, category.title())
        command_line = pick_item(title, MENUS[category], console, context)
        if command_line is None:
            return CommandResult(output="Menu closed.")

        if command_line == "search":
            try:
                if context.get("gui_read_line"):
                    query = context["gui_read_line"]("Search: ").strip()
                else:
                    query = input("Search: ").strip()
            except (EOFError, KeyboardInterrupt):
                console.print()
                return CommandResult(output="Search cancelled.")
            if not query:
                return CommandResult(output="Search cancelled.")
            command_line = f"search {query}"

        return run_shell_line(command_line, context)
