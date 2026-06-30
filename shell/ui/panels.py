"""Rich panel wrappers."""

from rich.panel import Panel
from rich.text import Text


class ForgePanel:
    """Styled panel for Forge OS output."""

    def __init__(
        self,
        content: str,
        title: str = "",
        border_style: str = "cyan",
        expand: bool = False,
    ) -> None:
        self._content = content
        self._title = title
        self._border_style = border_style
        self._expand = expand

    def render(self) -> Panel:
        return Panel(
            Text.from_markup(self._content),
            title=self._title,
            border_style=self._border_style,
            expand=self._expand,
        )
