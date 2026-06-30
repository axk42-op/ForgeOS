"""User management for Forge OS."""


class UserManager:
    """Manages virtual user accounts."""

    def __init__(self) -> None:
        self._current_user = "forge"
        self._hostname = "localhost"
        self._users: dict[str, dict] = {}

    @property
    def current_user(self) -> str:
        return self._current_user

    @property
    def hostname(self) -> str:
        return self._hostname

    def whoami(self) -> str:
        return self._current_user

    def set_current_user(self, username: str) -> None:
        self._current_user = username
        self.ensure_user(username)

    def ensure_user(self, username: str) -> dict:
        if username not in self._users:
            self._users[username] = {
                "uid": 1000 + len(self._users),
                "gid": 1000,
                "home": f"/home/{username}",
                "shell": "/bin/forge",
                "full_name": username.replace("_", " ").title(),
            }
        return self._users[username]

    def get_user(self, username: str) -> dict | None:
        return self._users.get(username)

    def info(self) -> dict[str, str]:
        user = self.ensure_user(self._current_user)
        return {
            "username": self._current_user,
            "hostname": self._hostname,
            "home": user["home"],
            "shell": user["shell"],
            "full_name": user["full_name"],
        }
