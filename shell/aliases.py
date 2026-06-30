"""Shell alias management."""

from collections.abc import Iterator


class AliasManager:
    """Maps alias names to replacement command strings."""

    def __init__(self) -> None:
        self._aliases: dict[str, str] = {}

    def set(self, name: str, value: str) -> None:
        self._aliases[name] = value

    def get(self, name: str) -> str | None:
        return self._aliases.get(name)

    def remove(self, name: str) -> bool:
        return self._aliases.pop(name, None) is not None

    def resolve(self, command: str) -> str:
        """Return alias expansion or the original command name."""
        return self._aliases.get(command, command)

    def expand(self, command: str, args: list[str]) -> str | None:
        """Return full expanded command line if an alias exists, else None."""
        alias_value = self._aliases.get(command)
        if alias_value is None:
            return None
        if args:
            return f"{alias_value} {' '.join(args)}"
        return alias_value

    def items(self) -> Iterator[tuple[str, str]]:
        return iter(self._aliases.items())

    def as_dict(self) -> dict[str, str]:
        return dict(self._aliases)
