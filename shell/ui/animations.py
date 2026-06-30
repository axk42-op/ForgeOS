"""Boot and UI animations."""

from collections.abc import Callable

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn


class BootLoader:
    """Animated boot sequence using Rich status spinners."""

    def __init__(self, console: Console | None = None) -> None:
        self._console = console or Console(force_terminal=True, legacy_windows=False)

    def run(self, loaders: list[tuple[str, Callable[[], None]]]) -> None:
        with Progress(
            SpinnerColumn(style="cyan"),
            TextColumn("[bold cyan]{task.description}"),
            console=self._console,
            transient=True,
        ) as progress:
            for label, loader in loaders:
                task = progress.add_task(label, total=None)
                loader()
                progress.update(task, description=f"[green]✓[/green] {label}")
        self._console.print()
