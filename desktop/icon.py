"""Set Forge OS window icon from bundled assets."""

from __future__ import annotations

import sys
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def icon_paths() -> dict[str, Path]:
    bundled = Path(__file__).resolve().parent / "assets" / "icons"
    legacy = project_root() / "assets" / "icons"
    root = bundled if bundled.is_dir() else legacy
    return {
        "svg": root / "forge.svg",
        "ico": root / "forge.ico",
    }


def apply_window_icon() -> None:
    """Apply forge.ico to the console window on Windows."""
    if sys.platform != "win32":
        return

    ico = icon_paths()["ico"]
    if not ico.is_file():
        return

    try:
        import ctypes

        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if not hwnd:
            return

        IMAGE_ICON = 1
        LR_LOADFROMFILE = 0x00000010
        WM_SETICON = 0x0080
        ICON_SMALL = 0
        ICON_BIG = 1

        load_image = ctypes.windll.user32.LoadImageW
        load_image.argtypes = [
            ctypes.c_void_p,
            ctypes.c_wchar_p,
            ctypes.c_uint,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_uint,
        ]
        load_image.restype = ctypes.c_void_p

        send_message = ctypes.windll.user32.SendMessageW
        send_message.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint,
            ctypes.c_void_p,
            ctypes.c_void_p,
        ]
        send_message.restype = ctypes.c_void_p

        hicon = load_image(0, str(ico.resolve()), IMAGE_ICON, 0, 0, LR_LOADFROMFILE)
        if not hicon:
            return

        send_message(hwnd, WM_SETICON, ICON_BIG, hicon)
        send_message(hwnd, WM_SETICON, ICON_SMALL, hicon)
    except OSError:
        pass
