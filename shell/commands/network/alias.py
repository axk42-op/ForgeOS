"""Manage command aliases."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class AliasCommand(BaseCommand):
    name = "alias"
    category = "network"
    description = "Manage command aliases"
    syntax = "alias [NAME[=VALUE]]"
    examples = (
        "alias",
        "alias ll=ls",
    )

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        session = context["session"]

        if not args:
            lines = [f"alias {name}='{value}'" for name, value in session.aliases.items()]
            return CommandResult(output="\n".join(lines) if lines else "No aliases defined.")

        for arg in args:
            if "=" not in arg:
                value = session.aliases.get(arg)
                if value is None:
                    return CommandResult(output=f"alias: {arg}: not found", exit_code=1)
                return CommandResult(output=f"alias {arg}='{value}'")

            name, value = arg.split("=", 1)
            session.aliases.set(name.strip(), value.strip())

        return CommandResult()
