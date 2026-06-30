"""Future redirection support."""

from dataclasses import dataclass
from enum import Enum


class RedirectType(Enum):
    """Supported redirection modes."""

    STDOUT = ">"
    STDOUT_APPEND = ">>"
    STDERR = "2>"
    STDIN = "<"


@dataclass(frozen=True)
class RedirectSpec:
    """Describes a single redirection operation."""

    redirect_type: RedirectType
    target: str


class RedirectParser:
    """Parses and applies I/O redirection. Full implementation deferred."""

    def parse(self, tokens: list[str]) -> tuple[list[str], list[RedirectSpec]]:
        return tokens, []

    def apply(self, output: str, redirects: list[RedirectSpec]) -> str:
        return output
