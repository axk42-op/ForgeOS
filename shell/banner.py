"""Boot banner and startup display."""

from collections.abc import Callable

from rich.console import Console
from rich.text import Text

from shell.ui.animations import BootLoader
from shell.ui.panels import ForgePanel


FORGE_LOGO = """\
███████╗ ██████╗ ██████╗  ██████╗ ███████╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
█████╗  ██║   ██║██████╔╝██║  ███╗█████╗
██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝
██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝"""


class BootBanner:
    """Displays the Forge OS boot screen."""

    def __init__(self, console: Console | None = None, version: str = "1.0.0") -> None:
        self._console = console or Console(force_terminal=True, legacy_windows=False)
        self._version = version

    def show_logo(self) -> None:
        self._console.print(Text(FORGE_LOGO, style="bold cyan"))
        self._console.print()
        self._console.print(f"Forge OS v{self._version}", style="bold white")
        self._console.print()

    def show_welcome_panel(self) -> None:
        panel = ForgePanel(
            "Welcome to Forge OS — a Python virtual operating system.\n"
            "Type [bold cyan]help[/] to list available commands.",
            title="Forge Shell",
            border_style="cyan",
        )
        self._console.print(panel.render())


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
