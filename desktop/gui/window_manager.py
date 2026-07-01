"""Managed application windows on the Forge OS desktop."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import tkinter as tk

from desktop.gui import theme as T

if TYPE_CHECKING:
    from desktop.gui.app import ForgeDesktop


class ManagedWindow(tk.Frame):
    """A draggable window with title bar, minimize, and close."""

    def __init__(
        self,
        desktop: ForgeDesktop,
        title: str,
        *,
        width: int = 820,
        height: int = 520,
        x: int = 80,
        y: int = 60,
        on_close: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(desktop.desktop_frame, bg=T.BORDER, bd=0, highlightthickness=0)
        self.desktop = desktop
        self.title = title
        self._on_close = on_close
        self._drag_x = 0
        self._drag_y = 0
        self._minimized = False
        self._saved_geometry: tuple[int, int, int, int] | None = None

        self.place(x=x, y=y, width=width, height=height)
        self.lift()

        self._title_bar = tk.Frame(self, bg=T.BG_TITLE, height=32)
        self._title_bar.pack(fill="x")
        self._title_bar.pack_propagate(False)

        self._title_label = tk.Label(
            self._title_bar,
            text=f"  {title}",
            font=T.FONT_TITLE,
            fg=T.FG_TEXT,
            bg=T.BG_TITLE,
            anchor="w",
        )
        self._title_label.pack(side="left", fill="both", expand=True)

        btn_frame = tk.Frame(self._title_bar, bg=T.BG_TITLE)
        btn_frame.pack(side="right")

        tk.Button(
            btn_frame,
            text="—",
            font=T.FONT_UI,
            fg=T.FG_TEXT,
            bg=T.BG_TITLE,
            activebackground=T.BORDER,
            bd=0,
            padx=8,
            command=self.minimize,
        ).pack(side="left")

        tk.Button(
            btn_frame,
            text="✕",
            font=T.FONT_UI,
            fg=T.FG_TEXT,
            bg=T.BG_TITLE,
            activebackground="#da3633",
            bd=0,
            padx=8,
            command=self.close,
        ).pack(side="left")

        for widget in (self._title_bar, self._title_label):
            widget.bind("<ButtonPress-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._on_drag)

        self.content = tk.Frame(self, bg=T.BG_WINDOW)
        self.content.pack(fill="both", expand=True)

        desktop.register_window(self)

    def _start_drag(self, event: tk.Event) -> None:
        self._drag_x = event.x_root - self.winfo_x()
        self._drag_y = event.y_root - self.winfo_y()
        self.lift()
        self.desktop.focus_window(self)

    def _on_drag(self, event: tk.Event) -> None:
        x = max(0, event.x_root - self._drag_x)
        y = max(0, event.y_root - self._drag_y)
        self.place(x=x, y=y)

    def focus(self) -> None:
        self.lift()

    def minimize(self) -> None:
        if self._minimized:
            return
        self._saved_geometry = (
            self.winfo_x(),
            self.winfo_y(),
            self.winfo_width(),
            self.winfo_height(),
        )
        self.place_forget()
        self._minimized = True
        self.desktop.on_window_minimized(self)

    def restore(self) -> None:
        if not self._minimized:
            self.focus()
            return
        if self._saved_geometry:
            x, y, w, h = self._saved_geometry
            self.place(x=x, y=y, width=w, height=h)
        self._minimized = False
        self.lift()
        self.desktop.on_window_restored(self)

    def close(self) -> None:
        self.desktop.unregister_window(self)
        if self._on_close:
            self._on_close()
        self.destroy()


class WindowManager:
    """Tracks open windows for the taskbar."""

    def __init__(self) -> None:
        self.windows: list[ManagedWindow] = []

    def add(self, window: ManagedWindow) -> None:
        self.windows.append(window)

    def remove(self, window: ManagedWindow) -> None:
        if window in self.windows:
            self.windows.remove(window)

    def visible_windows(self) -> list[ManagedWindow]:
        return list(self.windows)
