"""Neofetch-style system info layout for Forge OS."""

from __future__ import annotations

from typing import Any

import psutil
from rich.text import Text

from shell.ui.branding import (
    BLOCK_STYLE,
    FORGE_LOGO,
    FORGE_SIG,
    HEADER_STYLE,
    LABEL_STYLE,
    PALETTE,
    SIG_STYLE,
    VALUE_STYLE,
)


def _pad(lines: list[str], height: int) -> list[str]:
    if len(lines) >= height:
        return lines
    return lines + [""] * (height - len(lines))


def build_neofetch(
    *,
    kernel: Any,
    users: Any,
    packages: Any,
    session: Any,
) -> Text:
    """Compact sig on the left; block logo + system info on the right."""
    username = users.whoami()
    hostname = users.hostname
    version = session.environment.get("FORGE_VERSION", kernel.version)
    mem = psutil.virtual_memory()
    used_mb = mem.used // (1024 * 1024)
    total_mb = mem.total // (1024 * 1024)

    sig = FORGE_SIG.rstrip("\n").split("\n")
    block = FORGE_LOGO.rstrip("\n").split("\n")

    header = f"{username}@{hostname}"
    separator = "─" * len(header)
    fields = [
        ("OS", f"Forge OS {version}"),
        ("Host", hostname),
        ("Kernel", f"{kernel.name} {kernel.version}"),
        ("Uptime", kernel.uptime()),
        ("Packages", f"{len(packages.list_packages())} (forgepkg)"),
        ("Shell", "forge"),
        ("User", username),
        ("Memory", f"{used_mb}MiB / {total_mb}MiB"),
        ("CWD", session.cwd),
    ]

    palette = "".join(f"[{color}]██[/]" for color, _ in PALETTE)
    palette_names = " ".join(name.center(2) for _, name in PALETTE)

    right_rows: list[tuple[str, str]] = []
    for line in block:
        right_rows.append((line, BLOCK_STYLE))
    right_rows.append(("", ""))
    right_rows.append((header, HEADER_STYLE))
    right_rows.append((separator, HEADER_STYLE))
    for label, value in fields:
        right_rows.append((f"{label}: {value}", "field"))
    right_rows.append(("", ""))
    right_rows.append((palette, "palette"))
    right_rows.append((palette_names, "dim"))

    height = max(len(sig), len(right_rows))
    sig = _pad(sig, height)
    left_width = max(len(line) for line in sig)
    gap = 4
    output = Text()

    for row in range(height):
        if row:
            output.append("\n")
        output.append(sig[row].ljust(left_width), style=SIG_STYLE)
        output.append(" " * gap)

        if row >= len(right_rows):
            continue

        text, style = right_rows[row]
        if style == BLOCK_STYLE:
            output.append(text, style=BLOCK_STYLE)
        elif style == HEADER_STYLE:
            output.append(text, style=HEADER_STYLE)
        elif style == "field":
            label, value = text.split(": ", 1)
            output.append(label + ":", style=LABEL_STYLE)
            output.append(" " + value, style=VALUE_STYLE)
        elif style == "palette":
            output.append(Text.from_markup(text))
        elif style == "dim":
            output.append(text, style="dim")

    return output
