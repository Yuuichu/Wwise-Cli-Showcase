# Architecture

> **English** | [简体中文](architecture.zh-CN.md)

The design goal is a **single WAAPI surface with two consumers**, so that an operation behaves identically whether a human runs it in a terminal or an AI agent calls it as a tool.

## Layers

### 1. Connection layer — `connection.py`

`WaapiConnection` is a **singleton** WAAPI connection manager:

- Endpoint is `ws://{host}:{port}/waapi`, read from `WWISE_HOST` / `WWISE_PORT` (defaults `127.0.0.1` / `8080`).
- `call(uri, args, options)` is the single entry point every tool uses.
- **Auto-reconnect:** if a call raises `ConnectionError`, `TimeoutError`, `OSError` or `RuntimeError`, the manager marks the connection dead, reconnects, and retries the call once. A long bulk operation therefore survives the authoring application being restarted mid-run.
- `ensure_connected()` is called before every call, so tools never have to think about connection state.
- `reset()` exists for tests, and disconnects cleanly if a connection was open.

The underlying `waapi-client` is fully synchronous, and the wrapper keeps that model rather than layering a fake async API over it: the tool surface is synchronous, and the MCP server is the only place where concurrency questions arise.

### 2. Tool modules — `tools/`

Fourteen modules, one per WAAPI category (`objects`, `properties`, `events`, `rtpc`, `soundbank`, `import_audio`, `transport`, `switches`, `bus`, `query`, `attenuation`, `profiler`, `project`, `ui`).

Each module follows the same contract:

```python
@mcp.tool()
def some_operation(...):
    return get_connection().call("ak.wwise.core....", args)

def register_cli(parent_app):
    app = typer.Typer(help="...")
    parent_app.add_typer(app, name="<category>")

    @app.command()
    def some_operation(...):
        ...
```

Two registrations, one implementation surface. This is why the CLI and the MCP tool list stay in sync: adding a tool means adding both registrations in the same file, next to each other.

Shared behaviour lives in `tools/_cli_helpers.py`:

- `run_async()` — a single place where the event loop is bridged, so command bodies stay synchronous-looking.
- `output_result()` — one switch between JSON mode and human output.
- `render_table()` — the rich-table renderer used by list commands, so every list looks the same.

### 3. Two front ends

| Front end | Implementation | Consumer |
|---|---|---|
| `cli.py` | `typer.Typer` named `wwise`; iterates the tool modules and calls `register_cli(app)` for each | Audio designers, scripts, CI |
| `server.py` | FastMCP server exposing the same functions as MCP tools | AI agents (e.g. Claude Code) |

`wwise serve` and `python -m wwise_mcp serve` both start the MCP server; `wwise info` reports connection state.

## Guardrails

Three deliberate safety decisions:

1. **Idempotent creation with a query first.** RTPC/parameter creation queries existing parameters and only writes when the target does not already exist, so a bulk run cannot silently clobber a curve that a designer spent time on.
2. **Explicit transport lifecycle.** Playback objects are created by `transport_play` and removed by `transport_destroy`; `transport stop` with no ID stops all transports rather than leaving handles dangling.
3. **Undo groups.** `project undo-begin` / `undo-end` wrap bulk mutations so a bad batch can be rolled back inside Wwise as one operation.

## Why both interfaces exist

They are not two products. A designer doing a repetitive task wants a command with a table of results; an agent doing the same task wants a tool with structured output. Because both are generated from the same module, the *semantics* cannot diverge — only the presentation differs.