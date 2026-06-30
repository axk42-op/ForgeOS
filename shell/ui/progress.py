"""Rich progress bar utilities."""

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


class ForgeProgress:
    """Progress bar wrapper for long-running operations."""

    def __init__(self, description: str = "Working...") -> None:
        self._description = description
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
        )

    def __enter__(self) -> Progress:
        self._progress.start()
        return self._progress

    def __exit__(self, *args) -> None:
        self._progress.stop()
