"""Command input parser."""

from dataclasses import dataclass, field

from shell.errors import ParseError


@dataclass(frozen=True)
class ParsedCommand:
    """A single parsed command with its arguments."""

    name: str
    args: list[str]
    raw: str = ""


@dataclass(frozen=True)
class ParseResult:
    """Result of parsing a full input line.

    Designed for future pipe, redirect, and substitution support.
    """

    commands: list[ParsedCommand] = field(default_factory=list)
    raw_input: str = ""
    has_pipe: bool = False
    has_redirect: bool = False


class CommandParser:
    """Tokenizes shell input into structured commands.

    Current capabilities: basic whitespace splitting with quote awareness.
    Future: pipes, redirection, variables, command substitution.
    """

    def parse(self, line: str) -> ParseResult:
        stripped = line.strip()
        if not stripped:
            return ParseResult(raw_input=line)

        if self._contains_unquoted_pipe(stripped):
            return self._parse_pipeline(stripped)

        command = self._parse_single_command(stripped)
        return ParseResult(commands=[command], raw_input=line)

    def _contains_unquoted_pipe(self, line: str) -> bool:
        quote_char: str | None = None
        for char in line:
            if quote_char:
                if char == quote_char:
                    quote_char = None
                continue
            if char in ("'", '"'):
                quote_char = char
                continue
            if char == "|":
                return True
        return False

    def _parse_pipeline(self, line: str) -> ParseResult:
        segments = self._split_outside_quotes(line, "|")
        commands = [self._parse_single_command(segment.strip()) for segment in segments]
        return ParseResult(commands=commands, raw_input=line, has_pipe=True)

    def _split_outside_quotes(self, text: str, separator: str) -> list[str]:
        segments: list[str] = []
        current: list[str] = []
        quote_char: str | None = None
        index = 0

        while index < len(text):
            char = text[index]

            if quote_char:
                current.append(char)
                if char == quote_char:
                    quote_char = None
                index += 1
                continue

            if char in ("'", '"'):
                quote_char = char
                current.append(char)
                index += 1
                continue

            if text.startswith(separator, index):
                segments.append("".join(current))
                current = []
                index += len(separator)
                continue

            current.append(char)
            index += 1

        segments.append("".join(current))
        return segments

    def _parse_single_command(self, segment: str) -> ParsedCommand:
        tokens = self._tokenize(segment)
        if not tokens:
            raise ParseError("empty command")

        name = tokens[0]
        args = tokens[1:]
        return ParsedCommand(name=name, args=args, raw=segment)

    def _tokenize(self, text: str) -> list[str]:
        """Split input respecting single and double quotes."""
        tokens: list[str] = []
        current: list[str] = []
        quote_char: str | None = None
        index = 0

        while index < len(text):
            char = text[index]

            if quote_char:
                if char == quote_char:
                    quote_char = None
                else:
                    current.append(char)
                index += 1
                continue

            if char in ("'", '"'):
                quote_char = char
                index += 1
                continue

            if char.isspace():
                if current:
                    tokens.append("".join(current))
                    current = []
                index += 1
                continue

            if char == "\\" and index + 1 < len(text):
                current.append(text[index + 1])
                index += 2
                continue

            current.append(char)
            index += 1

        if quote_char:
            raise ParseError(f"unmatched quote: {quote_char}")

        if current:
            tokens.append("".join(current))

        return tokens
