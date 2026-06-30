"""Shell error types."""


class ShellError(Exception):
    """Base exception for shell operations."""

    def __init__(self, message: str, exit_code: int = 1) -> None:
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code


class CommandNotFoundError(ShellError):
    """Raised when a command is not registered."""

    def __init__(self, command: str) -> None:
        super().__init__(f"{command}: command not found", exit_code=127)
        self.command = command


class ParseError(ShellError):
    """Raised when input cannot be parsed."""

    def __init__(self, message: str) -> None:
        super().__init__(message, exit_code=2)


class CommandExecutionError(ShellError):
    """Raised when a command fails during execution."""

    def __init__(self, message: str, exit_code: int = 1) -> None:
        super().__init__(message, exit_code=exit_code)
