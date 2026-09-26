# C1 AI 日志（AI Log）

> 挑战要求：逐日记录「用了什么工具、什么 prompt、踩了什么坑」。
> 记录原则：真实、当天写、不事后美化。

---

## Day 1 · 2026-09-26 · 清点材料 + 搭翻译管线 + 首批翻译

### 今天做了什么

1. 清点离线课程材料：确认这是斯坦福 CS146S《The Modern Software Developer》(Fall 2025)。
   - `pages/` 31 篇 HTML 文章、`pdfs/` 3 个 PDF、`index.html` 课程主页、`Vibe_Coding_Playbook.pdf`。
2. 逐篇检查 HTML 正文，**踩到第一个坑**：部分文章抓下来只有 Ghost 博客的"Enter access code"登录壳，没有正文。
   - 排查方法：用 Python 剥掉 `<script>`/`<style>`/标签后统计纯文字长度。
   - 结论：27 篇有正文、4 篇是空壳（`good-context-good-code`、`how-warp-uses-warp`、`lessons-from-ai-code-reviews`、`peeking-under-the-hood-of-claude-code`）。
3. 建立术语表 `glossary.md`（61 条），核心术语如 Vibe Coding→氛围编程、Context Engineering→上下文工程、MCP→模型上下文协议。
4. 写了正文提取脚本 `scripts/extract.py`（HTML→纯文本，可复跑）。
5. 写了翻译指令模板 `scripts/translate_prompt.md`（固定 prompt + 术语表 + 原文）。
6. 按模板翻了第一篇 `warp-vs-claude-code.md`。

### 用了什么工具 / Prompt

- **正文提取**：Python 脚本（`html.parser`，跳过 script/style/nav/header/footer 等非正文标签）。
- **翻译 prompt（核心）**：专业科技翻译指令——术语强制用术语表、专有名词保留英文、忠实原文不增删、保留标题/列表层级、代码命令不翻、只输出译文。

### 踩的坑 / 教训

1. **离线缓存的 HTML 不等于都有正文**。抓取器会把需要登录/访问码的页面也存下来，直接翻会翻出一堆"Enter access code"垃圾。教训：翻译前必须先做"正文量体检"。
2. **大文件是假象**：`prompt-engineering-overview.html` 有 2MB，但那是内嵌图片/字体撑的，纯文字只有 2.3 万字。不能看文件大小判断工作量，要看"剥标签后的字数"。

### 下一步

- 按正文量从小到大批量翻译剩余 26 篇。
- 每篇翻译后用术语表做一次"术语一致性抽检"。

---

## Day 2 · 2026-09-26 · 批量翻译 + 分片合并流程

### 今天做了什么

1. 建立「长文分片翻译 → 接缝校验 → 合并 → 验证」的可复跑流程，应对超长文章单次输出截断的问题。
2. 完成多篇长文翻译并合并（累计已译 **22** 篇，剩余 **9** 篇 = 5 篇有正文 + 4 篇占位/空文件）：
   - `how-to-review-code-effectively.md`
   - `sast-vs-dast.md`
   - `agentic-ai-threats.md`（Unit 42：AI Agent 9 类攻击场景 + 5 类缓解）
   - `devin-coding-agents-101.md`
   - `writing-effective-tools-for-agents.md`（Anthropic：如何为智能体写高效工具）
3. 统一处理各站点页脚样板（"Looking to learn more?"、"Get the developer newsletter"、"### Tags"、Palo Alto 品牌区等），译文正文一律在样板前截止。

### 用了什么工具 / Prompt

- 固定翻译模板 `scripts/translate_prompt.md` + 术语表 `glossary.md`（61 条）。
- 分片写盘到 `translated/.parts/*.partNN.md`，用 PowerShell `Get-Content -Raw -Encoding UTF8` + `WriteAllText`（UTF8 无 BOM）合并。
- 合并后自动化校验：字符/行数、乱码检测、分片接缝、关键章节标题去重、页脚样板排除。

### 踩的坑 / 教训

1. 超长文章（5 万字+）单轮读取会触发结果读取预算上限（4K-token read budget），分段读取仍可能卡住；对策是分片写盘、逐片确认接缝，磁盘文件为准，对话里被截断的显示不可靠。
2. 不同站点正文边界不同（Ghost 博客 vs 厂商官网），翻译前必须先锁定「正文到哪一行结束」，否则会把 newsletter/推荐阅读等样板一并翻进去。

### 下一步

- 继续翻译剩余 5 篇有正文的文章。
- 4 篇空壳文件（`good-context-good-code`、`how-warp-uses-warp`、`lessons-from-ai-code-reviews`、`peeking-under-the-hood-of-claude-code`）已在 Day 1 说明，最终 README/AAR 里注明即可。
- 全部译完后做术语一致性抽检 + 校对。

---

## Day 3 · 2026-09-26 · 继续批量翻译 + 剩余文件盘点

### 今天做了什么

1. 完成 `prompt-engineering-overview.md`（Google Cloud 提示工程指南）的分片翻译与合并。
   - 源文 24,322 字符、627 行；正文截止线 567（其后为 Google Cloud 页脚样板，已排除）。
   - 源文表格被重复渲染（如 Q&A 表 ~142–211 行重复），译文去重为单次渲染。
2. 合并 4 个分片到 `translated/prompt-engineering-overview.md`，自动化校验通过：
   - 无乱码（锟斤拷 / U+FFFD / â€ 均未检出）；
   - 无页脚样板（Start your AI journey / See all products / free credits 均未出现）；
   - 三段分片接缝连续；
   - 表格数据行 35 行、0 重复。
3. 盘点剩余文件：累计已译 **23** 篇，剩余 **8** 篇 = 4 篇有正文 + 4 篇占位/空文件。

### 用了什么工具 / Prompt

- 固定翻译模板 `scripts/translate_prompt.md` + 术语表 `glossary.md`（61 条）。
- 分片写盘 `translated/.parts/*.partNN.md` → PowerShell `Get-Content -Raw` + `WriteAllText`（UTF8 无 BOM）合并。
- 合并后校验：字符数、乱码检测、页脚样板排除、分片接缝、表格数据行去重。

### 踩的坑 / 教训

1. **源文重复渲染表格**：厂商官网抓取的文章里同一张表会以两种格式各渲染一次（例如 Q&A 表 ~142–211 行重复），直接翻会翻出两份。教训：翻译前先比对源文表格是否重复，译文去重为单次渲染。
2. **表头跨表重复 ≠ 重复渲染**：去重校验时「场景/说明/示例提示词」这类表头行会在多张表里各出现一次，属于正常；只统计「数据行」才能准确判断是否真的重复。

### 下一步

- 继续翻译剩余 4 篇有正文的文章（按正文量从小到大）：
  - `finding-vulnerabilities-claude-codex.md`（26,247 字符）
  - `sre-introduction.md`（26,552 字符）
  - `mcp-introduction.md`（31,877 字符）
  - `context-rot.md`（51,232 字符）
- 4 篇占位/空文件已在 Day 1 说明，最终 README/AAR 里注明即可。

## Day 4 —— 完成剩余正文翻译 + 质量抽检

### 做了什么

1. **翻译剩余 4 篇正文文章**（分片写盘 → PowerShell 合并，流程同前）：
   - `finding-vulnerabilities-claude-codex.md`（Semgrep「用 AI 找漏洞」研究，26,247 字符 → 译文 10,333 字符）
   - `sre-introduction.md`（Google SRE 第 1 章，26,552 字符 → 译文 7,238 字符）
   - `mcp-introduction.md`（MCP 开发者入门，31,877 字符 → 译文 28,096 字节）
   - `context-rot.md`（Chroma「Context Rot」研究，51,232 字符 → 译文 18,687 字符）
2. **确认 4 篇占位/空文件无需翻译**：
   - `good-context-good-code.md` = Ghost 访问码壳页（`Enter access code`）
   - `how-warp-uses-warp.md` = Notion 页面
   - `lessons-from-ai-code-reviews.md` = 完全空文件
   - `peeking-under-the-hood-of-claude-code.md` = Medium 付费墙（自动抓取被拦截）
3. **质量抽检**（`check_fidelity.py` / `check_headings.py` / `check_headings_detail.py` + 定向核对）：
   - 编码：全部译文 UTF-8 无乱码；PowerShell 控制台 GBK 显示乱码 ≠ 文件损坏，`read_file` 读出干净。
   - 关键数据：`finding-vulnerabilities` 的 46 / 14% / 86%、21 / 18% / 82%、445、各分类 TPR 全部保留。
   - 术语：`context-rot` 全文无 `Project Gutenberg` 残留，PG 术语已正确落地。
   - 英文残留：无未翻译的 `Dive deeper` 等英文标题。
   - 标题数脚本标出的「疑似漏译」经逐条甄别，全部是页脚/导航/相关推荐/目录等样板噪音，非正文漏译；`ai-code-review` 的 9 个 FAQ 问题已全部译出。

### 用了什么工具 / Prompt

- 分片写盘 `translated/.parts/*.partNN.md` → `Get-Content -Raw` + `WriteAllText`（UTF8 无 BOM）合并。
- 校验脚本：`check_headings.py`（标题数对照）、`check_fidelity.py`（字符占比）、`check_headings_detail.py`（标题明细）。
- 定向 `IndexOf` 核对关键数字与术语残留。

### 踩的坑 / 教训

1. **批量翻译前要先甄别占位/空文件**：抓取到的源文件里混入了 Ghost 壳页、Notion 页面、空文件、Medium 付费墙，直接翻译会浪费 token 或产出无效内容。教训：先扫一遍源文件是否真的有正文。
2. **标题数脚本的假阳性**：`check_headings.py` 用「源标题数 vs 译标题数」判漏译，会把翻译时应剔除的页脚/导航/相关推荐/目录误判为漏译。教训：脚本报错后要回看源文件逐条甄别，不能盲信数字。
3. **控制台乱码 ≠ 文件损坏**：PowerShell 用 GBK 解码 UTF-8 中文会显示乱码。教训：判断编码用 `read_file` 或指定 UTF-8 读取，别被控制台显示误导。

### 最终盘点

- 源文件 **31** 篇；译文 **27** 篇；占位/空文件 **4** 篇（无需翻译）。
- 术语表 `glossary.md` 61 条。

### 下一步

- 完成 README、七维 AAR（≥3 条示例），打包提交 C1 挑战。
