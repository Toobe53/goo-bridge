# GOO Bridge

面向 GOO 风格 NPR 渲染的跨平台 GUI 和 CLI，调用本机或远程无头 Blender 5.2。

[English](README.md) | 简体中文

GOO Bridge 是 Blender 的**外置**辅助工具：它不修改 Blender，也不重新分发
Blender。它分析 `.blend`，打包场景和资产，在本机或通过 SSH 在服务器上运行
Blender，校验返回的文件，并报告哪些 GOO 功能可以达到 L2、L1 或 L0。

[![build](https://github.com/Toobe53/goo-bridge/actions/workflows/build.yml/badge.svg)](https://github.com/Toobe53/goo-bridge/actions/workflows/build.yml)

**第一次使用？** 请先看[中英双语教程](docs/tutorial.md)。

## 状态

- 39 项兼容报告：**13 项 L2**、**15 项 L1**、**11 项 L0**
- 本地渲染、SSH 远程渲染、资产打包与 SHA-256 校验
- Tkinter GUI 和 CLI，仅使用 Python 标准库
- 测试覆盖 Windows、Linux、macOS；CI 使用 Blender 5.2.3

L2 表示在约定的 1%–2% 视觉误差内；L1 是明确的近似实现；L0 明确不支持，
不会伪装成可用。

## 安装

```bash
git clone https://github.com/Toobe53/goo-bridge.git
cd goo-bridge
python -m pip install .
goo-bridge doctor
```

或安装已发布的 wheel：

```bash
python -m pip install https://github.com/Toobe53/goo-bridge/releases/download/v0.1.0/goo_bridge-0.1.0-py3-none-any.whl
goo-bridge doctor
```

需要 Python 3.11+ 和 Blender 5.2.x。如果 Blender 不在默认位置，设置
`GOO_BRIDGE_BLENDER`：

```powershell
$env:GOO_BRIDGE_BLENDER = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
```

```bash
export GOO_BRIDGE_BLENDER=/Applications/Blender.app/Contents/MacOS/Blender
```

## 快速开始

```bash
goo-bridge analyze scene.blend -o analysis.json
goo-bridge report analysis.json -o analysis.html
goo-bridge render scene.blend -o renders/ --camera Camera --samples 32 --resolution 100
goo-bridge gui
```

### 通过 SSH 远程渲染

```bash
goo-bridge remote add studio --host 10.0.0.5 --user render --key ~/.ssh/id_ed25519
goo-bridge remote test --profile studio
goo-bridge remote render --profile studio scene.blend -o renders/
```

远程机器只需要 SSH 访问、Blender 5.2.x 和可写的 `~/.goo-bridge`。密码不会
被保存，只使用 SSH 密钥和系统 `known_hosts`。默认情况下，缺失资产会阻止
远程任务。

## CLI

| 命令 | 用途 |
|---|---|
| `goo-bridge doctor` | 检查 Python、Blender、配置和引擎 |
| `goo-bridge analyze` | 分析 `.blend` 中的 GOO 节点组、资产和设置 |
| `goo-bridge report` | 生成 HTML 分析报告 |
| `goo-bridge compat` | 生成 39 项 L2/L1/L0 兼容报告 |
| `goo-bridge render` | 用 Blender 5.2 本地渲染 |
| `goo-bridge gui` | 打开桌面 GUI |
| `goo-bridge remote` | 通过 SSH 添加/测试/渲染/查询/取回/清理 |
| `goo-bridge verify` | 校验发布目录中的 `SHA256SUMS` |

任何命令都可以加 `--json` 获取机器可读输出。用
`goo-bridge <command> --help` 查看完整选项。

## 文档

- [使用教程](docs/tutorial.md) — 安装、本地和远程流程
- [架构](docs/architecture.md) — 组件、传输与安全边界
- [兼容矩阵](docs/compatibility.md) — 全部 39 项及等级
- [远程渲染](docs/remote.md) — 服务器配置与排错
- [CLI 参考](docs/cli.md) — 每个命令和选项
- [验证报告](docs/verification.md) — 测试、CI 矩阵与发布校验
- [优化记录](docs/optimizations.md) — 十轮加固与证据

## 开发

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python tools/install_blender.py --dest .blender --json
```

没有 Blender 时，依赖 Blender 的测试会自动跳过。CI 在 Windows、Linux、
macOS 上运行同一套测试，并额外运行 Blender 集成任务。

## 安全

- 不保存密码，只支持基于密钥的 SSH
- 远程任务执行固定的 worker 脚本，不执行任意 shell
- 校验工作区相对路径，拒绝 `..` 越界
- 下载结果使用 SHA-256 校验
- 缺失资产会被报告，并默认阻止远程任务

## 许可

GPL-3.0-or-later。Blender 本身不包含在本发行版中。GOO Engine 是独立项目，
请查看其自身许可和兼容性说明。
