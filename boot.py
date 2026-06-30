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
from launcher import set_console_title, should_spawn_window, spawn_forgeos_window


class ForgeOS:
    """Main Forge OS application."""

    VERSION = "1.0.0"

    def __init__(self, username: str | None = None) -> None:
        self._config = ShellConfig(version=self.VERSION)
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
        self.banner.show_logo()

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
        )

    def run(self) -> None:
        self.banner.show_welcome_panel()
        self.shell.start()


def run_session() -> int:
    set_console_title("ForgeOS")
    auth = AuthFlow()
    username = auth.authenticate()
    ForgeOS(username=username).run()
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Forge OS boot entry point")
    parser.add_argument(
        "--session",
        action="store_true",
        help="Run inside the ForgeOS terminal session (skip window spawn)",
    )
    args = parser.parse_args()

    if args.session or not should_spawn_window():
        return run_session()

    spawn_forgeos_window()
    print("Opening ForgeOS window...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
