"""Rich console output bridged to a tkinter Text widget."""

from __future__ import annotations

import queue
from typing import TYPE_CHECKING

from rich.console import Console

if TYPE_CHECKING:
    import tkinter as tk


class _TkWriter:
    def __init__(self, bridge: TextConsole) -> None:
        self._bridge = bridge

    def write(self, text: str) -> None:
        if text:
            self._bridge.append(text)

    def flush(self) -> None:
        pass


class TextConsole:
    """Thread-safe Rich console that appends to a tkinter Text widget."""

    def __init__(self, text_widget: tk.Text, root: tk.Mk, *, width: int = 100) -> None:
        self._text = text_widget
        self._root = root
        self._queue: queue.Queue[str | tuple[str, str] | str] = queue.Queue()
        self.console = Console(
            file=_TkWriter(self),
            force_terminal=False,
            color_system=None,
            width=width,
            legacy_windows=False,
            highlight=False,
        )
        self._poll()

    def append(self, text: str, tag: str | None = None) -> None:
        if tag:
            self._queue.put((text, tag))
        else:
            self._queue.put(text)

    def clear(self) -> None:
        self._queue.put("__CLEAR__")

    def _poll(self) -> None:
        try:
            while True:
                item = self._queue.get_nowait()
                if item == "__CLEAR__":
                    self._clear_sync()
                elif isinstance(item, tuple):
                    self._append_sync(item[0], item[1])
                else:
                    self._append_sync(item)
        except queue.Empty:
            pass
        self._root.after(50, self._poll)

    def _clear_sync(self) -> None:
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")
        self._text.configure(state="disabled")

    def _append_sync(self, text: str, tag: str | None = None) -> None:
        self._text.configure(state="normal")
        if tag:
            self._text.insert("end", text, tag)
        else:
            self._text.insert("end", text)
        self._text.see("end")
        self._text.configure(state="disabled")
