---
来源：GitHub
链接：https://github.com/kepano/obsidian-skills
时间：2026-09-11
平台：GitHub
tags: [GitHub, Obsidian, AI实操, Agent]
---

# kepano/obsidian-skills — 教 AI 用 Obsidian

> 触发素材：公众号「私人定制助理服务」08-21《obsidian-skills 4.6万星：教AI用Obsidian》（每日爆款情报 2026-09-10 篇3）。本条为 GitHub 一手实测记录，星数等数据以本日实查为准。

## 仓库实况（2026-09-11 api.github.com 实查）

- 地址：github.com/kepano/obsidian-skills
- 作者：kepano（Steph Ango，Obsidian CEO/联合创始人）
- Stars：**48,137**（公众号文章写稿时为 4.6 万，一周涨约 2000）
- 简介：Agent skills for Obsidian. Teach your agent to use Obsidian CLI and open formats
- 规格：遵循 agentskills.io 规范，兼容任何 skills 兼容 Agent（Claude Code / Codex / Open Code 等）

## 6 个技能

| 技能 | 用途 |
|------|------|
| obsidian-markdown | Obsidian 风味 Markdown：wikilink、embed、callout、属性 |
| obsidian-bases | .base 数据库视图：views/filters/formulas/summaries（499 行最大技能） |
| json-canvas | .canvas 白板：nodes/edges/groups |
| obsidian-cli | 驱动运行中的 Obsidian：读/写/搜/属性/任务/插件开发/dev:截图 |
| defuddle | 网页→干净 Markdown（省 token），kepano 自家工具 |
| knap | 模板+JSON/CSV→批量渲染 Markdown 笔记 |

## 安装方式（README 原文）

- Marketplace：`/plugin marketplace add kepano/obsidian-skills` → `/plugin install obsidian@obsidian-skills`
- npx：`npx skills add git@github.com:kepano/obsidian-skills.git`
- 手动：把 skills/ 拷进 Agent 的技能目录

## Obsidian CLI 关键事实（help.obsidian.md/cli，en 文档已全文转存 /tmp/obsidian-help）

- "Anything you can do in Obsidian can be done from the command line."
- CLI 二进制在 app 包内：`/Applications/Obsidian.app/Contents/MacOS/obsidian-cli`（1.12+ 安装器自带），软链到 /usr/local/bin 即用
- 启用路径：Settings → General → 打开 Command line interface → 按提示注册（GUI 操作，无配置文件写法；状态存主进程内存 D.cli，经 IPC 'cli' 通道切换）
- 要求 Obsidian 应用正在运行；TUI 支持自动补全/历史/Ctrl+R
- 常用命令：read / create / append / search / daily / daily:append / property:set / tasks / tags counts / backlinks / diff；开发向：plugin:reload / dev:errors / dev:screenshot / dev:dom / dev:console / eval
- 参数用 `key=value`（带空格加引号），flag 是裸开关；`file=` 按 wikilink 解析，`path=` 按 vault 根路径

## 本机实测记录（2026-09-11）

- Obsidian 1.13.7 已装且运行中，vault=/Users/pilot/Documents/bsidian-vault（唯一 vault）
- CLI 未启用（"Command line interface is not enabled"），待用户 GUI 打开后补测
- defuddle 0.19.3 / knap 0.4.1 已装（~/.npm-global，系统 npm 目录 EACCES 需改用户 prefix）
- defuddle 实测：stephango.com/vault 原始 HTML 24,411 字节 → Markdown 11,254 字节，**省 54%**
- knap 实测：读书卡模板 + JSON 2 条 → 2 张完整笔记（frontmatter/callout/块ID 全对）
- json-canvas 实测：为 vault 生成 知识库流水线.canvas（6 节点 6 边，引用全校验通过）
- obsidian-bases 实测：生成 知识库体检.base（3 视图：全表/30天遗忘预警/灵感卡片）
