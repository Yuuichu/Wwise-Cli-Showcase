> [English](architecture.md) | **简体中文**

# 架构

设计目标是**单一 WAAPI 界面、两个使用方**，从而让同一个操作在人从终端执行、或 AI 智能体作为工具调用时行为完全一致。

## 分层

### 1. 连接层 —— `connection.py`

`WaapiConnection` 是一个**单例** WAAPI 连接管理器：

- 端点为 `ws://{host}:{port}/waapi`，从 `WWISE_HOST` / `WWISE_PORT` 读取（默认 `127.0.0.1` / `8080`）。
- `call(uri, args, options)` 是每个工具都使用的唯一入口点。
- **自动重连：** 如果一次调用抛出 `ConnectionError`、`TimeoutError`、`OSError` 或 `RuntimeError`，管理器会把连接标记为失效、重新连接，并把该次调用重试一次。因此长时间的批量操作能在创作应用于运行中途被重启后继续存活。
- 每次调用前都会执行 `ensure_connected()`，因此工具本身永远不需要考虑连接状态。
- `reset()` 供测试使用；若之前有打开的连接，它会干净地断开。

底层的 `waapi-client` 完全是同步的，封装层保留了这个模型，而不是在其上再叠一层假异步 API：工具界面是同步的，MCP 服务器是唯一会出现并发问题的地方。

### 2. 工具模块 —— `tools/`

十四个模块，每个 WAAPI 类别一个（`objects`、`properties`、`events`、`rtpc`、`soundbank`、`import_audio`、`transport`、`switches`、`bus`、`query`、`attenuation`、`profiler`、`project`、`ui`）。

每个模块都遵循同一份契约：

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

两处注册，一份实现。这正是 CLI 与 MCP 工具列表能保持同步的原因：新增一个工具，就是在同一个文件里、相邻的位置添加这两处注册。

共享行为放在 `tools/_cli_helpers.py` 中：

- `run_async()` —— 桥接事件循环的唯一位置，因此命令主体看起来始终是同步的。
- `output_result()` —— JSON 模式与人类可读输出之间的唯一开关。
- `render_table()` —— 列表命令使用的 rich 表格渲染器，因此每个列表看起来都一致。

### 3. 两个前端

| 前端 | 实现 | 使用方 |
|---|---|---|
| `cli.py` | 名为 `wwise` 的 `typer.Typer`；遍历工具模块并对每个模块调用 `register_cli(app)` | 音频设计师、脚本、CI |
| `server.py` | FastMCP 服务器，把同样的函数暴露为 MCP 工具 | AI 智能体（例如 Claude Code） |

`wwise serve` 与 `python -m wwise_mcp serve` 都会启动 MCP 服务器；`wwise info` 报告连接状态。

## 防护措施

三个刻意的安全决定：

1. **先查询，再幂等创建。** RTPC/参数创建会先查询已有参数，只在目标不存在时才写入，因此批量运行不会静默覆盖设计师花时间调好的曲线。
2. **显式的传输控制生命周期。** 播放对象由 `transport_play` 创建、由 `transport_destroy` 移除；不带 ID 的 `transport stop` 会停止所有传输控制对象，而不是留下悬空的句柄。
3. **Undo 组。** `project undo-begin` / `undo-end` 把批量改动包起来，因此一批坏改动可以在 Wwise 内部作为一次操作整体回滚。

## 为什么两种接口都存在

它们不是两个产品。做重复性任务的设计师想要一条带结果表格的命令；做同一任务的智能体想要一个输出结构化的工具。由于两者都由同一个模块生成，*语义*不可能分叉——只有呈现方式不同。