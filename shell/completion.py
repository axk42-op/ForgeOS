"""Command completion support (extensible for future autocomplete)."""

from shell.registry import CommandRegistry
from shell.session import ShellSession


class CompletionEngine:
    """Provides tab-completion candidates for shell input."""

    def __init__(self, registry: CommandRegistry) -> None:
        self._registry = registry

    def complete(self, text: str, session: ShellSession) -> list[str]:
        stripped = text.strip()
        if not stripped or " " not in stripped:
            return self._complete_command(stripped)
        return self._complete_arguments(stripped, session)

    def _complete_command(self, prefix: str) -> list[str]:
        return [name for name in self._registry.names() if name.startswith(prefix)]

    def _complete_arguments(self, text: str, session: ShellSession) -> list[str]:
        """Argument completion deferred to command-specific handlers."""
        return []
