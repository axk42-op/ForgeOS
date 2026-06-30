"""Base command class and result type."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, ClassVar


@dataclass
class CommandResult:
    """Return value from command execution."""

    output: str | None = None
    renderable: Any = None
    exit_code: int = 0
    should_exit: bool = False
    clear_screen: bool = False
    data: dict[str, Any] = field(default_factory=dict)


class BaseCommand(ABC):
    """Abstract base for all shell commands."""

    name: ClassVar[str] = ""
    category: ClassVar[str] = "general"
    aliases: ClassVar[tuple[str, ...]] = ()
    description: ClassVar[str] = ""
    syntax: ClassVar[str] = ""
    examples: ClassVar[tuple[str, ...]] = ()

    @abstractmethod
    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        """Execute the command with parsed arguments and runtime context."""

    def help_text(self) -> str:
        lines = [
            f"[bold cyan]{self.name}[/bold cyan] — {self.description}",
            "",
            f"[bold]Syntax:[/bold] {self.syntax or self.name}",
        ]
        if self.examples:
            lines.append("")
            lines.append("[bold]Examples:[/bold]")
            for example in self.examples:
                lines.append(f"  {example}")
        return "\n".join(lines)
