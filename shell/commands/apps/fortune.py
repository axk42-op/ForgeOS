"""Display a random fortune."""

import random
from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.panels import ForgePanel


FORTUNES = (
    "A bug in the hand is better than one as yet undetected.",
    "Real operating systems have kernels. Forge OS has Python.",
    "There is no place like /home.",
    "Give a developer a shell, and they will automate the world.",
    "The best code is no code at all — but we wrote all of this anyway.",
    "May your pipes never leak and your redirects always land.",
)


class FortuneCommand(BaseCommand):
    name = "fortune"
    category = "apps"
    description = "Display a random fortune"
    syntax = "fortune"
    examples = ("fortune",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        quote = random.choice(FORTUNES)
        panel = ForgePanel(quote, title="Fortune", border_style="magenta")
        return CommandResult(renderable=panel.render())
