"""Boot banner and startup display."""

from collections.abc import Callable
from typing import Any

from rich.console import Console

from shell.ui.animations import BootLoader
from shell.ui.branding import FORGE_LOGO
from shell.ui.neofetch import build_neofetch


class BootBanner:
    """Displays the Forge OS boot screen."""

    def __init__(self, console: Console | None = None, version: str = "1.0.0") -> None:
        self._console = console or Console(force_terminal=True, legacy_windows=False)
        self._version = version

    def show_neofetch(
        self,
        *,
        kernel: Any,
        users: Any,
        packages: Any,
        session: Any,
    ) -> None:
        """Neofetch-style welcome: compact sig left, block logo + info right."""
        self._console.print()
        self._console.print(
            build_neofetch(
                kernel=kernel,
                users=users,
                packages=packages,
                session=session,
            )
        )
        self._console.print()
        self._console.print("Type [bold cyan]help[/] to list available commands.")
        self._console.print()

    def build_neofetch_text(
        self,
        *,
        kernel: Any,
        users: Any,
        packages: Any,
        session: Any,
        width: int = 96,
    ) -> str:
        """Export neofetch banner as plain text for GUI terminal windows."""
        export = Console(force_terminal=False, width=width, legacy_windows=False)
        with export.capture() as capture:
            export.print(
                build_neofetch(
                    kernel=kernel,
                    users=users,
                    packages=packages,
                    session=session,
                )
            )
        return capture.get()


class BootSequence:
    """Orchestrates animated subsystem loading during boot."""

    SUBSYSTEMS = (
        ("Kernel", "Initializing kernel services"),
        ("Virtual Filesystem", "Mounting virtual filesystem"),
        ("User Manager", "Loading user accounts"),
        ("Package Manager", "Initializing package manager"),
        ("Shell", "Starting Forge Shell"),
    )

    def __init__(self, console: Console | None = None) -> None:
        self._console = console or Console()
        self._loader = BootLoader(console=self._console)

    def run(self, loaders: list[tuple[str, Callable[[], None]]]) -> None:
        """Run boot animation while executing loader callables."""
        self._loader.run(loaders)


# Re-export for commands that import from banner
__all__ = ["BootBanner", "BootSequence", "FORGE_LOGO"]
