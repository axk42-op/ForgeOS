"""Forge package manager (placeholder)."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult
from shell.ui.tables import ForgeTable


class ForgepkgCommand(BaseCommand):
    name = "forgepkg"
    category = "developer"
    description = "Forge package manager (placeholder)"
    syntax = "forgepkg [list|info|install]"
    examples = ("forgepkg list", "forgepkg install mypkg")

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        packages = context["packages"]
        subcommand = args[0] if args else "list"

        if subcommand == "list":
            table = ForgeTable(title="Installed Packages")
            table.add_column("Package", style="cyan")
            table.add_column("Version", style="green")
            table.add_column("Description")
            for name, meta in packages.list_packages().items():
                table.add_row(name, meta["version"], meta["description"])
            return CommandResult(renderable=table.render())

        if subcommand == "info":
            info = packages.info()
            lines = [f"{key}: {value}" for key, value in info.items()]
            return CommandResult(output="\n".join(lines))

        if subcommand == "install":
            if len(args) < 2:
                return CommandResult(
                    output="forgepkg install: missing package name",
                    exit_code=1,
                )
            package_name = args[1]
            if not packages.install_package(package_name):
                return CommandResult(
                    output=f"forgepkg: package '{package_name}' is already installed",
                    exit_code=1,
                )
            return CommandResult(output=f"Installed package '{package_name}'.")

        return CommandResult(
            output=f"forgepkg: unknown command '{subcommand}'. Try 'list', 'info', or 'install'.",
            exit_code=1,
        )
