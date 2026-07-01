"""Forge OS bottom taskbar — real tkinter widgets."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import tkinter as tk

from desktop.gui import theme as T

if TYPE_CHECKING:
    from desktop.gui.app import ForgeDesktop


class Taskbar(tk.Frame):
    """Bottom taskbar with Start, app buttons, clock, and user."""

    def __init__(self, desktop: ForgeDesktop) -> None:
        super().__init__(desktop.root, bg=T.BG_TASKBAR, height=44)
        self.desktop = desktop
        self.pack_propagate(False)

        left = tk.Frame(self, bg=T.BG_TASKBAR)
        left.pack(side="left", fill="y", padx=4, pady=4)

        self._start_btn = tk.Button(
            left,
            text="⊞  Start",
            font=T.FONT_TITLE,
            fg="white",
            bg=T.ACCENT,
            activebackground="#e67e00",
            activeforeground="white",
            bd=0,
            padx=12,
            pady=4,
            command=self.desktop.toggle_start_menu,
        )
        self._start_btn.pack(side="left", padx=(4, 8))

        for label, command in (
            ("Terminal", self.desktop.open_terminal),
            ("About", self.desktop.open_about),
            ("Settings", self.desktop.open_settings),
        ):
            tk.Button(
                left,
                text=label,
                font=T.FONT_UI,
                fg="white",
                bg=T.ACCENT_BLUE,
                activebackground="#2a508c",
                activeforeground="white",
                bd=0,
                padx=10,
                pady=4,
                command=command,
            ).pack(side="left", padx=2)

        self._apps_frame = tk.Frame(self, bg=T.BG_TASKBAR)
        self._apps_frame.pack(side="left", fill="y", padx=8, pady=4)

        right = tk.Frame(self, bg=T.BG_TASKBAR)
        right.pack(side="right", fill="y", padx=8, pady=6)

        self._clock = tk.Label(right, font=T.FONT_CLOCK, fg=T.FG_TEXT, bg=T.BG_TASKBAR)
        self._clock.pack(side="right", padx=(8, 0))

        user = desktop.forge_os.shell.session.environment.get("USER", "forge")
        tk.Label(
            right,
            text=user,
            font=T.FONT_TITLE,
            fg=T.ACCENT,
            bg=T.BG_TASKBAR,
        ).pack(side="right", padx=(12, 4))
        self._tick()

    def _tick(self) -> None:
        now = datetime.now()
        self._clock.config(text=now.strftime("%a %d %b %Y   %I:%M %p"))
        self.desktop.root.after(1000, self._tick)

    def refresh_apps(self) -> None:
        for child in self._apps_frame.winfo_children():
            child.destroy()

        for window in self.desktop.wm.windows:
            label = window.title
            minimized = window._minimized
            style_bg = T.ACCENT_GREEN if not minimized else T.BG_TITLE

            tk.Button(
                self._apps_frame,
                text=f"■ {label}",
                font=T.FONT_UI,
                fg="white",
                bg=style_bg,
                activebackground=T.ACCENT_GREEN,
                activeforeground="white",
                bd=0,
                padx=10,
                pady=4,
                command=lambda w=window: w.restore() if w._minimized else w.focus(),
            ).pack(side="left", padx=2)
