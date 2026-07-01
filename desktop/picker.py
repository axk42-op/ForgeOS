"""Interactive menu picker for the Forge OS taskbar."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from desktop.menus import MenuItem

if TYPE_CHECKING:
    from rich.console import Console


def pick_item(
    title: str,
    items: tuple[MenuItem, ...],
    console: Console,
    context: dict[str, Any] | None = None,
) -> str | None:
    """Return the command line for the chosen item, or None if cancelled."""
    if not items:
        return None

    if context and context.get("gui_mode"):
        return _pick_numbered(title, items, console, context.get("gui_read_line"))

    values = [(item.command, item.label) for item in items]

    try:
        from prompt_toolkit.shortcuts import radiolist_dialog

        result = radiolist_dialog(
            title=f"Forge OS — {title}",
            text="Use arrow keys and Enter to choose:",
            values=values,
        ).run()
        if result is None:
            return None
        return str(result)
    except Exception:
        return _pick_numbered(title, items, console, None)


def _pick_numbered(
    title: str,
    items: tuple[MenuItem, ...],
    console: Console,
    read_line,
) -> str | None:
    console.print()
    console.print(f"[bold cyan]{title}[/bold cyan]")
    for index, item in enumerate(items, start=1):
        console.print(f"  [bold]{index:2}.[/bold] {item.label}  [dim]({item.command})[/dim]")
    console.print("   [dim]Enter a number, or press Enter to cancel[/dim]")

    try:
        if read_line:
            choice = read_line("Choice: ").strip()
        else:
            choice = input("Choice: ").strip()
    except (EOFError, KeyboardInterrupt):
        console.print()
        return None

    if not choice:
        return None

    if not choice.isdigit():
        console.print("[red]Invalid choice.[/red]")
        return None

    index = int(choice)
    if index < 1 or index > len(items):
        console.print("[red]Invalid choice.[/red]")
        return None

    return items[index - 1].command
