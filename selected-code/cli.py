"""Wwise CLI - Command line interface for Wwise Authoring API."""

from __future__ import annotations

import typer

from .tools import (
    objects,
    properties,
    events,
    rtpc,
    soundbank,
    import_audio,
    transport,
    switches,
    bus,
    query,
    attenuation,
    profiler,
    project,
    ui,
)

app = typer.Typer(
    name="wwise",
    help="Wwise CLI - Command line interface for Wwise Authoring API (WAAPI)",
    no_args_is_help=True,
)

_TOOL_MODULES = [
    objects,
    properties,
    events,
    rtpc,
    soundbank,
    import_audio,
    transport,
    switches,
    bus,
    query,
    attenuation,
    profiler,
    project,
    ui,
]

for _module in _TOOL_MODULES:
    _module.register_cli(app)


@app.command("serve")
def serve():
    """Start the Wwise MCP server for AI agent integration."""
    from .server import main
    main()


@app.command("info")
def info():
    """Show Wwise connection info."""
    from .connection import get_connection
    conn = get_connection()
    conn.ensure_connected()
    result = conn.get_info()
    from rich.console import Console
    from rich.table import Table
    console = Console()
    table = Table(title="Wwise Connection Info")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    for key, value in result.items():
        table.add_row(str(key), str(value))
    console.print(table)


def cli_main():
    """CLI entry point."""
    try:
        app()
    finally:
        from .connection import get_connection
        try:
            conn = get_connection()
            if conn.is_connected:
                conn.disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    cli_main()
