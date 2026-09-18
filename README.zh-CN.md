> [English](README.md) | **简体中文**

# wwise-mcp —— Wwise Authoring API 工具箱（CLI + MCP 服务器）

一套内核，两种接口：面向**音频设计师**的 CLI，用于在 Wwise 中做批量工作；以及面向 **AI 智能体**的 MCP 服务器，驱动同一批操作。

## 为什么做这个

Wwise 的创作应用是为一次一个、手把手的工作方式设计的。对声音设计来说这是正确的设计，对重复性的项目工作来说则是错误的设计：批量创建参数、连接衰减曲线、配置并生成 SoundBank，或者采样分析器来回答「到底有哪些声部在播」。这些都是可脚本化的操作，却一直靠手工完成。

Wwise Authoring API（WAAPI）让这些操作变得可脚本化，但裸用 WAAPI 客户端每次仍然等于一个小型脚本工程。我想要一个统一封装好的界面：设计师能从终端使用，AI 智能体可以把它当作工具调用——而且语义完全一致，这样两者的行为不会发生偏移。

## 功能概览

- **14 个类别共 55 个工具**，覆盖对象、属性、事件、RTPC、SoundBank、导入、传输控制、Switch/State、总线、WAQL 查询、衰减、分析器、项目管理和 UI 控制。
- **一套内核，双接口：** 每个工具同时以 MCP 工具（面向 AI 智能体）和 CLI 子命令（面向人）两种形式暴露，名称与参数一一对应。
- **支持 WAQL**，可做表达力强的查询（`wwise query waql '$ from type Sound'`）。
- **断线自动重连**，因此长时间的批量操作能在创作工具被重启后继续存活。
- **每条命令都支持 JSON 输出模式**，用于脚本和 CI；交互使用时则提供 rich 表格/彩色输出。
- **可安装的包**（`pip install -e .`），附带双语文档和 pytest 测试套件。

## 工作流

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

## 技术要点

- **55 个已注册工具，14 个类别**——直接从源码注册表核对得出，而不是照抄文档。`docs/tool-catalog.zh-CN.md` 中的表格由工具模块生成。
- **在 WAAPI 有风险的地方加防护。** RTPC 创建是幂等的，并且会先查询再写入，因此批量创建参数不可能静默覆盖已有的曲线；WAQL 输入经过校验，而不是做字符串拼接。
- **共享的 CLI 管道。** 输出格式化、JSON 模式与错误处理都放在同一个辅助模块（`_cli_helpers.py`）里，因此新增工具会继承一致的终端行为，不会各自漂移出不同的输出格式。
- **显式的传输控制生命周期。** 传输控制对象被创建、恢复并显式销毁，因此播放对象不会在多次操作之间泄漏。
- **关闭时清理服务器**，因此 MCP 会话中断不会留下半开的 WAAPI 连接。

## 架构

`docs/architecture.zh-CN.md` 介绍连接层、工具模块契约、CLI/MCP 双界面，以及两者为何并存。

## 我的角色

独立作者：WAAPI 封装设计、工具界面、CLI、MCP 服务器、测试与文档。

## 局限与边界

- **需要 Wwise 2023.1+ 并启用 WAAPI。** 这里的一切都不替代创作应用，而是驱动它。
- **没有离线模式。** 这些工具针对**正在运行**的 Wwise 实例工作，因此在没有实例的情况下无法在 CI 中演练。
- **结构性改动不是免费的。** 操作有防护（幂等创建、显式查询），但批量操作仍然会改动真实项目——请使用版本控制和 undo 组。
- **覆盖面是 WAAPI 的接口面，而不是 Wwise 的功能集。** 混音行为、效果器和总线层级是通过通用的对象/属性操作触及的，而不是通过专门的高层工具。
- **未经过工作室规模的实战检验。** 它尚未在大型团队或长周期生产项目中使用过。

## 仓库范围

这是一个作品集展示仓库。完整开发仓库保持私有。

`selected-code/` 中包含：连接层、CLI 接线、一个 RTPC 工具模块和一个 SoundBank 工具模块。另外包含：完整且经核对的工具目录（`docs/tool-catalog.zh-CN.md`）。不包含：其余工具模块（它们是同一模式的程序化变体）、项目夹具，以及任何项目特定的配置。

## 技术栈

`Python 3.10+` · `Wwise Authoring API (WAAPI)` · `WAQL` · `MCP (Model Context Protocol)` · `FastMCP` · `typer` · `rich` · `pytest`