"""
Wwise RTPC / Game Parameter Operations.

Provides tools for creating and managing Game Parameters (RTPCs).
"""

import json
from ..constants import GAME_PARAMETERS_ROOT


def _create_game_parameter(
    conn,
    name: str,
    min_value: float = 0.0,
    max_value: float = 100.0,
    default_value: float = 0.0
) -> dict:
    """Create a Game Parameter."""
    # Create Game Parameter under Game Parameters\Default Work Unit
    parent_path = GAME_PARAMETERS_ROOT

    result = conn.call("ak.wwise.core.object.create", {
        "parent": parent_path,
        "type": "GameParameter",
        "name": name,
        "onNameConflict": "rename"
    })

    # Set properties
    if result.get("id"):
        param_id = result["id"]

        # Set Min
        conn.call("ak.wwise.core.object.setProperty", {
            "object": param_id,
            "property": "Min",
            "value": min_value
        })

        # Set Max
        conn.call("ak.wwise.core.object.setProperty", {
            "object": param_id,
            "property": "Max",
            "value": max_value
        })

        # Set InitialValue (default value)
        conn.call("ak.wwise.core.object.setProperty", {
            "object": param_id,
            "property": "InitialValue",
            "value": default_value
        })

    return result


def _set_game_parameter_value(
    conn,
    game_parameter_path: str,
    value: float
) -> dict:
    """Set the current value of a game parameter."""
    result = conn.call("ak.wwise.core.object.setProperty", {
        "object": game_parameter_path,
        "property": "InitialValue",
        "value": value
    })
    return result


def _list_game_parameters(conn) -> dict:
    """List all game parameters."""
    waql = '$ from type GameParameter'

    result = conn.call("ak.wwise.core.object.get",
        {"waql": waql},
        options={"return": ["id", "name", "path", "@Min", "@Max", "@InitialValue"]}
    )
    return result


def register_mcp(mcp):
    """Register MCP tools for RTPC/Game Parameter operations."""

    @mcp.tool()
    async def create_game_parameter(
        name: str,
        min_value: float = 0.0,
        max_value: float = 100.0,
        default_value: float = 0.0
    ) -> str:
        """
        Create a Game Parameter (RTPC) under \\Game Parameters\\Default Work Unit.

        Args:
            name: Name for the game parameter
            min_value: Minimum value for the parameter
            max_value: Maximum value for the parameter
            default_value: Default/initial value for the parameter

        Returns:
            JSON string with created game parameter info
        """
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _create_game_parameter(conn, name, min_value, max_value, default_value)
        return json.dumps(result, indent=2, ensure_ascii=False)

    @mcp.tool()
    async def set_game_parameter_value(
        game_parameter_path: str,
        value: float
    ) -> str:
        """
        Set the current value of a game parameter.

        Args:
            game_parameter_path: Path to the game parameter
            value: New value to set

        Returns:
            JSON string with operation result
        """
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _set_game_parameter_value(conn, game_parameter_path, value)
        return json.dumps(result, indent=2, ensure_ascii=False)

    @mcp.tool()
    async def list_game_parameters() -> str:
        """
        List all game parameters in the project.

        Returns:
            JSON string with list of game parameters including their ranges and current values
        """
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _list_game_parameters(conn)
        return json.dumps(result, indent=2, ensure_ascii=False)


def register_cli(parent_app):
    """Register CLI commands for RTPC/Game Parameter operations."""
    import typer
    from rich.table import Table
    from ._cli_helpers import console

    app = typer.Typer(help="Wwise RTPC / Game Parameter operations")
    parent_app.add_typer(app, name="rtpc")

    def _output(result, as_json: bool):
        if as_json:
            typer.echo(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if isinstance(result, dict):
                if "return" in result:
                    # List of game parameters
                    items = result.get("return", [])
                    if items:
                        table = Table(title="Game Parameters")
                        table.add_column("Name", style="cyan")
                        table.add_column("Min", style="yellow")
                        table.add_column("Max", style="yellow")
                        table.add_column("Current", style="green")
                        table.add_column("Path", style="blue")
                        for item in items:
                            table.add_row(
                                item.get("name", ""),
                                str(item.get("@Min", "")),
                                str(item.get("@Max", "")),
                                str(item.get("@InitialValue", "")),
                                item.get("path", "")
                            )
                        console.print(table)
                    else:
                        console.print("[yellow]No game parameters found[/yellow]")
                else:
                    # Single operation result
                    console.print(f"[green]Success:[/green]")
                    console.print(f"  ID: {result.get('id', 'N/A')}")
                    console.print(f"  Name: {result.get('name', 'N/A')}")
            else:
                console.print(result)

    @app.command()
    def create(
        name: str = typer.Argument(..., help="Game parameter name"),
        min_value: float = typer.Option(0.0, help="Minimum value"),
        max_value: float = typer.Option(100.0, help="Maximum value"),
        default_value: float = typer.Option(0.0, help="Default value"),
        json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON")
    ):
        """Create a Game Parameter (RTPC)."""
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _create_game_parameter(conn, name, min_value, max_value, default_value)
        _output(result, json_output)

    @app.command()
    def set_value(
        game_parameter_path: str = typer.Argument(..., help="Game parameter path"),
        value: float = typer.Argument(..., help="Value to set"),
        json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON")
    ):
        """Set the current value of a game parameter."""
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _set_game_parameter_value(conn, game_parameter_path, value)
        _output(result, json_output)

    @app.command()
    def list(
        json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON")
    ):
        """List all game parameters."""
        from ..connection import get_connection
        conn = get_connection()
        conn.ensure_connected()
        result = _list_game_parameters(conn)
        _output(result, json_output)
