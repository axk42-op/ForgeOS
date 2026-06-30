"""Prompt generation and formatting."""

from rich.text import Text

from shell.config import ShellConfig
from shell.session import ShellSession
from shell.ui.colors import ThemeColors


class PromptRenderer:
    """Generates shell prompts with support for themes and git branch (future)."""

    def __init__(self, session: ShellSession, config: ShellConfig | None = None) -> None:
        self._session = session
        self._config = config or session.config
        self._colors = ThemeColors(config=self._config)

    def render_plain(self) -> str:
        username = self._session.environment.get("USER", "forge")
        hostname = self._session.environment.get("HOSTNAME", "localhost")
        directory = self._session.cwd or "/"
        symbol = self._config.prompt_symbol
        return f"{username}@{hostname}:{directory} {symbol} "

    def render_rich(self) -> Text:
        username = self._session.environment.get("USER", "forge")
        hostname = self._session.environment.get("HOSTNAME", "localhost")
        directory = self._session.cwd or "/"
        symbol = self._config.prompt_symbol

        text = Text()
        text.append(username, style=self._colors.username)
        text.append("@", style=self._colors.separator)
        text.append(hostname, style=self._colors.hostname)
        text.append(":", style=self._colors.separator)
        text.append(directory, style=self._colors.directory)
        text.append(f" {symbol} ", style=self._colors.symbol)
        return text

    def render_git_branch(self) -> str | None:
        """Placeholder for future git integration."""
        return None
