"""Ping a host (simulated)."""

import random
import time
from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class PingCommand(BaseCommand):
    name = "ping"
    category = "network"
    description = "Ping a network host (simulated)"
    syntax = "ping HOST"
    examples = ("ping localhost",)

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if not args:
            return CommandResult(output="ping: missing host operand", exit_code=1)

        host = args[0]
        lines = [f"PING {host} (127.0.0.1): 56 data bytes"]
        for seq in range(1, 5):
            ms = random.randint(1, 20)
            lines.append(f"64 bytes from {host}: icmp_seq={seq} ttl=64 time={ms} ms")
            time.sleep(0.05)
        lines.append(f"--- {host} ping statistics ---")
        lines.append("4 packets transmitted, 4 received, 0% packet loss")
        return CommandResult(output="\n".join(lines))
