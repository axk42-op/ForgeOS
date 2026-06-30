"""Interactive registration and login prompts."""

from getpass import getpass

from rich.console import Console
from rich.panel import Panel

from auth.factory import get_credential_store


class AuthFlow:
    """Handles first-run registration and returning-user login."""

    def __init__(self, store=None, console: Console | None = None) -> None:
        self._store = store or get_credential_store()
        self._console = console or Console(force_terminal=True, legacy_windows=False)

    def authenticate(self) -> str:
        """Register on first run, otherwise prompt for login. Returns username."""
        if not self._store.has_users():
            return self._register()
        return self._login()

    def _register(self) -> str:
        self._console.print(
            Panel(
                "Welcome to Forge OS.\nCreate your account (stored locally on this machine).\n"
                "Passwords are stored as salted hashes — never plain text.",
                title="First Run Setup",
                border_style="cyan",
            )
        )
        while True:
            username = input("Choose a username: ").strip()
            if not username:
                self._console.print("[red]Username cannot be empty.[/red]")
                continue
            if " " in username:
                self._console.print("[red]Username cannot contain spaces.[/red]")
                continue

            password = getpass("Choose a password: ")
            confirm = getpass("Confirm password: ")
            if password != confirm:
                self._console.print("[red]Passwords do not match. Try again.[/red]")
                continue

            try:
                record = self._store.register(username, password)
                self._store.remember_username(record.username)
                self._console.print(f"[green]Account created for '{record.username}'.[/green]")
                self._console.print()
                return record.username
            except ValueError as error:
                self._console.print(f"[red]{error}[/red]")
            except Exception as error:
                self._console.print(f"[red]Registration failed: {error}[/red]")

    def _login(self) -> str:
        hint = self._store.last_username()
        hint_text = f"\nLast signed in: [cyan]{hint}[/cyan]" if hint else ""
        self._console.print(
            Panel(
                f"Sign in to continue.{hint_text}",
                title="Forge OS Login",
                border_style="cyan",
            )
        )

        attempts = 3
        while attempts > 0:
            default = hint or ""
            username = input(f"Username{f' [{default}]' if default else ''}: ").strip() or default
            if not username:
                self._console.print("[red]Username is required.[/red]")
                continue

            password = getpass("Password: ")
            if self._store.verify(username, password):
                self._store.remember_username(username)
                self._console.print(f"[green]Welcome back, {username}.[/green]")
                self._console.print()
                return username

            attempts -= 1
            remaining = attempts
            if remaining:
                self._console.print(f"[red]Invalid credentials. {remaining} attempt(s) left.[/red]")
            else:
                self._console.print("[red]Too many failed attempts. Exiting.[/red]")
                raise SystemExit(1)

        raise SystemExit(1)
