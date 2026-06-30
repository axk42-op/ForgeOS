"""Shell session state."""

from dataclasses import dataclass, field
from typing import Any

from shell.aliases import AliasManager
from shell.config import ShellConfig
from shell.environment import Environment
from shell.history import CommandHistory


@dataclass
class ShellSession:
    """Encapsulates per-session shell state."""

    config: ShellConfig
    environment: Environment
    history: CommandHistory
    aliases: AliasManager
    cwd: str = "/"
    running: bool = True
    last_exit_code: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, config: ShellConfig | None = None, users: Any | None = None) -> "ShellSession":
        config = config or ShellConfig()
        username = users.whoami() if users is not None else "forge"
        hostname = users.hostname if users is not None else "localhost"
        user_record = users.get_user(username) if users is not None else None
        home = user_record["home"] if user_record else "/home/forge"

        environment = Environment(
            {
                "USER": username,
                "HOSTNAME": hostname,
                "HOME": home,
                "SHELL": user_record["shell"] if user_record else "/bin/forge",
                "PATH": "/usr/bin:/bin:/usr/local/bin",
                "PWD": home,
                "FORGE_VERSION": config.version,
            }
        )
        session = cls(
            config=config,
            environment=environment,
            history=CommandHistory(max_entries=config.history_max_entries),
            aliases=AliasManager(),
            cwd=home,
        )
        session.set_cwd(home)
        return session

    def set_cwd(self, path: str) -> None:
        self.cwd = path
        self.environment.set("PWD", path)

    def stop(self) -> None:
        self.running = False
