"""Change Forge OS password."""

from getpass import getpass
from typing import Any

from auth.factory import get_credential_store
from shell.commands.base import BaseCommand, CommandResult


class PasswdCommand(BaseCommand):
    name = "passwd"
    category = "user"
    description = "Change your Forge OS password"
    syntax = "passwd"
    examples = ("passwd",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        store = get_credential_store()
        username = context["users"].whoami()

        if not store.user_exists(username):
            return CommandResult(output="passwd: no account configured for this user", exit_code=1)

        current = getpass("Current password: ")
        new_password = getpass("New password: ")
        confirm = getpass("Confirm new password: ")

        if new_password != confirm:
            return CommandResult(output="passwd: passwords do not match", exit_code=1)

        try:
            if not store.update_password(username, current, new_password):
                return CommandResult(output="passwd: incorrect current password", exit_code=1)
        except ValueError as error:
            return CommandResult(output=f"passwd: {error}", exit_code=1)
        except Exception as error:
            return CommandResult(output=f"passwd: {error}", exit_code=1)

        return CommandResult(output="Password updated successfully.")
