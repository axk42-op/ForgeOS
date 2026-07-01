"""Launch Forge OS in a dedicated window."""

import os
import subprocess
import sys
from pathlib import Path


def set_console_title(title: str = "Forge OS") -> None:
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
    """Open the Forge OS desktop in a new process."""
    root = project_root()
    script = boot_script()
    python = sys.executable

    env = os.environ.copy()
    env["FORGEOS_SESSION"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    cmd = [python, str(script), "--gui"]
    subprocess.Popen(cmd, cwd=root, env=env)
    return 0
