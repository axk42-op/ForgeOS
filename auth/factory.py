"""Credential store factory."""

from auth.base import CredentialBackend
from auth.storage import LocalCredentialStore

_store: CredentialBackend | None = None


def get_credential_store() -> CredentialBackend:
    """Return local credential storage."""
    global _store
    if _store is None:
        _store = LocalCredentialStore()
    return _store
