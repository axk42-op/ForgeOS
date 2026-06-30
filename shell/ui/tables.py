"""Rich table utilities."""

from rich.table import Table


class ForgeTable:
    """Styled table builder for command output."""

    def __init__(self, title: str = "", show_header: bool = True) -> None:
        self._table = Table(title=title, show_header=show_header, header_style="bold cyan")
        self._columns: list[str] = []

    def add_column(self, name: str, style: str = "") -> "ForgeTable":
        self._table.add_column(name, style=style)
        self._columns.append(name)
        return self

    def add_row(self, *values: str) -> "ForgeTable":
        self._table.add_row(*values)
        return self

    def render(self) -> Table:
        return self._table
