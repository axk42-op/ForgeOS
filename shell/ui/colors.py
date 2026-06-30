"""Rich UI color themes."""

from dataclasses import dataclass, field

from shell.config import ShellConfig


@dataclass
class ThemeColors:
    """Color palette for shell UI elements."""

    username: str = "bold green"
    hostname: str = "bold cyan"
    directory: str = "bold blue"
    separator: str = "white"
    symbol: str = "bold yellow"
    success: str = "bold green"
    error: str = "bold red"
    warning: str = "bold yellow"
    info: str = "cyan"
    muted: str = "dim white"
    accent: str = "magenta"
    config: ShellConfig = field(default_factory=ShellConfig, repr=False)

    def __post_init__(self) -> None:
        if self.config.theme == "dark":
            self.directory = "bold magenta"
        elif self.config.theme == "minimal":
            self.username = "white"
            self.hostname = "white"
            self.directory = "white"
