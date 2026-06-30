"""Shell logging."""

from datetime import datetime
from enum import IntEnum

from rich.console import Console


class LogLevel(IntEnum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40


class ShellLogger:
    """Structured logger for shell operations."""

    def __init__(self, console: Console | None = None, level: LogLevel = LogLevel.WARNING) -> None:
        self._console = console or Console()
        self._level = level
        self._entries: list[tuple[datetime, LogLevel, str]] = []

    def set_level(self, level: LogLevel) -> None:
        self._level = level

    def debug(self, message: str) -> None:
        self._log(LogLevel.DEBUG, message)

    def info(self, message: str) -> None:
        self._log(LogLevel.INFO, message)

    def warning(self, message: str) -> None:
        self._log(LogLevel.WARNING, message)

    def error(self, message: str) -> None:
        self._log(LogLevel.ERROR, message)

    def _log(self, level: LogLevel, message: str) -> None:
        self._entries.append((datetime.now(), level, message))
        if level >= self._level:
            style = {
                LogLevel.DEBUG: "dim",
                LogLevel.INFO: "cyan",
                LogLevel.WARNING: "yellow",
                LogLevel.ERROR: "bold red",
            }[level]
            self._console.print(f"[{level.name}] {message}", style=style)
