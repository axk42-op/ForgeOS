"""Run shell commands from desktop menus."""

from __future__ import annotations

from typing import Any

from shell.commands.base import CommandResult
from shell.parser import CommandParser


def run_shell_line(line: str, context: dict[str, Any]) -> CommandResult:
    """Parse and dispatch a command line through the active shell."""
    session = context["session"]
    dispatcher = context.get("dispatcher")
    if dispatcher is None:
        return CommandResult(output="desktop: shell dispatcher unavailable", exit_code=1)

    parse_result = CommandParser().parse(line)
    if not parse_result.commands:
        return CommandResult()

    dispatch_result = dispatcher.dispatch(parse_result, session)
    return CommandResult(
        output=dispatch_result.output,
        renderable=dispatch_result.renderable,
        exit_code=dispatch_result.exit_code,
        should_exit=dispatch_result.should_exit,
        clear_screen=dispatch_result.clear_screen,
    )
