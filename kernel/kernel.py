"""Forge OS kernel."""

from datetime import datetime, timezone


class Kernel:
    """Core kernel services for Forge OS."""

    def __init__(self) -> None:
        self._boot_time = datetime.now(timezone.utc)
        self._version = "1.0.0"
        self._name = "Forge Kernel"

    @property
    def version(self) -> str:
        return self._version

    @property
    def name(self) -> str:
        return self._name

    @property
    def boot_time(self) -> datetime:
        return self._boot_time

    def uptime(self) -> str:
        delta = datetime.now(timezone.utc) - self._boot_time
        total_seconds = int(delta.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def info(self) -> dict[str, str]:
        return {
            "name": self._name,
            "version": self._version,
            "boot_time": self._boot_time.isoformat(),
            "uptime": self.uptime(),
        }
