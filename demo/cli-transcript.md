# CLI walkthrough

This is the intended command sequence for a typical bulk operation, not captured terminal output. Producing real output requires a running Wwise instance with WAAPI enabled, which was not available while this showcase was assembled — so nothing here is presented as a transcript, and no output text has been invented.

## Scenario: bulk-create an RTPC, wire a SoundBank, verify with the profiler

```bash
# 1. Confirm we are talking to the right Wwise instance
wwise info

# 2. Create the game parameter used to drive vehicle pitch
wwise rtpc create "RPM_Engine" --min-value 0 --max-value 11000 --default-value 0

# 3. Create the SoundBank and include the relevant objects
wwise soundbank create "Vehicle_Main"
wwise soundbank set-inclusions "\\SoundBanks\\Vehicle_Main" \
  "\\Actor-Mixer Hierarchy\\Vehicles, \\Events\\Play_Engine_Loop"

# 4. Read the inclusions back — verify before generating
wwise soundbank get-inclusions "\\SoundBanks\\Vehicle_Main"

# 5. Generate
wwise soundbank generate --soundbank-paths "Vehicle_Main"

# 6. Observe what Wwise is actually playing
wwise profiler start
wwise profiler voices
wwise profiler busses
wwise profiler stop
```

## What the output looks like

Two modes, selected per command:

- **Human mode (default):** list-style commands render a rich table. For example `wwise soundbank list` renders a `SoundBanks` table with columns Name / ID / Short ID / Path. A transport command prints `Transport ID`, `Object` and `Action`; a state query prints the state.
- **Machine mode (`--json` / `-j`):** the same result is emitted as pretty-printed JSON with `ensure_ascii=False`, so non-ASCII object names survive round-tripping into a script.

Both modes are implemented once, in `tools/_cli_helpers.py`, so every command behaves consistently.

## Bulk-edit safety pattern

```bash
wwise project undo-begin
wwise object create ...      # repeated many times
wwise project undo-end
```

If the batch is wrong, the whole run is a single undo step inside Wwise.
