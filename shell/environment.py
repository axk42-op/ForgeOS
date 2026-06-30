"""Shell environment variable management."""

import re
from collections.abc import Iterator


class Environment:
    """Manages shell environment variables."""

    def __init__(self, initial: dict[str, str] | None = None) -> None:
        self._vars: dict[str, str] = dict(initial or {})

    def get(self, key: str, default: str | None = None) -> str | None:
        return self._vars.get(key, default)

    def set(self, key: str, value: str) -> None:
        self._vars[key] = value

    def unset(self, key: str) -> None:
        self._vars.pop(key, None)

    def has(self, key: str) -> bool:
        return key in self._vars

    def items(self) -> Iterator[tuple[str, str]]:
        return iter(self._vars.items())

    def as_dict(self) -> dict[str, str]:
        return dict(self._vars)

    def update(self, values: dict[str, str]) -> None:
        self._vars.update(values)

    def expand(self, text: str) -> str:
        """Expand $VAR and ${VAR} references."""
        result = text
        for key in sorted(self._vars, key=len, reverse=True):
            value = self._vars[key]
            result = result.replace(f"${{{key}}}", value)
        for key in sorted(self._vars, key=len, reverse=True):
            value = self._vars[key]
            result = re.sub(rf"(?<!\w)\${re.escape(key)}(?!\w)", value, result)
        return result
