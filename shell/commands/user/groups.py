"""Display group membership."""

from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class GroupsCommand(BaseCommand):
    name = "groups"
    category = "user"
    description = "Display group membership"
    syntax = "groups [USER]"
    examples = ("groups",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        users = context["users"]
        username = args[0] if args else users.whoami()
        record = users.get_user(username) or users.ensure_user(username)
        return CommandResult(output=f"{username} : {record['gid']}({username})")
