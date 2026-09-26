# C1 翻译项目

把一批英文技术文章翻译成简体中文，统一术语、保留关键数据与代码块，并全程记录 AI 协作日志与复盘。

## 项目背景

材料来源是斯坦福 **CS146S《The Modern Software Developer》(Fall 2025)** 的离线课程资料：一个围绕「氛围编程（Vibe Coding）/ AI 辅助软件开发」的技术文章合集，共 **31 篇**原始英文文章，主题涵盖提示词工程、上下文工程、MCP、SRE、AI 安全等。

## 目录结构

```
C1_翻译项目/
├── README.md            本文件
├── glossary.md          术语表（61 条，全文翻译的统一依据）
├── AI日志.md            逐日 AI 协作日志（Day 1–4，含工具/Prompt/踩坑/教训）
├── source/              原始英文材料（31 篇）
├── translated/          译文（27 篇 Markdown）+ .parts/ 分片临时文件
└── scripts/             翻译与校验脚本
    ├── extract.py              HTML → 纯文本提取
    ├── translate_prompt.md     固定翻译指令模板
    ├── check_headings.py       标题数对照（漏译初筛）
    ├── check_headings_detail.py 标题明细
    └── check_fidelity.py       字符占比（编译忠实度粗检）
```

## 翻译范围与口径

| 项 | 说明 |
| -- | -- |
| 源文总量 | 31 篇英文文章 |
| 实际译文 | **27 篇** |
| 占位/空文件 | **4 篇**，无需翻译（详见下） |
| 术语表 | 61 条，全文强制统一 |

4 篇占位/空文件（抓取时未拿到真实正文，已在 AI 日志中说明）：

- `good-context-good-code.md` —— Ghost 博客「Enter access code」登录壳页
- `how-warp-uses-warp.md` —— Notion 页面
- `lessons-from-ai-code-reviews.md` —— 完全空文件
- `peeking-under-the-hood-of-claude-code.md` —— Medium 付费墙（自动抓取被拦截）

## 翻译规范（术语表约定）

1. 术语首次出现：中文 +（英文原文），如「模型上下文协议（Model Context Protocol，MCP）」。
2. 专有名词保留英文：GitHub、Kubernetes、Claude、Copilot、Devin、Warp、Semgrep、Anthropic、OpenAI 等。
3. 代码、命令、文件路径不翻译；标题/列表层级、关键数据原文保留。
4. 全项目以 `glossary.md` 为准；要改译法，先改术语表再全局替换。

## 工作流程（可复跑）

1. **正文提取**：`scripts/extract.py` 把 HTML 剥成纯文本（跳过 script/style/nav/header/footer 等非正文标签）。
2. **翻译**：按 `scripts/translate_prompt.md` 固定模板（术语表 + 原文）逐篇翻译；超长文章分片写盘到 `translated/.parts/`，再合并。
3. **校验**：`check_headings.py`（标题数对照）、`check_fidelity.py`（字符占比）、`check_headings_detail.py`（标题明细）+ 定向核对关键数字与术语残留。

## 复盘

完整的过程复盘（学到了什么、流程、与 AI 的协作、卡点与突破、改进方向）见七维 AAR，逐日细节见 `AI日志.md`。
