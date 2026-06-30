"""Command dispatcher."""

from dataclasses import dataclass
from typing import Any

from shell.errors import CommandNotFoundError, ShellError
from shell.parser import CommandParser, ParsedCommand, ParseResult
from shell.pipes import PipeExecutor
from shell.registry import CommandRegistry
from shell.session import ShellSession


@dataclass
class DispatchResult:
    """Outcome of dispatching a parsed command."""

    output: str | None = None
    renderable: Any = None
    exit_code: int = 0
    should_exit: bool = False
    clear_screen: bool = False


class CommandDispatcher:
    """Routes parsed commands to registered handlers."""

    def __init__(
        self,
        registry: CommandRegistry,
        context: dict[str, Any],
        parser: CommandParser | None = None,
    ) -> None:
        self._registry = registry
        self._context = context
        self._parser = parser or CommandParser()
        self._pipe_executor = PipeExecutor()

    def dispatch(self, parse_result: ParseResult, session: ShellSession) -> DispatchResult:
        if not parse_result.commands:
            return DispatchResult()

        if self._pipe_executor.can_execute(parse_result):
            output = self._pipe_executor.execute(parse_result, self, session)
            return DispatchResult(output=output, exit_code=session.last_exit_code)

        return self.dispatch_single(parse_result.commands[0], session)

    def dispatch_single(
        self,
        command: ParsedCommand,
        session: ShellSession,
        stdin: str = "",
    ) -> DispatchResult:
        command = self._resolve_alias(command, session)
        command_class = self._registry.get(command.name)

        if command_class is None:
            error = CommandNotFoundError(command.name)
            session.last_exit_code = error.exit_code
            return DispatchResult(output=error.message, exit_code=error.exit_code)

        instance = command_class()
        context = {**self._context, "session": session, "stdin": stdin}

        try:
            result = instance.execute(command.args, context)
            session.last_exit_code = result.exit_code
            return DispatchResult(
                output=result.output,
                renderable=result.renderable,
                exit_code=result.exit_code,
                should_exit=result.should_exit,
                clear_screen=result.clear_screen,
            )
        except ShellError as error:
            session.last_exit_code = error.exit_code
            return DispatchResult(output=error.message, exit_code=error.exit_code)
        except Exception as error:
            session.last_exit_code = 1
            return DispatchResult(
                output=f"{command.name}: {error}",
                exit_code=1,
            )

    def _resolve_alias(self, command: ParsedCommand, session: ShellSession) -> ParsedCommand:
        expanded = session.aliases.expand(command.name, command.args)
        if expanded is None:
            return command
        parse_result = self._parser.parse(expanded)
        if not parse_result.commands:
            return command
        return parse_result.commands[0]
