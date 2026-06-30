"""Display user identity."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class IdCommand(BaseCommand):
    name = "id"
    category = "user"
    description = "Display user and group identity"
    syntax = "id [USER]"
    examples = ("id",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        users = context["users"]
        username = args[0] if args else users.whoami()
        record = users.get_user(username) or users.ensure_user(username)
        return CommandResult(
            output=(
                f"uid={record['uid']}({username}) "
                f"gid={record['gid']}({username}) "
                f"groups={record['gid']}({username})"
            )
        )
