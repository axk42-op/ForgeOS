"""Shell configuration."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ShellConfig:
    """Runtime configuration for Forge Shell."""

    version: str = "1.0.0"
    prompt_symbol: str = "$"
    history_max_entries: int = 1000
    enable_completion: bool = True
    enable_syntax_highlighting: bool = True
    theme: str = "default"
    boot_animation: bool = True
    extra: dict[str, Any] = field(default_factory=dict)
