"""GUI login and registration for Forge OS."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from auth.factory import get_credential_store
from desktop.gui import theme as T
from desktop.icon import icon_paths


class LoginWindow(tk.Tk):
    """Standalone sign-in window (uses mainloop — reliable on Windows)."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Forge OS — Sign In")
        self.configure(bg=T.BG_WINDOW)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._cancel)

        self.result: str | None = None
        self._store = get_credential_store()
        self._first_run = not self._store.has_users()

        self._set_icon()
        self._build()
        self._center_on_screen()
        self.lift()
        self.attributes("-topmost", True)
        self.after(300, lambda: self.attributes("-topmost", False))
        self.focus_force()

    def _set_icon(self) -> None:
        ico = icon_paths().get("ico")
        if ico and ico.is_file():
            try:
                self.iconbitmap(str(ico.resolve()))
            except tk.TclError:
                pass

    def _cancel(self) -> None:
        self.result = None
        self.quit()

    def _center_on_screen(self) -> None:
        self.update_idletasks()
        width = 420
        height = 320 if self._first_run else 280
        x = max(0, (self.winfo_screenwidth() - width) // 2)
        y = max(0, (self.winfo_screenheight() - height) // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _build(self) -> None:
        frame = tk.Frame(self, bg=T.BG_WINDOW, padx=24, pady=20)
        frame.pack(fill="both", expand=True)

        title = "Create your account" if self._first_run else "Sign in to continue"
        tk.Label(frame, text=title, font=("Segoe UI", 14, "bold"), fg=T.ACCENT, bg=T.BG_WINDOW).pack(
            anchor="w"
        )
        tk.Label(
            frame,
            text="Credentials are stored locally on this machine.",
            font=T.FONT_UI,
            fg=T.FG_DIM,
            bg=T.BG_WINDOW,
        ).pack(anchor="w", pady=(4, 16))

        hint = self._store.last_username()
        if hint and not self._first_run:
            tk.Label(
                frame,
                text=f"Last signed in: {hint}",
                font=T.FONT_UI,
                fg=T.ACCENT_BLUE,
                bg=T.BG_WINDOW,
            ).pack(anchor="w", pady=(0, 8))

        tk.Label(frame, text="Username", font=T.FONT_UI, fg=T.FG_TEXT, bg=T.BG_WINDOW).pack(anchor="w")
        self._user = ttk.Entry(frame, width=40)
        self._user.pack(fill="x", pady=(2, 10))
        if hint and not self._first_run:
            self._user.insert(0, hint)

        tk.Label(frame, text="Password", font=T.FONT_UI, fg=T.FG_TEXT, bg=T.BG_WINDOW).pack(anchor="w")
        self._pass = ttk.Entry(frame, width=40, show="•")
        self._pass.pack(fill="x", pady=(2, 10))

        if self._first_run:
            tk.Label(frame, text="Confirm password", font=T.FONT_UI, fg=T.FG_TEXT, bg=T.BG_WINDOW).pack(anchor="w")
            self._confirm = ttk.Entry(frame, width=40, show="•")
            self._confirm.pack(fill="x", pady=(2, 10))
        else:
            self._confirm = None

        btn_row = tk.Frame(frame, bg=T.BG_WINDOW)
        btn_row.pack(fill="x", pady=(12, 0))
        ttk.Button(btn_row, text="Continue", command=self._submit).pack(side="right")
        self._pass.bind("<Return>", lambda _e: self._submit())
        self._user.focus_set()

    def _submit(self) -> None:
        username = self._user.get().strip()
        password = self._pass.get()

        if not username:
            messagebox.showerror("Forge OS", "Username cannot be empty.", parent=self)
            return

        if self._first_run:
            confirm = self._confirm.get() if self._confirm else ""
            if password != confirm:
                messagebox.showerror("Forge OS", "Passwords do not match.", parent=self)
                return
            try:
                record = self._store.register(username, password)
                self._store.remember_username(record.username)
                self._done(record.username)
            except ValueError as error:
                messagebox.showerror("Forge OS", str(error), parent=self)
            except Exception as error:
                messagebox.showerror("Forge OS", f"Registration failed: {error}", parent=self)
            return

        if self._store.verify(username, password):
            self._store.remember_username(username)
            self._done(username)
        else:
            messagebox.showerror("Forge OS", "Invalid credentials.", parent=self)

    def _done(self, username: str) -> None:
        self.result = username
        self.quit()


def run_login() -> str | None:
    """Show login window and return username, or None if cancelled."""
    window = LoginWindow()
    window.mainloop()
    window.destroy()
    return window.result


# Backwards compatibility
LoginDialog = LoginWindow
