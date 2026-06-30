"""Rich spinner utilities."""

from rich.console import Console
from rich.status import Status


class ForgeSpinner:
    """Status spinner for indeterminate operations."""

    def __init__(
        self,
        message: str = "Loading...",
        console: Console | None = None,
        spinner: str = "dots",
    ) -> None:
        self._message = message
        self._console = console or Console()
        self._spinner = spinner
        self._status: Status | None = None

    def __enter__(self) -> "ForgeSpinner":
        self._status = self._console.status(self._message, spinner=self._spinner)
        self._status.__enter__()
        return self

    def __exit__(self, *args) -> None:
        if self._status:
            self._status.__exit__(*args)

    def update(self, message: str) -> None:
        if self._status:
            self._status.update(message)
