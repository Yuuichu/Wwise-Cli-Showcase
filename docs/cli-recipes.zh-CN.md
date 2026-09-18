> [English](cli-recipes.md) | **简体中文**

# CLI 实战配方

下面的每条命令都与工具模块中注册的参数签名一致：位置参数为必填，`--json` / `-j` 把输出切换为机器可读形式。

## 连接

```bash
wwise info
```

## 用 WAQL 查询项目

```bash
wwise query waql '$ from type Sound'
wwise query find Sound
```

## 创建对象

```bash
wwise object create "\\Actor-Mixer Hierarchy\\SFX" Sound "Footstep"
wwise object rename "\\Actor-Mixer Hierarchy\\SFX\\Footstep" "Footstep_Grass"
wwise object list-children "\\Actor-Mixer Hierarchy\\SFX"
```

## 游戏参数（RTPC）

```bash
wwise rtpc create "Speed" --min-value 0 --max-value 200 --default-value 0
wwise rtpc set-value "\\Game Parameters\\Speed" 120
wwise rtpc list --json
```

## SoundBank —— 创建、配置、生成

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

## 传输控制 —— 从命令行试听事件

```bash
wwise transport play "\\Events\\Play_Footstep"
wwise transport pause   <transport-id>
wwise transport resume  <transport-id>
wwise transport get-state <transport-id>
wwise transport destroy <transport-id>

# No ID: stop everything
wwise transport stop
```

## 分析器 —— 到底在播什么

```bash
wwise profiler start
wwise profiler voices      # active voices
wwise profiler busses      # per-bus levels
wwise profiler stop
```

## 安全的批量编辑

```bash
wwise project undo-begin
# ... bulk operations ...
wwise project undo-end
wwise project save
```

## 脚本与自动化

每条命令都接受 `--json` / `-j`，这使得该工具箱可以在 shell 管道或 CI 步骤中使用：

```bash
wwise query waql '$ from type Sound' --json > sounds.json
```

## AI 智能体集成

```bash
wwise serve
# or
python -m wwise_mcp serve
```

用 MCP 客户端注册它（以 Claude Code 为例）：

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

## 前置条件

- Wwise 2023.1+ 正在运行，且在创作应用中**已启用 WAAPI**。
- 若不使用默认值（`127.0.0.1` / `8080`），需设置 `WWISE_HOST` / `WWISE_PORT`。
- 已安装该包（`pip install -e .`），它会暴露 `wwise` 入口点。