"""Credential store interface."""

from dataclasses import dataclass
from typing import Protocol


@dataclass
class StoredCredentials:
    username: str
    password_hash: str
    salt: str


class CredentialBackend(Protocol):
    """Backend for Forge OS user credentials."""

    def has_users(self) -> bool:
        """Return True if at least one account exists."""

    def user_exists(self, username: str) -> bool:
        """Return True if the username is registered."""

    def load(self, username: str | None = None) -> StoredCredentials | None:
        """Load credentials for a username (or default/local user)."""

    def register(self, username: str, password: str) -> StoredCredentials:
        """Create a new account."""

    def verify(self, username: str, password: str) -> bool:
        """Verify username and password."""

    def update_password(self, username: str, current_password: str, new_password: str) -> bool:
        """Change password for an account."""

    def remember_username(self, username: str) -> None:
        """Cache last signed-in username for prompts."""

    def last_username(self) -> str | None:
        """Return cached username hint, if any."""
