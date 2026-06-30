"""Screen management utilities."""

from rich.console import Console


class ScreenManager:
    """Manages terminal screen state."""

    def __init__(self, console: Console | None = None) -> None:
        self._console = console or Console()

    def clear(self) -> None:
        self._console.clear()

    def print(self, content: str | object) -> None:
        self._console.print(content)

    @property
    def console(self) -> Console:
        return self._console
