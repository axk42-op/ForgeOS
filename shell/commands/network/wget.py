"""Download a file (simulated)."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class WgetCommand(BaseCommand):
    name = "wget"
    category = "network"
    description = "Download a file from the web (simulated)"
    syntax = "wget URL"
    examples = ("wget https://forge.os/file.txt",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if not args:
            return CommandResult(output="wget: missing URL", exit_code=1)

        url = args[0]
        filename = url.rstrip("/").split("/")[-1] or "index.html"
        return CommandResult(
            output=(
                f"--{url}\n"
                f"Resolving forge.os... done.\n"
                f"Saving to: '{filename}'\n"
                f"Download complete (simulated)."
            )
        )
