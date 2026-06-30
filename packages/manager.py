"""Package manager for Forge OS."""


class PackageManager:
    """Manages Forge OS packages via forgepkg."""

    def __init__(self) -> None:
        self._packages: dict[str, dict] = {
            "forge-shell": {"version": "1.0.0", "description": "Forge Shell terminal"},
            "forge-core": {"version": "1.0.0", "description": "Forge OS core system"},
        }

    def list_packages(self) -> dict[str, dict]:
        return dict(self._packages)

    def get_package(self, name: str) -> dict | None:
        return self._packages.get(name)

    def install_package(self, name: str, version: str = "1.0.0", description: str = "") -> bool:
        if name in self._packages:
            return False
        self._packages[name] = {
            "version": version,
            "description": description or f"{name} package",
        }
        return True

    def info(self) -> dict[str, str]:
        return {
            "manager": "forgepkg",
            "version": "1.0.0",
            "installed_count": str(len(self._packages)),
        }
