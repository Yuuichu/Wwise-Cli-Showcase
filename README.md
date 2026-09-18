# wwise-mcp — Wwise Authoring API toolkit (CLI + MCP server)

One kernel, two interfaces: a **CLI for audio designers** doing bulk work in Wwise, and an **MCP server for AI agents** driving the same operations.

<!-- Hero image: see screenshots/README.md -->

## Why I Built This

Wwise's authoring application is built for one-at-a-time, hands-on work. That is the right design for sound design, and the wrong one for repetitive project work: creating parameters in bulk, wiring attenuation curves, configuring and generating SoundBanks, or sampling the profiler to answer "which voices are actually playing". Those are scriptable operations that were being done by hand.

The Wwise Authoring API (WAAPI) makes them scriptable, but a raw WAAPI client is still a scripting project every time. I wanted a single wrapped surface that a designer can use from a terminal and an AI agent can use as tools — with identical semantics, so behaviour does not drift between the two.

## What It Does

- **55 tools across 14 categories** covering objects, properties, events, RTPC, SoundBanks, import, transport, switches/states, buses, WAQL queries, attenuation, profiler, project management and UI control.
- **Dual interface over one kernel:** every tool is exposed both as an MCP tool (for AI agents) and as a CLI subcommand (for humans), with matching names and parameters.
- **WAQL support** for expressive queries (`wwise query waql '$ from type Sound'`).
- **Auto-reconnect** on connection loss, so a long bulk operation survives the authoring tool being restarted.
- **JSON output mode** on every command for scripting and CI, plus rich table/colour output for interactive use.
- **Packaged install** (`pip install -e .`) with bilingual documentation and a pytest suite.

## Workflow

```text
WAAPI (Wwise Authoring API)
        |
        v
   connection layer  (connect, auto-reconnect, error handling)
        |
        v
   tool modules  x 14   (objects, rtpc, soundbank, profiler, ...)
        |
        +--> CLI  (typer)   --> audio designer in a terminal
        |
        +--> MCP  (FastMCP) --> AI agent / automation
```

## Technical Highlights

- **55 registered tools, 14 categories** — verified directly from the source registry rather than from documentation. The table in `docs/tool-catalog.md` is generated from the tool modules.
- **Guardrails where WAAPI is dangerous.** RTPC creation is idempotent and queries before writing, so bulk parameter creation cannot silently overwrite an existing curve; WAQL input is validated rather than string-concatenated.
- **Shared CLI plumbing.** Output formatting, JSON mode and error handling live in one helper module (`_cli_helpers.py`), so a new tool inherits consistent terminal behaviour and cannot drift into its own output format.
- **Explicit transport lifecycle.** Transport commands are created, resumed and explicitly destroyed, so playback objects do not leak between operations.
- **Server cleanup on shutdown**, so a dropped MCP session does not leave a half-open WAAPI connection behind.

## Demo

`demo/cli-transcript.md` walks through the command surface. Screenshots are pending — see `screenshots/README.md`.

Selected source is in `selected-code/` (connection layer, CLI wiring, an RTPC tool module and a SoundBank tool module).

## Architecture

`docs/architecture.md` covers the connection layer, the tool-module contract, the CLI/MCP dual surface, and why both exist.

## My Role

Sole author: WAAPI wrapper design, tool surface, CLI, MCP server, tests and documentation.

## Limitations

- **Requires Wwise 2023.1+ with WAAPI enabled.** Nothing here replaces the authoring application; it drives it.
- **No offline mode.** The tools operate against a *running* Wwise instance, so they cannot be exercised in CI without one.
- **Structural changes are not free.** Operations are guarded (idempotent creation, explicit queries), but a bulk operation still mutates a real project — use version control and undo groups.
- **Coverage is the WAAPI surface, not the Wwise feature set.** Mix behaviour, effects and bus hierarchies are touched through generic object/property operations rather than dedicated high-level tools.
- **Not battle-tested at studio scale.** It has not been used across a large team or a long-lived production project.

## Repository Scope

This is a portfolio showcase repository. The full development repository remains private.

Included: the connection layer, CLI wiring and two representative tool modules, plus the complete verified tool catalog. Excluded: the remaining tool modules (they are procedural variations of the same pattern), project fixtures, and any project-specific configuration.

## Tech Stack

`Python 3.10+` · `Wwise Authoring API (WAAPI)` · `WAQL` · `MCP (Model Context Protocol)` · `FastMCP` · `typer` · `rich` · `pytest`