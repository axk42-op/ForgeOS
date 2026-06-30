"""Forge OS command-line interface."""

import argparse
import sys

from launcher import boot_script, project_root, spawn_forgeos_window


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="forgeos",
        description="Forge OS — a Python virtual operating system",
    )
    subparsers = parser.add_subparsers(dest="command")

    login_parser = subparsers.add_parser("login", help="Open Forge OS in a new window and sign in")
    login_parser.set_defaults(handler=_cmd_login)

    start_parser = subparsers.add_parser("start", help="Alias for forgeos login")
    start_parser.set_defaults(handler=_cmd_login)

    subparsers.add_parser("version", help="Show Forge OS version").set_defaults(handler=_cmd_version)

    args = parser.parse_args()
    if not hasattr(args, "handler"):
        return _cmd_login(args)
    return args.handler(args)


def _cmd_login(_args: argparse.Namespace) -> int:
    spawn_forgeos_window()
    print("Opening ForgeOS window...")
    return 0


def _cmd_version(_args: argparse.Namespace) -> int:
    from boot import ForgeOS

    print(f"Forge OS v{ForgeOS.VERSION}")
    print(f"Install path: {project_root()}")
    print(f"Boot script: {boot_script()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
