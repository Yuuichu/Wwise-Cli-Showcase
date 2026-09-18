"""
Wwise SoundBank Operations.

Provides tools for creating, managing, and generating SoundBanks.
"""

import json
from ..constants import SOUNDBANKS_ROOT


def _create_soundbank(conn, name: str) -> dict:
    """Create a SoundBank."""
    parent_path = SOUNDBANKS_ROOT

    result = conn.call("ak.wwise.core.object.create", {
        "parent": parent_path,
        "type": "SoundBank",
        "name": name,
        "onNameConflict": "rename"
    })
    return result


def _set_soundbank_inclusions(
    conn,
    soundbank_path: str,
    inclusions: str
) -> dict:
    """Set inclusions for a SoundBank."""
    # Parse comma-separated paths
    inclusion_paths = [p.strip() for p in inclusions.split(",") if p.strip()]

    # Build inclusions list
    inclusions_list = []
    for path in inclusion_paths:
        inclusions_list.append({
            "object": path,
            "filter": ["events", "structures", "media"]
        })

    result = conn.call("ak.wwise.core.soundbank.setInclusions", {
        "soundbank": soundbank_path,
        "operation": "add",
        "inclusions": inclusions_list
    })
    return result


def _get_soundbank_inclusions(conn, soundbank_path: str) -> dict:
    """Get inclusions for a SoundBank."""
    result = conn.call("ak.wwise.core.soundbank.getInclusions", {
        "soundbank": soundbank_path
    })
    return result


def _generate_soundbanks(conn, soundbank_paths: str = "") -> dict:
    """Generate SoundBanks."""
    if soundbank_paths:
        # Parse comma-separated names/paths
        names = [n.strip() for n in soundbank_paths.split(",") if n.strip()]
        soundbanks_list = [{"name": name} for name in names]

        result = conn.call("ak.wwise.core.soundbank.generate", {
            "soundbanks": soundbanks_list
        })
    else:
        # Generate all soundbanks
        result = conn.call("ak.wwise.core.soundbank.generate", {})

    return result


def _list_soundbanks(conn) -> dict:
    """List all SoundBanks."""
    waql = '$ from type SoundBank'

    result = conn.call("ak.wwise.core.object.get",
        {"waql": waql},
        options={"return": ["id", "name", "path", "shortId"]}
    )
    return result


def register_mcp(mcp):
    """Register MCP tools for SoundBank operations."""

    @mcp.tool()
    async def create_soundbank(name: str) -> str:
        """
        Create a SoundBank under \\SoundBanks\\Default Work Unit.

        Args:
            name: Name for the new SoundBank

        Returns:
            JSON string with created SoundBank info
        """
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _create_soundbank(conn, name)
        return json.dumps(result, indent=2, ensure_ascii=False)

    @mcp.tool()
    async def set_soundbank_inclusions(
        soundbank_path: str,
        inclusions: str
    ) -> str:
        """
        Set inclusions for a SoundBank.

        Args:
            soundbank_path: Path to the SoundBank
            inclusions: Comma-separated list of object paths to include

        Returns:
            JSON string with operation result
        """
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _set_soundbank_inclusions(conn, soundbank_path, inclusions)
        return json.dumps(result, indent=2, ensure_ascii=False)

    @mcp.tool()
    async def get_soundbank_inclusions(soundbank_path: str) -> str:
        """
        Get inclusions for a SoundBank.

        Args:
            soundbank_path: Path to the SoundBank

        Returns:
            JSON string with list of inclusions
        """
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _get_soundbank_inclusions(conn, soundbank_path)
        return json.dumps(result, indent=2, ensure_ascii=False)

    @mcp.tool()
    async def generate_soundbanks(soundbank_paths: str = "") -> str:
        """
        Generate SoundBanks.

        Args:
            soundbank_paths: Optional comma-separated list of SoundBank names/paths.
                           If empty, generates all SoundBanks.

        Returns:
            JSON string with generation result
        """
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _generate_soundbanks(conn, soundbank_paths)
        return json.dumps(result, indent=2, ensure_ascii=False)

    @mcp.tool()
    async def list_soundbanks() -> str:
        """
        List all SoundBanks in the project.

        Returns:
            JSON string with list of SoundBanks
        """
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _list_soundbanks(conn)
        return json.dumps(result, indent=2, ensure_ascii=False)


def register_cli(parent_app):
    """Register CLI commands for SoundBank operations."""
    import typer
    from rich.table import Table
    from ._cli_helpers import console

    app = typer.Typer(help="Wwise SoundBank operations")
    parent_app.add_typer(app, name="soundbank")

    def _output(result, as_json: bool):
        if as_json:
            typer.echo(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if isinstance(result, dict):
                if "return" in result:
                    # List of soundbanks
                    items = result.get("return", [])
                    if items:
                        table = Table(title="SoundBanks")
                        table.add_column("Name", style="cyan")
                        table.add_column("ID", style="yellow")
                        table.add_column("Short ID", style="green")
                        table.add_column("Path", style="blue")
                        for item in items:
                            table.add_row(
                                item.get("name", ""),
                                item.get("id", ""),
                                str(item.get("shortId", "")),
                                item.get("path", "")
                            )
                        console.print(table)
                    else:
                        console.print("[yellow]No SoundBanks found[/yellow]")
                elif "inclusions" in result:
                    # Inclusions list
                    inclusions = result.get("inclusions", [])
                    if inclusions:
                        table = Table(title="SoundBank Inclusions")
                        table.add_column("Object", style="cyan")
                        table.add_column("Filter", style="yellow")
                        for inc in inclusions:
                            filters = ", ".join(inc.get("filter", []))
                            table.add_row(inc.get("object", ""), filters)
                        console.print(table)
                    else:
                        console.print("[yellow]No inclusions[/yellow]")
                else:
                    # Single operation result
                    console.print(f"[green]Success:[/green] {result}")
            else:
                console.print(result)

    @app.command()
    def create(
        name: str = typer.Argument(..., help="SoundBank name"),
        json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON")
    ):
        """Create a SoundBank."""
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _create_soundbank(conn, name)
        _output(result, json_output)

    @app.command()
    def set_inclusions(
        soundbank_path: str = typer.Argument(..., help="SoundBank path"),
        inclusions: str = typer.Argument(..., help="Comma-separated object paths"),
        json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON")
    ):
        """Set inclusions for a SoundBank."""
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _set_soundbank_inclusions(conn, soundbank_path, inclusions)
        _output(result, json_output)

    @app.command()
    def get_inclusions(
        soundbank_path: str = typer.Argument(..., help="SoundBank path"),
        json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON")
    ):
        """Get inclusions for a SoundBank."""
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _get_soundbank_inclusions(conn, soundbank_path)
        _output(result, json_output)

    @app.command()
    def generate(
        soundbank_paths: str = typer.Option("", help="Comma-separated SoundBank names (empty = all)"),
        json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON")
    ):
        """Generate SoundBanks."""
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _generate_soundbanks(conn, soundbank_paths)
        _output(result, json_output)

    @app.command()
    def list(
        json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON")
    ):
        """List all SoundBanks."""
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _list_soundbanks(conn)
        _output(result, json_output)
