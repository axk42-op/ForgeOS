"""Credential store factory."""

from auth.base import CredentialBackend
from auth.config import is_supabase_configured, load_env
from auth.storage import LocalCredentialStore
from auth.supabase_store import SupabaseCredentialStore

_store: CredentialBackend | None = None


def get_credential_store() -> CredentialBackend:
    """Return Supabase store when configured, otherwise local storage."""
    global _store
    if _store is not None:
        return _store

    load_env()
    if is_supabase_configured():
        _store = SupabaseCredentialStore()
    else:
        _store = LocalCredentialStore()
    return _store
