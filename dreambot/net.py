"""LAN connectivity utilities."""

from __future__ import annotations

import socket
from dataclasses import dataclass


@dataclass(frozen=True)
class ConnectionResult:
    host: str
    port: int
    success: bool
    message: str


def connect_to_lan(host: str, port: int, timeout: float) -> ConnectionResult:
    address = (host, port)
    try:
        with socket.create_connection(address, timeout=timeout):
            return ConnectionResult(
                host=host,
                port=port,
                success=True,
                message="Connection successful.",
            )
    except OSError as exc:
        return ConnectionResult(
            host=host,
            port=port,
            success=False,
            message=f"Connection failed: {exc}",
        )
