# Screenshots

Empty in this draft. Everything here requires a running Wwise 2023.1+ instance with WAAPI enabled, which was not available while assembling the showcase.

## What should be captured

1. **`hero-cli-table.png`** — a terminal after `wwise soundbank list`: the rich table with Name / ID / Short ID / Path. This is the clearest single image of the CLI as a product.
2. **`cli-json-mode.png`** — the same command with `--json`, showing that it is scriptable rather than a demo toy.
3. **`mcp-tools.png`** — the tool list as an MCP client sees it, which is the evidence that the same kernel serves AI agents.
4. **`profiler-voices.png`** — `wwise profiler voices` output during playback: the "what is actually playing" capability.
5. **`rtpc-bulk.png`** — a Wwise project tree showing several parameters created by one bulk command.

## Constraints on what may be shown

- **No client or production Wwise project content.** Project names, object hierarchies, event names and SoundBank names visible in any capture must come from a synthetic test project.
- No absolute local paths in the terminal prompt (a generic prompt is preferable).
- No API keys or authorisation tokens in the frame.

Until these exist, the showcase makes no visual claims.