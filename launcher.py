"""Launch Forge OS in a dedicated terminal window."""

import os
import subprocess
import sys
from pathlib import Path


def set_console_title(title: str = "ForgeOS") -> None:
    """Set the current terminal window title."""
    if sys.platform == "win32":
        try:
            import ctypes

            ctypes.windll.kernel32.SetConsoleTitleW(title)
        except OSError:
            pass
    else:
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()


def project_root() -> Path:
    return Path(__file__).resolve().parent


def boot_script() -> Path:
    return project_root() / "boot.py"


def should_spawn_window() -> bool:
    return os.environ.get("FORGEOS_SESSION") != "1"


def spawn_forgeos_window() -> int:
    """Open a new terminal window titled ForgeOS and return immediately."""
    root = project_root()
    script = boot_script()
    python = sys.executable

    env = os.environ.copy()
    env["FORGEOS_SESSION"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    if sys.platform == "win32":
        command = (
            f'start "ForgeOS" cmd /k "cd /d "{root}" && '
            f'set FORGEOS_SESSION=1&& set PYTHONIOENCODING=utf-8&& '
            f'"{python}" "{script}" --session"'
        )
        subprocess.Popen(command, shell=True, cwd=root)
        return 0

    if sys.platform == "darwin":
        command = (
            f'cd "{root}" && FORGEOS_SESSION=1 PYTHONIOENCODING=utf-8 '
            f'"{python}" "{script}" --session; exec bash'
        )
        subprocess.Popen(["osascript", "-e", f'tell app "Terminal" to do script "{command}"'])
        return 0

    terminals = [
        ["gnome-terminal", "--title=ForgeOS", "--", python, str(script), "--session"],
        ["xterm", "-T", "ForgeOS", "-e", python, str(script), "--session"],
        ["konsole", "--title", "ForgeOS", "-e", python, str(script), "--session"],
    ]
    for terminal_cmd in terminals:
        try:
            subprocess.Popen(terminal_cmd, cwd=root, env=env)
            return 0
        except FileNotFoundError:
            continue

    env["FORGEOS_SESSION"] = "1"
    os.execve(python, [python, str(script), "--session"], env)
    return 0
