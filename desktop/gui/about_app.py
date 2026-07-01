"""Simple About window."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tkinter as tk

from desktop.gui import theme as T
from desktop.gui.window_manager import ManagedWindow

if TYPE_CHECKING:
    from desktop.gui.app import ForgeDesktop


class AboutApp(ManagedWindow):
    def __init__(self, desktop: ForgeDesktop) -> None:
        super().__init__(desktop, "About Forge OS", width=480, height=320, x=200, y=120)
        body = tk.Frame(self.content, bg=T.BG_WINDOW, padx=24, pady=20)
        body.pack(fill="both", expand=True)

        tk.Label(body, text="Forge OS", font=("Segoe UI", 20, "bold"), fg=T.ACCENT, bg=T.BG_WINDOW).pack(anchor="w")
        tk.Label(
            body,
            text=f"Version {desktop.forge_os.VERSION}",
            font=T.FONT_UI,
            fg=T.FG_TEXT,
            bg=T.BG_WINDOW,
        ).pack(anchor="w", pady=(4, 16))
        tk.Label(
            body,
            text=(
                "A Python virtual operating system.\n\n"
                "• Terminal runs as a window on this desktop\n"
                "• More apps will open the same way\n"
                "• Inspired by Linux desktop environments"
            ),
            font=T.FONT_UI,
            fg=T.FG_DIM,
            bg=T.BG_WINDOW,
            justify="left",
        ).pack(anchor="w")
