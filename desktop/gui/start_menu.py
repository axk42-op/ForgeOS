"""Start menu popup."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tkinter as tk

from desktop.gui import theme as T
from desktop.menus import MENU_LABELS, MENUS, MenuItem

if TYPE_CHECKING:
    from desktop.gui.app import ForgeDesktop


class StartMenu(tk.Toplevel):
    """Popup Start menu anchored to the taskbar."""

    def __init__(self, desktop: ForgeDesktop) -> None:
        super().__init__(desktop.root)
        self.desktop = desktop
        self.overrideredirect(True)
        self.configure(bg=T.BORDER)

        outer = tk.Frame(self, bg=T.BG_WINDOW, padx=1, pady=1)
        outer.pack(fill="both", expand=True)

        header = tk.Label(
            outer,
            text="Forge OS",
            font=("Segoe UI", 12, "bold"),
            fg=T.ACCENT,
            bg=T.BG_WINDOW,
            anchor="w",
            padx=12,
            pady=10,
        )
        header.pack(fill="x")

        body = tk.Frame(outer, bg=T.BG_WINDOW, padx=8, pady=4)
        body.pack(fill="both", expand=True)

        for key in ("start", "file", "view", "terminal", "help", "settings"):
            self._section(body, MENU_LABELS[key], MENUS[key], key)

        sep = tk.Frame(outer, bg=T.BORDER, height=1)
        sep.pack(fill="x", padx=8)

        footer = tk.Frame(outer, bg=T.BG_WINDOW, padx=12, pady=8)
        footer.pack(fill="x")
        tk.Button(
            footer,
            text="Shut down",
            font=T.FONT_UI,
            fg="white",
            bg="#da3633",
            activebackground="#b62324",
            bd=0,
            padx=12,
            pady=4,
            command=self.desktop.shutdown,
        ).pack(anchor="w")

        self.bind("<FocusOut>", lambda _e: self.close())
        self.protocol("WM_DELETE_WINDOW", self.close)

    def _section(
        self,
        parent: tk.Frame,
        title: str,
        items: tuple[MenuItem, ...],
        category: str,
    ) -> None:
        row = tk.Frame(parent, bg=T.BG_WINDOW)
        row.pack(fill="x", pady=2)

        tk.Label(row, text=title, font=T.FONT_TITLE, fg=T.ACCENT_BLUE, bg=T.BG_WINDOW, width=10, anchor="w").pack(
            side="left"
        )

        links = tk.Frame(row, bg=T.BG_WINDOW)
        links.pack(side="left", fill="x", expand=True)

        for item in items[:4]:
            tk.Button(
                links,
                text=item.label,
                font=T.FONT_UI,
                fg=T.FG_TEXT,
                bg=T.BG_WINDOW,
                activebackground=T.BG_TITLE,
                activeforeground=T.ACCENT,
                bd=0,
                anchor="w",
                command=lambda cmd=item.command: self._launch(cmd),
            ).pack(fill="x")

        if len(items) > 4:
            tk.Button(
                links,
                text=f"More {title}…",
                font=T.FONT_UI,
                fg=T.FG_DIM,
                bg=T.BG_WINDOW,
                activebackground=T.BG_TITLE,
                bd=0,
                anchor="w",
                command=lambda c=category: self._open_terminal_menu(c),
            ).pack(fill="x", anchor="w")

    def _launch(self, command: str) -> None:
        self.close()
        if command in {"help", "forgefetch", "clear", "shutdown", "docs", "source"}:
            self.desktop.run_in_terminal(command)
        else:
            self.desktop.open_terminal()
            self.desktop.run_in_terminal(command)

    def _open_terminal_menu(self, category: str) -> None:
        self.close()
        self.desktop.open_terminal()
        self.desktop.run_in_terminal(f"menu {category}")

    def show_at(self, x: int, y: int) -> None:
        self.update_idletasks()
        self.geometry(f"380x420+{x}+{y}")
        self.deiconify()
        self.lift()
        self.focus_force()

    def close(self) -> None:
        self.desktop._start_menu = None
        self.destroy()
