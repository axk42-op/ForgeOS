"""Forge Terminal — shell running inside a desktop window."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING

import tkinter as tk
from tkinter import ttk

from desktop.gui import theme as T
from desktop.gui.text_console import TextConsole
from desktop.gui.window_manager import ManagedWindow

if TYPE_CHECKING:
    from desktop.gui.app import ForgeDesktop


class ShellInputBridge:
    """Blocks the shell thread until the user submits a line from the GUI."""

    def __init__(
        self,
        root: tk.Mk,
        prompt_var: tk.StringVar,
        entry: ttk.Entry,
        echo: callable,
    ) -> None:
        self._root = root
        self._prompt_var = prompt_var
        self._entry = entry
        self._echo = echo
        self._event = threading.Event()
        self._value = ""
        self._waiting = False
        self._pending: list[str] = []

    def queue_command(self, command: str) -> None:
        def inject() -> None:
            if self._waiting:
                self._value = command
                self._echo(f"{self._prompt_var.get()}{command}\n")
                self._entry.delete(0, "end")
                self._event.set()
            else:
                self._pending.append(command)

        self._root.after(0, inject)

    def read_line(self, prompt: str) -> str:
        if self._pending:
            return self._pending.pop(0)

        self._event.clear()
        self._waiting = True
        ready = threading.Event()

        def show_prompt() -> None:
            self._prompt_var.set(prompt)
            self._entry.delete(0, "end")
            self._entry.focus_set()
            ready.set()

        self._root.after(0, show_prompt)
        ready.wait()
        self._event.wait()
        self._waiting = False
        return self._value

    def submit(self, prompt: str) -> None:
        text = self._entry.get()
        self._value = text
        self._echo(f"{prompt}{text}\n")
        self._entry.delete(0, "end")
        self._event.set()


class TerminalApp(ManagedWindow):
    """Terminal emulator window hosting Forge Shell."""

    def __init__(self, desktop: ForgeDesktop, *, x: int = 100, y: int = 70) -> None:
        super().__init__(
            desktop,
            "Terminal",
            width=860,
            height=540,
            x=x,
            y=y,
            on_close=self._on_close,
        )
        self._desktop = desktop
        self._forge_os = desktop.forge_os
        self._shell_thread: threading.Thread | None = None
        self._input_bridge: ShellInputBridge | None = None
        self._text_console: TextConsole | None = None
        self._build()
        self._start_shell()

    def _build(self) -> None:
        self._text = tk.Text(
            self.content,
            bg=T.BG_INPUT,
            fg="#c9d1d9",
            insertbackground="#58a6ff",
            font=T.FONT_MONO,
            wrap="word",
            bd=0,
            highlightthickness=0,
            state="disabled",
        )
        self._text.pack(fill="both", expand=True, padx=2, pady=2)
        self._text.tag_configure("error", foreground="#f85149")

        input_row = tk.Frame(self.content, bg=T.BG_WINDOW)
        input_row.pack(fill="x", padx=4, pady=4)

        self._prompt_var = tk.StringVar(value="")
        self._prompt_label = tk.Label(
            input_row,
            textvariable=self._prompt_var,
            font=T.FONT_MONO,
            fg="#58a6ff",
            bg=T.BG_WINDOW,
        )
        self._prompt_label.pack(side="left")

        self._entry = ttk.Entry(input_row, font=T.FONT_MONO)
        self._entry.pack(side="left", fill="x", expand=True, padx=(4, 0))
        self._entry.bind("<Return>", lambda _e: self._submit())
        self._entry.focus_set()

    def _submit(self) -> None:
        if self._input_bridge:
            self._input_bridge.submit(self._prompt_var.get())

    def run_command(self, command: str) -> None:
        if self._input_bridge:
            self._input_bridge.queue_command(command)

    def _start_shell(self) -> None:
        self._text_console = TextConsole(self._text, self._desktop.root, width=96)
        shell = self._forge_os.shell

        shell.attach_gui_console(self._text_console.console)
        shell.set_gui_mode(True)
        shell.set_gui_clear(self._text_console.clear)

        self._input_bridge = ShellInputBridge(
            self._desktop.root,
            self._prompt_var,
            self._entry,
            self._text_console.append,
        )

        self._shell_thread = threading.Thread(target=self._run_shell, daemon=True)
        self._shell_thread.start()

    def _run_shell(self) -> None:
        assert self._text_console is not None
        assert self._input_bridge is not None
        shell = self._forge_os.shell

        banner = self._forge_os.banner.build_neofetch_text(
            kernel=self._forge_os.kernel,
            users=self._forge_os.users,
            packages=self._forge_os.packages,
            session=shell.session,
        )
        self._text_console.append(banner)
        self._text_console.append("\nForge OS Terminal ready. Type help and press Enter.\n\n")

        try:
            shell.start_gui(self._input_bridge.read_line)
        except Exception as error:
            self._text_console.append(f"\nTerminal error: {error}\n", "error")

    def _on_close(self) -> None:
        if self._forge_os.shell.session.running:
            self._forge_os.shell.session.stop()
