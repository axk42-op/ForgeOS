"""Future pipe execution support."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from shell.parser import ParseResult
from shell.session import ShellSession

if TYPE_CHECKING:
    from shell.dispatcher import CommandDispatcher


@dataclass
class PipeContext:
    """Carries stdin/stdout between piped commands."""

    stdin: str = ""
    stdout: str = ""


class PipeExecutor:
    """Executes piped command chains."""

    def can_execute(self, parse_result: ParseResult) -> bool:
        return parse_result.has_pipe and len(parse_result.commands) > 1

    def execute(
        self,
        parse_result: ParseResult,
        dispatcher: "CommandDispatcher",
        session: ShellSession,
    ) -> str:
        """Run commands in sequence, passing output as input."""
        output = ""
        for command in parse_result.commands:
            result = dispatcher.dispatch_single(command, session, stdin=output)
            output = result.output or ""
        return output
