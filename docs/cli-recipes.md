# CLI recipes

Every command below matches the argument signatures registered in the tool modules: positional arguments are required, `--json` / `-j` switches output to machine-readable form.

## Connection

```bash
wwise info
```

## Query the project with WAQL

```bash
wwise query waql '$ from type Sound'
wwise query find Sound
```

## Create objects

```bash
wwise object create "\\Actor-Mixer Hierarchy\\SFX" Sound "Footstep"
wwise object rename "\\Actor-Mixer Hierarchy\\SFX\\Footstep" "Footstep_Grass"
wwise object list-children "\\Actor-Mixer Hierarchy\\SFX"
```

## Game parameters (RTPC)

```bash
wwise rtpc create "Speed" --min-value 0 --max-value 200 --default-value 0
wwise rtpc set-value "\\Game Parameters\\Speed" 120
wwise rtpc list --json
```

## SoundBanks — create, configure, generate

```bash
wwise soundbank create "SFX_Main"

wwise soundbank set-inclusions "\\SoundBanks\\SFX_Main" \
  "\\Actor-Mixer Hierarchy\\SFX, \\Events\\Play_Footstep"

# Read back what is included before generating
wwise soundbank get-inclusions "\\SoundBanks\\SFX_Main"

# Empty --soundbank-paths means "generate all"
wwise soundbank generate
wwise soundbank generate --soundbank-paths "SFX_Main"

wwise soundbank list
```

## Transport — audition events from the command line

```bash
wwise transport play "\\Events\\Play_Footstep"
wwise transport pause   <transport-id>
wwise transport resume  <transport-id>
wwise transport get-state <transport-id>
wwise transport destroy <transport-id>

# No ID: stop everything
wwise transport stop
```

## Profiler — what is actually playing

```bash
wwise profiler start
wwise profiler voices      # active voices
wwise profiler busses      # per-bus levels
wwise profiler stop
```

## Safe bulk edits

```bash
wwise project undo-begin
# ... bulk operations ...
wwise project undo-end
wwise project save
```

## Scripting and automation

Every command accepts `--json` / `-j`, which makes the toolkit usable from a shell pipeline or CI step:

```bash
wwise query waql '$ from type Sound' --json > sounds.json
```

## AI agent integration

```bash
wwise serve
# or
python -m wwise_mcp serve
```

Register it with an MCP client (Claude Code example):

```json
{
  "mcpServers": {
    "wwise": {
      "command": "python",
      "args": ["-m", "wwise_mcp", "serve"]
    }
  }
}
```

## Prerequisites

- Wwise 2023.1+ running, with **WAAPI enabled** in the authoring application.
- `WWISE_HOST` / `WWISE_PORT` set if not using the defaults (`127.0.0.1` / `8080`).
- The package installed (`pip install -e .`), which exposes the `wwise` entry point.