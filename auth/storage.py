"""Local credential storage for Forge OS."""

import json
from dataclasses import asdict
from pathlib import Path

from platformdirs import user_data_dir

from auth.base import StoredCredentials
from auth.crypto import hash_password, new_salt, verify_password


class LocalCredentialStore:
    """Persists a single Forge OS account on the host machine."""

    APP_NAME = "ForgeOS"
    APP_AUTHOR = "ForgeOS"

    def __init__(self, path: Path | None = None) -> None:
        if path is None:
            data_dir = Path(user_data_dir(self.APP_NAME, self.APP_AUTHOR))
            data_dir.mkdir(parents=True, exist_ok=True)
            path = data_dir / "credentials.json"
        self._path = path

    @property
    def path(self) -> Path:
        return self._path

    def has_users(self) -> bool:
        return self._path.is_file()

    def user_exists(self, username: str) -> bool:
        record = self.load()
        return record is not None and record.username == username.strip()

    def load(self, username: str | None = None) -> StoredCredentials | None:
        if not self._path.is_file():
            return None
        data = json.loads(self._path.read_text(encoding="utf-8"))
        record = StoredCredentials(**data)
        if username and record.username != username.strip():
            return None
        return record

    def register(self, username: str, password: str) -> StoredCredentials:
        username = username.strip()
        if not username:
            raise ValueError("username cannot be empty")
        if len(password) < 4:
            raise ValueError("password must be at least 4 characters")
        if self.has_users():
            existing = self.load()
            if existing and existing.username != username:
                raise ValueError("a local account already exists; use passwd to change password")

        salt = new_salt()
        record = StoredCredentials(
            username=username,
            salt=salt,
            password_hash=hash_password(password, salt),
        )
        self._path.write_text(json.dumps(asdict(record), indent=2), encoding="utf-8")
        return record

    def verify(self, username: str, password: str) -> bool:
        record = self.load(username)
        if record is None:
            return False
        return verify_password(password, record.salt, record.password_hash)

    def update_password(self, username: str, current_password: str, new_password: str) -> bool:
        record = self.load(username)
        if record is None:
            return False
        if not verify_password(current_password, record.salt, record.password_hash):
            return False
        if len(new_password) < 4:
            raise ValueError("password must be at least 4 characters")

        salt = new_salt()
        updated = StoredCredentials(
            username=record.username,
            salt=salt,
            password_hash=hash_password(new_password, salt),
        )
        self._path.write_text(json.dumps(asdict(updated), indent=2), encoding="utf-8")
        return True

    def remember_username(self, username: str) -> None:
        record = self.load()
        if record is None:
            return
        if record.username == username.strip():
            return
        updated = StoredCredentials(
            username=username.strip(),
            salt=record.salt,
            password_hash=record.password_hash,
        )
        self._path.write_text(json.dumps(asdict(updated), indent=2), encoding="utf-8")

    def last_username(self) -> str | None:
        record = self.load()
        return record.username if record else None
