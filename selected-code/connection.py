"""WAAPI connection manager for Wwise MCP."""

from __future__ import annotations

import os
from typing import Any, Optional


class WaapiConnection:
    """Singleton WAAPI connection manager with auto-reconnect.

    waapi-client (WaapiClient) is fully synchronous:
    - Connects during __init__
    - call() is blocking
    - disconnect() is blocking
    """

    _instance: Optional[WaapiConnection] = None
    _client: Any = None
    _connected: bool = False

    def __init__(self, host: str | None = None, port: int | None = None):
        self.host = host or os.getenv("WWISE_HOST", "127.0.0.1")
        self.port = port or int(os.getenv("WWISE_PORT", "8080"))
        self.url = f"ws://{self.host}:{self.port}/waapi"

    @classmethod
    def get_instance(cls) -> WaapiConnection:
        if cls._instance is None:
            cls._instance = WaapiConnection()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton (for testing)."""
        if cls._instance and cls._instance._connected:
            try:
                cls._instance.disconnect()
            except Exception:
                pass
        cls._instance = None

    def ensure_connected(self) -> None:
        """Connect to Wwise if not already connected."""
        if self._connected and self._client:
            return
        self.connect()

    def connect(self) -> None:
        """Connect to Wwise WAAPI."""
        from waapi import WaapiClient
        self._client = WaapiClient(url=self.url)
        self._connected = self._client.is_connected()

    def disconnect(self) -> None:
        """Disconnect from Wwise."""
        if self._client and self._connected:
            try:
                self._client.disconnect()
            except Exception:
                pass
            self._connected = False
            self._client = None

    def call(self, uri: str, args: dict | None = None, options: dict | None = None) -> Any:
        """Call a WAAPI endpoint with auto-reconnect on failure."""
        self.ensure_connected()
        try:
            if options:
                return self._client.call(uri, args or {}, options=options)
            return self._client.call(uri, args or {})
        except (ConnectionError, TimeoutError, OSError, RuntimeError):
            self._connected = False
            self.connect()
            if options:
                return self._client.call(uri, args or {}, options=options)
            return self._client.call(uri, args or {})

    @property
    def is_connected(self) -> bool:
        return self._connected

    def get_info(self) -> dict:
        """Get Wwise application info."""
        return self.call("ak.wwise.core.getInfo")


def get_connection() -> WaapiConnection:
    """Get the singleton WAAPI connection."""
    return WaapiConnection.get_instance()
