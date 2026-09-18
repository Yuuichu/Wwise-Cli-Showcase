> [English](tool-catalog.md) | **简体中文**

# 工具目录

**14 个类别共 55 个工具**，直接从 `src/wwise_mcp/tools/` 中已注册的工具模块提取。每个工具都以两种形式暴露：以下函数名对应的 MCP 工具，以及一个 CLI 子命令。

> 核对说明：工具模块被解析以提取 `@mcp.tool` 装饰器及其后紧跟的函数定义，CLI 界面则解析 `@app.command()` 注册。两者计数都是 55，这也是本目录与仓库自身 `README.md` 中那张更短的表格不一致的原因（该表列出 52 个，并遗漏了 `get-inclusions`、`transport resume`、`transport destroy` 以及 Switch 赋值的重命名）。

## 对象 —— 8

| MCP 工具 | CLI |
|---|---|
| `create_object` | `wwise object create` |
| `delete_object` | `wwise object delete` |
| `move_object` | `wwise object move` |
| `copy_object` | `wwise object copy` |
| `get_object` | `wwise object get` |
| `rename_object` | `wwise object rename` |
| `set_object_notes` | `wwise object set-notes` |
| `list_children` | `wwise object list-children` |

## 属性 —— 4

| MCP 工具 | CLI |
|---|---|
| `set_property` | `wwise property set` |
| `get_properties` | `wwise property get` |
| `set_reference` | `wwise property set-reference` |
| `list_property_names` | `wwise property list-names` |

## 事件 —— 3

| MCP 工具 | CLI |
|---|---|
| `create_event` | `wwise event create` |
| `add_event_action` | `wwise event add-action` |
| `list_events` | `wwise event list` |

## RTPC —— 3

| MCP 工具 | CLI |
|---|---|
| `create_game_parameter` | `wwise rtpc create` |
| `set_game_parameter_value` | `wwise rtpc set-value` |
| `list_game_parameters` | `wwise rtpc list` |

## SoundBank —— 5

| MCP 工具 | CLI |
|---|---|
| `create_soundbank` | `wwise soundbank create` |
| `set_soundbank_inclusions` | `wwise soundbank set-inclusions` |
| `get_soundbank_inclusions` | `wwise soundbank get-inclusions` |
| `generate_soundbanks` | `wwise soundbank generate` |
| `list_soundbanks` | `wwise soundbank list` |

## 导入 —— 2

| MCP 工具 | CLI |
|---|---|
| `import_audio_files` | `wwise import audio` |
| `batch_import` | `wwise import batch` |

## 传输控制 —— 6

| MCP 工具 | CLI |
|---|---|
| `transport_play` | `wwise transport play` |
| `transport_stop` | `wwise transport stop` |
| `transport_pause` | `wwise transport pause` |
| `transport_resume` | `wwise transport resume` |
| `transport_get_state` | `wwise transport get-state` |
| `transport_destroy` | `wwise transport destroy` |

## Switch / State —— 5

| MCP 工具 | CLI |
|---|---|
| `create_switch_group` | `wwise switch create-group` |
| `create_state_group` | `wwise switch create-state-group` |
| `add_switch_assignment` | `wwise switch add-assignment` |
| `remove_switch_assignment` | `wwise switch remove-assignment` |
| `get_switch_assignments` | `wwise switch list-assignments` |

## 总线 —— 3

| MCP 工具 | CLI |
|---|---|
| `create_bus` | `wwise bus create` |
| `create_aux_bus` | `wwise bus create-aux` |
| `set_bus_routing` | `wwise bus set-routing` |

## 查询 —— 2

| MCP 工具 | CLI |
|---|---|
| `waql_query` | `wwise query waql` |
| `find_by_type` | `wwise query find` |

## 衰减 —— 3

| MCP 工具 | CLI |
|---|---|
| `create_attenuation` | `wwise attenuation create` |
| `set_attenuation_curve` | `wwise attenuation set-curve` |
| `get_attenuation_curve` | `wwise attenuation get-curve` |

## 分析器 —— 4

| MCP 工具 | CLI |
|---|---|
| `profiler_start_capture` | `wwise profiler start` |
| `profiler_stop_capture` | `wwise profiler stop` |
| `profiler_get_voices` | `wwise profiler voices` |
| `profiler_get_busses` | `wwise profiler busses` |

## 项目 —— 5

| MCP 工具 | CLI |
|---|---|
| `project_save` | `wwise project save` |
| `project_get_info` | `wwise project info` |
| `undo_begin_group` | `wwise project undo-begin` |
| `undo_end_group` | `wwise project undo-end` |
| `undo` | `wwise project undo` |

## UI —— 2

| MCP 工具 | CLI |
|---|---|
| `ui_get_selected` | `wwise ui selected` |
| `ui_execute_command` | `wwise ui exec` |

## 附加

| 命令 | 用途 |
|---|---|
| `wwise info` | 显示 Wwise 连接信息 |
| `wwise serve` | 启动 MCP 服务器（等价于 `python -m wwise_mcp serve`） |