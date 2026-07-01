"""Taskbar and Start menu definitions — each item runs a real shell command."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MenuItem:
    command: str
    label: str


START_MENU: tuple[MenuItem, ...] = (
    MenuItem("help", "Help — all commands"),
    MenuItem("search", "Search commands"),
    MenuItem("forgefetch", "System information"),
    MenuItem("logo", "Forge logo"),
    MenuItem("calc", "Calculator"),
    MenuItem("docs", "Documentation (browser)"),
    MenuItem("source", "Source code (GitHub)"),
    MenuItem("clear", "Clear screen"),
    MenuItem("shutdown", "Shut down Forge OS"),
)

FILE_MENU: tuple[MenuItem, ...] = (
    MenuItem("pwd", "Print working directory"),
    MenuItem("ls", "List files"),
    MenuItem("tree", "Directory tree"),
    MenuItem("touch notes.txt", "Create notes.txt"),
    MenuItem("find .", "Find files here"),
    MenuItem("mv", "Move files — usage: mv SRC DST"),
    MenuItem("rm", "Remove files — usage: rm FILE"),
)

VIEW_MENU: tuple[MenuItem, ...] = (
    MenuItem("clear", "Clear screen"),
    MenuItem("cls", "Clear screen (alias)"),
    MenuItem("forgefetch", "System information"),
    MenuItem("logo", "Show logo"),
    MenuItem("date", "Today's date"),
    MenuItem("time", "Current time"),
    MenuItem("uptime", "Session uptime"),
    MenuItem("free", "Memory usage"),
    MenuItem("df", "Disk usage"),
)

TERMINAL_MENU: tuple[MenuItem, ...] = (
    MenuItem("history", "Command history"),
    MenuItem("alias", "List aliases"),
    MenuItem("env", "Environment variables"),
    MenuItem("whoami", "Current user"),
    MenuItem("hostname", "Host name"),
    MenuItem("version", "Forge OS version"),
    MenuItem("uname", "Kernel info"),
)

HELP_MENU: tuple[MenuItem, ...] = (
    MenuItem("help", "Command reference"),
    MenuItem("search", "Search commands"),
    MenuItem("docs", "Wiki documentation"),
    MenuItem("source", "GitHub repository"),
    MenuItem("disclaimer", "Privacy & storage"),
    MenuItem("about", "About Forge OS"),
    MenuItem("license", "License"),
    MenuItem("authors", "Authors"),
)

SETTINGS_MENU: tuple[MenuItem, ...] = (
    MenuItem("passwd", "Change password"),
    MenuItem("env", "Environment"),
    MenuItem("alias", "Aliases"),
    MenuItem("logout", "Sign out"),
    MenuItem("disclaimer", "Local storage info"),
)

MENUS: dict[str, tuple[MenuItem, ...]] = {
    "start": START_MENU,
    "file": FILE_MENU,
    "view": VIEW_MENU,
    "terminal": TERMINAL_MENU,
    "help": HELP_MENU,
    "settings": SETTINGS_MENU,
}

MENU_LABELS: dict[str, str] = {
    "start": "Start",
    "file": "File",
    "view": "View",
    "terminal": "Terminal",
    "help": "Help",
    "settings": "Settings",
}
