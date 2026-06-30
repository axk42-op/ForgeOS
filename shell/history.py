"""Command history management."""

from collections.abc import Sequence

from prompt_toolkit.history import History


class CommandHistory:
    """Stores and retrieves command history entries."""

    def __init__(self, max_entries: int = 1000) -> None:
        self._max_entries = max_entries
        self._entries: list[str] = []

    def add(self, command: str) -> None:
        stripped = command.strip()
        if not stripped:
            return
        if self._entries and self._entries[-1] == stripped:
            return
        self._entries.append(stripped)
        if len(self._entries) > self._max_entries:
            self._entries.pop(0)

    def entries(self) -> Sequence[str]:
        return tuple(self._entries)

    def search(self, prefix: str) -> list[str]:
        return [entry for entry in self._entries if entry.startswith(prefix)]

    def clear(self) -> None:
        self._entries.clear()

    def __len__(self) -> int:
        return len(self._entries)


class SessionHistory(History):
    """prompt_toolkit history backed by CommandHistory."""

    def __init__(self, command_history: CommandHistory) -> None:
        super().__init__()
        self._history = command_history

    def load_history_strings(self):
        yield from reversed(self._history.entries())

    def store_string(self, string: str) -> None:
        self._history.add(string)
