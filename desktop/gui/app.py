"""Forge OS desktop environment — main window."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import TYPE_CHECKING

from desktop.gui import theme as T
from desktop.gui.about_app import AboutApp
from desktop.gui.start_menu import StartMenu
from desktop.gui.taskbar import Taskbar
from desktop.gui.terminal_app import TerminalApp
from desktop.gui.window_manager import WindowManager
from desktop.icon import icon_paths

if TYPE_CHECKING:
    from boot import ForgeOS


class ForgeDesktop:
    """Full Forge OS desktop with taskbar and managed application windows."""

    def __init__(self, forge_os: ForgeOS) -> None:
        self.forge_os = forge_os
        self.wm = WindowManager()
        self._start_menu: StartMenu | None = None
        self._terminal: TerminalApp | None = None
        self._window_offset = 0

        self.root = tk.Tk()
        self.root.title("Forge OS")
        self.root.configure(bg=T.BG_DESKTOP)
        self.root.geometry("1280x720")
        self.root.minsize(960, 540)
        self._center_window(self.root, 1280, 720)

        self._set_icon()
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after(400, lambda: self.root.attributes("-topmost", False))
        self.root.focus_force()

        self.desktop_frame = tk.Frame(self.root, bg=T.BG_DESKTOP)
        self.desktop_frame.pack(fill="both", expand=True)

        self._wallpaper = tk.Label(
            self.desktop_frame,
            text="Forge OS",
            font=("Segoe UI", 28, "bold"),
            fg="#21262d",
            bg=T.BG_DESKTOP,
        )
        self._wallpaper.place(relx=0.5, rely=0.42, anchor="center")

        user = forge_os.shell.session.environment.get("USER", "forge")
        tk.Label(
            self.desktop_frame,
            text=f"Welcome, {user}",
            font=("Segoe UI", 13),
            fg=T.FG_DIM,
            bg=T.BG_DESKTOP,
        ).place(relx=0.5, rely=0.48, anchor="center")

        self.taskbar = Taskbar(self)
        self.taskbar.pack(side="bottom", fill="x")

        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)
        self.root.after(300, self.open_terminal)

    def _center_window(self, window: tk.Mk, width: int, height: int) -> None:
        window.update_idletasks()
        x = max(0, (window.winfo_screenwidth() - width) // 2)
        y = max(0, (window.winfo_screenheight() - height) // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def _set_icon(self) -> None:
        ico = icon_paths().get("ico")
        if ico and ico.is_file():
            try:
                self.root.iconbitmap(str(ico.resolve()))
            except tk.TclError:
                pass

    def register_window(self, window) -> None:
        self.wm.add(window)
        self.taskbar.refresh_apps()

    def unregister_window(self, window) -> None:
        self.wm.remove(window)
        if window is self._terminal:
            self._terminal = None
        self.taskbar.refresh_apps()

    def focus_window(self, window) -> None:
        window.focus()
        self.taskbar.refresh_apps()

    def on_window_minimized(self, _window) -> None:
        self.taskbar.refresh_apps()

    def on_window_restored(self, _window) -> None:
        self.taskbar.refresh_apps()

    def _next_position(self) -> tuple[int, int]:
        self._window_offset = (self._window_offset + 32) % 160
        return 90 + self._window_offset, 70 + self._window_offset

    def open_terminal(self) -> None:
        if self._terminal and self._terminal.winfo_exists():
            self._terminal.restore()
            return
        x, y = self._next_position()
        self._terminal = TerminalApp(self, x=x, y=y)

    def open_about(self) -> None:
        AboutApp(self)

    def open_settings(self) -> None:
        self.open_terminal()
        self.run_in_terminal("settings")

    def run_in_terminal(self, command: str) -> None:
        if not self._terminal or not self._terminal.winfo_exists():
            self.open_terminal()
        assert self._terminal is not None
        self._terminal.restore()
        self._terminal.run_command(command)

    def toggle_start_menu(self) -> None:
        if self._start_menu and self._start_menu.winfo_exists():
            self._start_menu.close()
            return
        self._start_menu = StartMenu(self)
        self.root.update_idletasks()
        bx = self.taskbar._start_btn.winfo_rootx()
        by = self.taskbar.winfo_rooty()
        self._start_menu.show_at(bx, by - 420)

    def shutdown(self) -> None:
        if messagebox.askyesno("Forge OS", "Shut down Forge OS?"):
            self.forge_os.shell.session.stop()
            self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()
