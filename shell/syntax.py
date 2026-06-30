"""Syntax highlighting and shell scripting support (future)."""

from dataclasses import dataclass


@dataclass
class SyntaxToken:
    """A token with syntax classification."""

    text: str
    token_type: str


class SyntaxHighlighter:
    """Provides syntax highlighting for shell input. Extensible for scripting."""

    KEYWORDS = frozenset({"if", "then", "else", "fi", "for", "do", "done", "while"})

    def highlight(self, text: str) -> list[SyntaxToken]:
        tokens: list[SyntaxToken] = []
        for part in text.split():
            if part in self.KEYWORDS:
                tokens.append(SyntaxToken(part, "keyword"))
            elif part.startswith("$"):
                tokens.append(SyntaxToken(part, "variable"))
            elif part in ("|", ">", ">>", "<", "&&", "||"):
                tokens.append(SyntaxToken(part, "operator"))
            else:
                tokens.append(SyntaxToken(part, "word"))
        return tokens
