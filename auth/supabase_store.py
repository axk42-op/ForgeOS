"""Supabase-backed credential storage for Forge OS."""

from __future__ import annotations

import json
from pathlib import Path

from platformdirs import user_data_dir

from auth.base import StoredCredentials
from auth.config import get_supabase_key, get_supabase_url
from auth.crypto import hash_password, new_salt, verify_password


class SupabaseCredentialStore:
    """Stores hashed credentials in Supabase table `forge_users`."""

    TABLE = "forge_users"
    APP_NAME = "ForgeOS"
    APP_AUTHOR = "ForgeOS"

    def __init__(self) -> None:
        url = get_supabase_url()
        key = get_supabase_key()
        if not url or not key:
            raise RuntimeError(
                "Supabase is not configured. Set FORGEOS_SUPABASE_URL and FORGEOS_SUPABASE_KEY in .env"
            )

        from supabase import create_client

        self._client = create_client(url, key)
        cache_dir = Path(user_data_dir(self.APP_NAME, self.APP_AUTHOR))
        cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache_path = cache_dir / "session.json"

    def has_users(self) -> bool:
        response = (
            self._client.table(self.TABLE)
            .select("id", count="exact")
            .limit(1)
            .execute()
        )
        return bool(response.count and response.count > 0)

    def user_exists(self, username: str) -> bool:
        return self.load(username) is not None

    def load(self, username: str | None = None) -> StoredCredentials | None:
        target = username.strip() if username else self.last_username()
        if not target:
            return None

        response = (
            self._client.table(self.TABLE)
            .select("username, password_hash, salt")
            .eq("username", target)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        if not rows:
            return None
        row = rows[0]
        return StoredCredentials(
            username=row["username"],
            password_hash=row["password_hash"],
            salt=row["salt"],
        )

    def register(self, username: str, password: str) -> StoredCredentials:
        username = username.strip()
        if not username:
            raise ValueError("username cannot be empty")
        if " " in username:
            raise ValueError("username cannot contain spaces")
        if len(password) < 4:
            raise ValueError("password must be at least 4 characters")
        if self.user_exists(username):
            raise ValueError(f"username '{username}' is already taken")

        salt = new_salt()
        record = StoredCredentials(
            username=username,
            salt=salt,
            password_hash=hash_password(password, salt),
        )
        self._client.table(self.TABLE).insert(
            {
                "username": record.username,
                "password_hash": record.password_hash,
                "salt": record.salt,
            }
        ).execute()
        self.remember_username(username)
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
        password_hash = hash_password(new_password, salt)
        (
            self._client.table(self.TABLE)
            .update({"password_hash": password_hash, "salt": salt})
            .eq("username", record.username)
            .execute()
        )
        return True

    def remember_username(self, username: str) -> None:
        self._cache_path.write_text(
            json.dumps({"last_username": username.strip()}),
            encoding="utf-8",
        )

    def last_username(self) -> str | None:
        if not self._cache_path.is_file():
            return None
        data = json.loads(self._cache_path.read_text(encoding="utf-8"))
        value = data.get("last_username")
        return str(value).strip() if value else None
