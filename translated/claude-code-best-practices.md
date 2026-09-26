# Claude Code 概览 | Claude Code 文档

Claude Code 是一个 AI 驱动的编码助手，帮助你构建功能、修复 bug、自动化开发任务。它能理解你的整个代码库，并可跨多个文件与工具协作完成任务。

## 快速开始

选择你的环境开始使用。大多数入口都需要 Claude 订阅或 Anthropic Console 账号。终端 CLI 与 VS Code 还支持第三方提供商。

**终端**：功能完备的 CLI，可直接在终端中使用 Claude Code。编辑文件、运行命令、从命令行管理整个项目。安装 Claude Code 可用以下方法之一：

原生安装（推荐）：

- macOS、Linux、WSL：`curl -fsSL https://claude.ai/install.sh | bash`
- Windows PowerShell：`irm https://claude.ai/install.ps1 | iex`
- Windows CMD：`curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`

（如果你看到 "The token '&&' is not a valid statement separator" 的提示，说明你在 PowerShell 而非 CMD 中，请改用上面的 PowerShell 命令。当提示符显示 PS C:\ 时即处于 PowerShell。Windows 需要 Git for Windows，若没有请先安装。）

原生安装会在后台自动更新，使你始终保持最新版本。

- Homebrew：`brew install --cask claude-code`
- WinGet：`winget install Anthropic.ClaudeCode`

Homebrew 与 WinGet 安装不会自动更新，需定期运行相应升级命令以获取最新功能与安全修复。

然后在任意项目中启动 Claude Code：

```
cd your-project
claude
```

首次使用时会提示登录。就这些！继续阅读快速开始 →

参见高级设置了解安装选项、手动更新或卸载说明。如遇问题，请访问故障排查。

**VS Code**：VS Code 扩展在你编辑器中直接提供行内 diff、@ 提及、计划评审与对话历史。可安装用于 VS Code 或 Cursor，或在扩展视图（Mac 为 Cmd+Shift+X，Windows/Linux 为 Ctrl+Shift+X）中搜索 "Claude Code"。安装后打开命令面板（Cmd+Shift+P / Ctrl+Shift+P），输入 "Claude Code" 并选择 "Open in New Tab"。

**桌面应用**：一个独立应用，用于在 IDE 或终端之外运行 Claude Code。可直观查看 diff、并行运行多个会话、安排重复任务，并启动云会话。提供 macOS（Intel 与 Apple Silicon）、Windows（x64）、Windows ARM64（仅远程会话）版本。安装后启动 Claude、登录并点击 Code 标签页即可开始编码。需要付费订阅。

**Web**：在浏览器中运行 Claude Code，无需本地设置。启动长时间任务并在完成时回来查看、处理本地没有的仓库，或并行运行多个任务。可用于桌面浏览器与 Claude iOS 应用。在 claude.ai/code 开始编码。

**JetBrains**：面向 IntelliJ IDEA、PyCharm、WebStorm 及其他 JetBrains IDE 的插件，支持交互式 diff 查看与选择上下文共享。从 JetBrains Marketplace 安装 Claude Code 插件并重启 IDE。

## 你能做什么

以下是一些使用 Claude Code 的方式：

**自动化你一直拖延的工作**：Claude Code 处理占用你时间的繁琐任务：为未测试的代码编写测试、修复项目各处的 lint 错误、解决合并冲突、更新依赖、撰写发布说明。

```
claude "write tests for the auth module, run them, and fix any failures"
```

**构建功能、修复 bug**：用自然语言描述你想要的。Claude Code 会规划方案、跨多个文件编写代码，并验证其可用。对于 bug，粘贴错误信息或描述症状，Claude Code 会在你的代码库中追踪问题、定位根因并实现修复。更多示例见常用工作流。

**创建提交与拉取请求**：Claude Code 直接与 git 协作。它暂存更改、撰写提交信息、创建分支并打开拉取请求。

```
claude "commit my changes with a descriptive message"
```

在 CI 中，你可以用 GitHub Actions 或 GitLab CI/CD 自动化代码评审与问题分类。

**用 MCP 连接你的工具**：模型上下文协议（Model Context Protocol，MCP）是连接 AI 工具与外部数据源的开放标准。借助 MCP，Claude Code 可以读取 Google Drive 中的设计文档、更新 Jira 中的工单、从 Slack 拉取数据，或使用你自己的自定义工具。

**用指令、技能与钩子自定义**：CLAUDE.md 是添加到项目根目录的 markdown 文件，Claude Code 在每个会话开始时读取它。用它设定编码标准、架构决策、首选库与评审清单。Claude 还会在工作时建立自动记忆，跨会话保存构建命令、调试洞察等学习成果，而无需你手动书写。你可以创建自定义命令来封装团队可共享的可复用工作流（如 /review-pr 或 /deploy-staging）。钩子（Hooks）让你在 Claude Code 动作前后运行 shell 命令，例如每次文件编辑后自动格式化，或提交前运行 lint。

**运行智能体团队、构建自定义智能体**：同时生成多个 Claude Code 智能体，分别处理任务的不同部分。一个主智能体协调工作、分配子任务、合并结果。对于完全自定义的工作流，Agent SDK 让你基于 Claude Code 的工具与能力构建自己的智能体，并完全掌控编排、工具访问与权限。

**用 CLI 管道、脚本化与自动化**：Claude Code 可组合，遵循 Unix 哲学。把日志管道传给它、在 CI 中运行它，或与其他工具串联：

```
# 分析最近的日志输出
tail -200 app.log | claude -p "Slack me if you see any anomalies"
# 在 CI 中自动化翻译
claude -p "translate new strings into French and raise a PR for review"
# 跨文件批量操作
git diff main --name-only | claude -p "review these changed files for security issues"
```

完整命令与标志见 CLI 参考。

**安排重复任务**：让 Claude 按计划运行以自动化重复工作：早间 PR 评审、夜间 CI 失败分析、每周依赖审计，或 PR 合并后同步文档。云计划任务运行在 Anthropic 管理的基础设施上，即使电脑关机也能持续运行。可从 Web、桌面应用或 CLI 中运行 /schedule 创建。桌面计划任务运行在你的机器上，可直接访问本地文件与工具。`/loop` 在 CLI 会话内重复某个提示词以快速轮询。

**随处办公**：会话不绑定单一入口。随着上下文变化，可在环境之间迁移工作：离开办公桌后，用 Remote Control 通过手机或任意浏览器继续工作；用 Message 从手机派发任务并打开其创建的桌面会话；在 Web 或 iOS 应用上启动长时间任务，再用 `claude --teleport` 拉进终端；用 `/desktop` 把终端会话交给桌面应用进行可视化 diff 评审；从团队聊天路由任务：在 Slack 中 @Claude 提交 bug 报告，即可收到拉取请求。

## 随处使用 Claude Code

每个入口都连接到同一个底层 Claude Code 引擎，因此你的 CLAUDE.md 文件、设置与 MCP 服务器在所有入口间通用。除上述终端、VS Code、JetBrains、桌面与 Web 环境外，Claude Code 还与 CI/CD、聊天与浏览器工作流集成：

| 我想…… | 最佳选择 |
|---|---|
| 从手机或其他设备继续本地会话 | Remote Control |
| 把 Telegram、Discord、iMessage 或自有 webhook 的事件推送到会话 | Channels |
| 本地启动任务、在移动端继续 | Web 或 Claude iOS 应用 |
| 按重复计划运行 Claude | 云计划任务或桌面计划任务 |
| 自动化 PR 评审与问题分类 | GitHub Actions 或 GitLab CI/CD |
| 每个 PR 自动获得代码评审 | GitHub Code Review |
| 把 Slack 中的 bug 报告路由为拉取请求 | Slack |
| 调试线上 Web 应用 | Chrome |
| 为自己的工作流构建自定义智能体 | Agent SDK |

## 下一步

安装 Claude Code 后，以下指南可助你深入：

- 快速开始：走完第一个真实任务，从探索代码库到提交修复
- 存储指令与记忆：用 CLAUDE.md 文件与自动记忆给 Claude 持久化指令
- 常用工作流与最佳实践：最大化发挥 Claude Code 的模式
- 设置：为你的工作流自定义 Claude Code
- 故障排查：常见问题的解决方案
- code.claude.com：演示、定价与产品详情
