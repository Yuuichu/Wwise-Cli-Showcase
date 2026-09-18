# Tool catalog

**55 tools across 14 categories**, extracted directly from the registered tool modules in `src/wwise_mcp/tools/`. Each tool is exposed twice: as an MCP tool with the function name below, and as a CLI subcommand.

> Verification note: the tool modules were parsed for `@mcp.tool` decorators and their following function definitions, and the CLI surface for `@app.command()` registrations. Both counts are 55, which is why this catalog differs from the shorter table in the repository's own `README.md` (that table lists 52 and omits `get-inclusions`, `transport resume`, `transport destroy` and the switch-assignment renames).

## Object — 8

| MCP tool | CLI |
|---|---|
| `create_object` | `wwise object create` |
| `delete_object` | `wwise object delete` |
| `move_object` | `wwise object move` |
| `copy_object` | `wwise object copy` |
| `get_object` | `wwise object get` |
| `rename_object` | `wwise object rename` |
| `set_object_notes` | `wwise object set-notes` |
| `list_children` | `wwise object list-children` |

## Property — 4

| MCP tool | CLI |
|---|---|
| `set_property` | `wwise property set` |
| `get_properties` | `wwise property get` |
| `set_reference` | `wwise property set-reference` |
| `list_property_names` | `wwise property list-names` |

## Event — 3

| MCP tool | CLI |
|---|---|
| `create_event` | `wwise event create` |
| `add_event_action` | `wwise event add-action` |
| `list_events` | `wwise event list` |

## RTPC — 3

| MCP tool | CLI |
|---|---|
| `create_game_parameter` | `wwise rtpc create` |
| `set_game_parameter_value` | `wwise rtpc set-value` |
| `list_game_parameters` | `wwise rtpc list` |

## SoundBank — 5

| MCP tool | CLI |
|---|---|
| `create_soundbank` | `wwise soundbank create` |
| `set_soundbank_inclusions` | `wwise soundbank set-inclusions` |
| `get_soundbank_inclusions` | `wwise soundbank get-inclusions` |
| `generate_soundbanks` | `wwise soundbank generate` |
| `list_soundbanks` | `wwise soundbank list` |

## Import — 2

| MCP tool | CLI |
|---|---|
| `import_audio_files` | `wwise import audio` |
| `batch_import` | `wwise import batch` |

## Transport — 6

| MCP tool | CLI |
|---|---|
| `transport_play` | `wwise transport play` |
| `transport_stop` | `wwise transport stop` |
| `transport_pause` | `wwise transport pause` |
| `transport_resume` | `wwise transport resume` |
| `transport_get_state` | `wwise transport get-state` |
| `transport_destroy` | `wwise transport destroy` |

## Switch / State — 5

| MCP tool | CLI |
|---|---|
| `create_switch_group` | `wwise switch create-group` |
| `create_state_group` | `wwise switch create-state-group` |
| `add_switch_assignment` | `wwise switch add-assignment` |
| `remove_switch_assignment` | `wwise switch remove-assignment` |
| `get_switch_assignments` | `wwise switch list-assignments` |

## Bus — 3

| MCP tool | CLI |
|---|---|
| `create_bus` | `wwise bus create` |
| `create_aux_bus` | `wwise bus create-aux` |
| `set_bus_routing` | `wwise bus set-routing` |

## Query — 2

| MCP tool | CLI |
|---|---|
| `waql_query` | `wwise query waql` |
| `find_by_type` | `wwise query find` |

## Attenuation — 3

| MCP tool | CLI |
|---|---|
| `create_attenuation` | `wwise attenuation create` |
| `set_attenuation_curve` | `wwise attenuation set-curve` |
| `get_attenuation_curve` | `wwise attenuation get-curve` |

## Profiler — 4

| MCP tool | CLI |
|---|---|
| `profiler_start_capture` | `wwise profiler start` |
| `profiler_stop_capture` | `wwise profiler stop` |
| `profiler_get_voices` | `wwise profiler voices` |
| `profiler_get_busses` | `wwise profiler busses` |

## Project — 5

| MCP tool | CLI |
|---|---|
| `project_save` | `wwise project save` |
| `project_get_info` | `wwise project info` |
| `undo_begin_group` | `wwise project undo-begin` |
| `undo_end_group` | `wwise project undo-end` |
| `undo` | `wwise project undo` |

## UI — 2

| MCP tool | CLI |
|---|---|
| `ui_get_selected` | `wwise ui selected` |
| `ui_execute_command` | `wwise ui exec` |

## Plus

| Command | Purpose |
|---|---|
| `wwise info` | Show Wwise connection info |
| `wwise serve` | Start the MCP server (equivalent to `python -m wwise_mcp serve`) |