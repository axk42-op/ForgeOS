"""Forge OS bottom taskbar — real menus, clock, and date."""

from __future__ import annotations

from datetime import datetime

from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text

from shell.config import ShellConfig
from shell.session import ShellSession


class DesktopChrome:
    """Renders the bottom taskbar and menu panels."""

    TASKBAR_MENUS: tuple[tuple[str, str], ...] = (
        ("start", "⊞ Start"),
        ("file", "File"),
        ("view", "View"),
        ("terminal", "Terminal"),
        ("help", "Help"),
    )

    def __init__(
        self,
        console: Console,
        session: ShellSession,
        config: ShellConfig | None = None,
    ) -> None:
        self._console = console
        self._session = session
        self._config = config or session.config
        self._open_apps: list[str] = ["Shell"]

    def show_taskbar(self) -> None:
        """Draw the taskbar at the bottom of the terminal (above the prompt)."""
        self._console.print(self._taskbar())

    def show_menu_panel(self, menu_key: str) -> None:
        from desktop.menus import MENU_LABELS, MENUS

        items = MENUS.get(menu_key, ())
        title = MENU_LABELS.get(menu_key, menu_key.title())
        lines = [Text(f"{title} menu", style="bold cyan"), Text("")]
        for item in items:
            lines.append(Text(f"  {item.label}", style="white"))
            lines.append(Text(f"      → {item.command}", style="dim"))
        lines.append(Text(""))
        lines.append(
            Text(f"Open: menu {menu_key}   (interactive picker)", style="bold #FF8C00"),
        )
        self._console.print(
            Panel(
                Group(*lines),
                title=title,
                border_style="cyan",
                padding=(0, 1),
            )
        )

    def register_app(self, name: str) -> None:
        if name not in self._open_apps:
            self._open_apps.append(name)

    def _clock_text(self) -> tuple[str, str]:
        now = datetime.now()
        return now.strftime("%a %d %b %Y"), now.strftime("%I:%M %p")

    def _taskbar(self) -> Panel:
        user = self._session.environment.get("USER", "forge")
        date_text, time_text = self._clock_text()

        line = Text()
        for key, label in self.TASKBAR_MENUS:
            if key == "start":
                line.append(f" {label} ", style="bold white on #FF8C00")
            else:
                line.append(f" {label} ", style="white on #3465A4")

        for app in self._open_apps:
            line.append(f" ■ {app} ", style="bold white on #478061")

        line.append(" ⚙ ", style="white on #555753")
        line.append(" 🔍 ", style="black on #e6edf3")
        line.append(f" {date_text} ", style="bold white on #2d333b")
        line.append(f" {time_text} ", style="bold white on #3465A4")
        line.append(f" {user} ", style="bold white on #FF8C00")

        return Panel(
            line,
            border_style="#478061",
            padding=(0, 0),
            expand=True,
            title="[dim]Forge OS[/dim]",
            title_align="left",
        )
