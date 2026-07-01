"""Forge OS boot entry point."""

import argparse
import sys

from rich.console import Console

from auth.login import AuthFlow
from kernel.kernel import Kernel
from filesystem.vfs import VirtualFileSystem
from users.users import UserManager
from packages.manager import PackageManager
from shell.banner import BootBanner, BootSequence
from shell.config import ShellConfig
from shell.shell import ForgeShell
from launcher import set_console_title
from desktop.icon import apply_window_icon
from desktop.gui.login import run_login


class ForgeOS:
    """Main Forge OS application."""

    VERSION = "2.0.0"

    def __init__(self, username: str | None = None, *, desktop: bool = False) -> None:
        self._desktop_mode = desktop
        self._config = ShellConfig(version=self.VERSION)
        if desktop:
            self._config.boot_animation = False
        self._console = Console(force_terminal=True, legacy_windows=False)
        self.banner = BootBanner(console=self._console, version=self.VERSION)
        self.boot_sequence = BootSequence(console=self._console)
        self.kernel = None
        self.vfs = None
        self.users = None
        self.packages = None
        self.shell = None
        self._username = username

        self._boot()

    def _boot(self) -> None:
        loaders = [
            (label, loader)
            for label, loader in (
                ("Kernel", self._load_kernel),
                ("Virtual Filesystem", self._load_filesystem),
                ("User Manager", self._load_users),
                ("Package Manager", self._load_packages),
                ("Shell", self._load_shell),
            )
        ]

        if self._config.boot_animation:
            self.boot_sequence.run(loaders)
        else:
            for _, loader in loaders:
                loader()

    def _load_kernel(self) -> None:
        self.kernel = Kernel()

    def _load_filesystem(self) -> None:
        self.vfs = VirtualFileSystem()
        if self._username:
            self.vfs.ensure_user_home(self._username)

    def _load_users(self) -> None:
        self.users = UserManager()
        if self._username:
            self.users.set_current_user(self._username)

    def _load_packages(self) -> None:
        self.packages = PackageManager()

    def _load_shell(self) -> None:
        self.shell = ForgeShell(
            kernel=self.kernel,
            filesystem=self.vfs,
            users=self.users,
            packages=self.packages,
            config=self._config,
            console=self._console,
            gui_mode=self._desktop_mode,
        )

    def run(self) -> None:
        if self._desktop_mode:
            from desktop.gui.app import ForgeDesktop

            ForgeDesktop(self).run()
            return

        self.banner.show_neofetch(
            kernel=self.kernel,
            users=self.users,
            packages=self.packages,
            session=self.shell.session,
        )
        self.shell.start()


def run_session() -> int:
    set_console_title("Forge OS")
    apply_window_icon()
    auth = AuthFlow()
    username = auth.authenticate()
    ForgeOS(username=username).run()
    return 0


def run_gui_session() -> int:
    print("Starting Forge OS desktop...", flush=True)
    try:
        username = run_login()

        if not username:
            print("Sign-in cancelled.", flush=True)
            return 0

        print(f"Welcome, {username}. Loading desktop...", flush=True)
        ForgeOS(username=username, desktop=True).run()
        print("Forge OS closed.", flush=True)
        return 0
    except Exception as error:
        import traceback

        print(f"Forge OS failed to start: {error}", flush=True)
        traceback.print_exc()
        try:
            from tkinter import messagebox

            messagebox.showerror("Forge OS", f"Failed to start:\n{error}")
        except Exception:
            pass
        return 1


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Forge OS boot entry point")
    parser.add_argument(
        "--session",
        action="store_true",
        help="Run in legacy full-screen terminal mode",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Run the Forge OS desktop window (default)",
    )
    args = parser.parse_args()

    if args.session:
        return run_session()

    return run_gui_session()


if __name__ == "__main__":
    raise SystemExit(main())
