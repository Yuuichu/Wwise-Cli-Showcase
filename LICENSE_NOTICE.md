# Licence and third-party notice

## wwise-mcp (this toolkit)

Released under the **MIT licence**. The full licence text is included in this showcase as `LICENSE` and is unchanged from the private repository.

## Audiokinetic Wwise

**Wwise is a commercial product and a trademark of Audiokinetic Inc.** It is *not* included, redistributed or licensed here.

This toolkit is an independent client that talks to a running Wwise authoring application through Audiokinetic's own **Wwise Authoring API (WAAPI)**. Using it — and using WAAPI at all — requires your own valid Wwise licence. Nothing in this repository grants any right to Wwise itself, to its SDK, or to its sound engine.

No Audiokinetic proprietary code, headers, sample projects or Wwise content are redistributed in this showcase.

## Third-party Python dependencies

| Package | Role | Licence |
|---|---|---|
| `waapi-client` | Official-style Python client for WAAPI (`WaapiClient`) | See the upstream package |
| `typer` | CLI framework | MIT |
| `rich` | Terminal tables and colour output | MIT |
| `mcp` / FastMCP | Model Context Protocol server | MIT |

Dependencies are declared in `pyproject.toml` and installed from PyPI; none are vendored into this repository.

## Included sources

`selected-code/` contains verbatim copies of the connection layer, the CLI wiring, and two representative tool modules (RTPC and SoundBank), with no credentials and no project-specific configuration. `.env.example` contains only host/port defaults.