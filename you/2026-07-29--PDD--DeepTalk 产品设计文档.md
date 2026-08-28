---
type: prd
status: sprouting
tags: [自我访谈, AI智能体, 产品设计, 架构]
---

# DeepTalk — 产品设计文档（PDD）

> **版本：** v1.0  
> **日期：** 2026-07-29  
> **依赖：** [DeepTalk Agent PRD v2](./2026-07-29--PRD--DeepTalk Self Agent 产品需求说明书.md)  
> **作者：** 飞叔  

---

## 文档导航

| 章节 | 内容 | 读者 |
|------|------|------|
| 一、整体架构 | 系统全景图、分层关系、核心流程 | 所有人 |
| 二、业务架构 | 能力域、业务流程、服务蓝图 | 产品经理 |
| 三、技术架构 | 模块设计、组件交互、部署方案 | 开发工程师 |
| 四、数据架构 | 数据模型、存储策略、流转路径 | 后端/数据工程师 |

---

# 一、整体架构

## 1.1 系统全景

```
                         用户
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                  ▼
   ┌─────────┐      ┌─────────┐       ┌──────────┐
   │  CLI    │      │ Feishu  │       │ Telegram │  ← 多端接入
   │(主入口) │      │(未来)   │       │(未来)    │
   └────┬────┘      └────┬────┘       └────┬─────┘
        │                │                 │
        └────────────────┼─────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   表示层（Interface）  │
              │  - CLI 交互循环        │
              │  - 会话管理            │
              │  - 输出渲染            │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   编排层（Orchestra）  │
              │  - Agent Loop 状态机   │
              │  - 工具调度            │
              │  - 上下文窗口管理       │
              └──────────┬──────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   ┌────────────┐ ┌────────────┐ ┌────────────┐
   │  工具层     │ │  模型层     │ │  记忆层     │
   │ (Tools)    │ │ (LLM)      │ │ (Memory)   │
   └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
         │              │              │
         └──────────────┼──────────────┘
                        │
                        ▼
              ┌─────────────────────┐
              │   持久化层            │
              │  - 文件系统 (memory/) │
              │  - SQLite (sessions/) │
              │  - YAML (config/)    │
              └─────────────────────┘
```

## 1.2 分层职责

| 层 | 职责 | 输入 | 输出 | 关键技术 |
|----|------|------|------|---------|
| 表示层 | 接收用户输入、渲染 Agent 回复 | 键盘输入 | 格式化文本 | prompt_toolkit, rich |
| 编排层 | Agent Loop 状态机，工具调度决策 | 用户输入 + 记忆上下文 | 工具调用指令 | Python 状态机 |
| 工具层 | 执行专用访谈工具 | 工具调用指令 | 工具执行结果 | 规则引擎 + LLM |
| 模型层 | LLM API 调用 | 提示词 + 上下文 | LLM 文本回复 | OpenAI SDK |
| 记忆层 | 管理热/温/冷三层记忆 | 工具读写请求 | 记忆数据 | 文件系统 I/O |
| 持久化层 | 数据落盘 | 结构化数据 | 文件 / 数据库行 | YAML, SQLite, MD |

## 1.3 核心流程（一次完整对话）

```
时间线                    系统动作                         涉及组件
──────────────────────────────────────────────────────────────────
T+0s     用户执行 deeptalk
T+0.1s   → 加载 config.yaml                               配置层
T+0.2s   → 加载 profile.md + timeline.md                  记忆层→热记忆
T+0.3s   → 注入系统提示词 + 记忆摘要                        编排层→LLM上下文
T+0.5s   → 展示开场白                                      表示层
         「距上次对话已过7天。最近有什么事在你脑子里转？」

T+5s     用户输入：「在想换工作...」
T+5.1s   → 追加到会话上下文                                 编排层
T+5.2s   → 触发 probe_decide 工具                         工具层
          检测到模糊信号：「在想」+ 话题重大
T+5.3s   → Agent 生成追问                                  模型层
         「你提到换工作——是有什么具体的事情触发了这个想法？」

T+15s    用户输入：「老板上周把我做的项目砍了」
T+15.1s  → 追加到会话上下文
T+15.2s  → 触发 question_pick 工具                        工具层
          基于「项目被砍」→ 匹配维度：D1 决策逻辑 / D5 防御机制
T+15.3s  → 选择问题：D5 「当努力的结果被否定时，你的第一反应是什么？」 
T+15.4s  → Agent 提问                                     模型层

...（循环 10-15 轮）...

T+10min  → should_close() 返回 True                       编排层
          （超过 15 轮 或 用户说累了）
T+10.1s  → 触发 session_summarize 工具                    工具层
T+10.2s  → Agent 展示总结 + 收尾问题                       模型层→表示层

T+10.5s  → 后台异步执行 Reflect                            编排层
           ├─ memory_save → 更新 profile.md                记忆层→冷记忆
           ├─ 追加 timeline.md
           ├─ pattern_detect → 更新 patterns.md            工具层
           └─ evolution_track → 写 evolution-log.md        工具层
```

---

# 二、业务架构

## 2.1 能力域地图

```
DeepTalk 能力域
│
├── 对话能力 ──────────────────────────────
│   ├── 暖场（基于距上次对话时间定制开场白）
│   ├── 访谈（问→听→判→追→转 循环）
│   ├── 追问（≤2层深挖，信号驱动）
│   ├── 收尾（总结 + 用户自评）
│   └── 情绪感知（检测敷衍/回避/兴奋/低落）
│
├── 记忆能力 ──────────────────────────────
│   ├── 短期记忆（会话内上下文，不超过 15 轮）
│   ├── 长期记忆（跨会话画像，持续更新）
│   ├── 模式识别（从多次对话中提取行为模式）
│   └── 记忆演化（标记陈旧、确认矛盾、记录转折）
│
├── 知识能力 ──────────────────────────────
│   ├── 题库管理（63 题 + 自进化）
│   ├── 维度框架（7 维度 × 关键词体系）
│   ├── 追问策略（决策树 + 模板库）
│   └── 画像融合（四家哲学对照表）
│
├── 进化能力 ──────────────────────────────
│   ├── 题库进化（低质量淘汰 + 新题候选 + 验证入库）
│   ├── 策略进化（失败聚类 + 策略调整 + 回归验证）
│   └── 画像进化（发现→确认→稳定→预测）
│
└── 分发能力（Phase 4）────────────────────
    ├── pip 安装
    ├── 首次设置向导
    └── 多平台 Gateway
```

## 2.2 业务流程图（服务蓝图）

```
用户旅程              前台交互             后台处理              支撑系统
──────────────────────────────────────────────────────────────────
                       
[安装] ──────────→ pip install deeptalk
                         │
                         ▼
[首次配置] ──────→ 设置向导             创建 ~/.deeptalk/       文件系统
                  选 Provider           写 config.yaml
                  输 API Key            初始化 skills/
                                        初始化 memory/
                         │
                         ▼
[日常对话] ──────→ deeptalk             memory_load            文件系统
                         │              question_pick          题库引擎
                         ▼
                   对话循环              probe_decide           追问引擎
                   (10-15轮)            上下文管理              LLM API
                         │
                         ▼
[收尾] ─────────→ 看到总结              session_summarize       LLM API
                  回答自评              追加 timeline.md        文件系统
                         │
                         ▼
[后台]                              ───→ portrait_update        LLM API
                                        pattern_detect          规则引擎
                                        更新 profile.md         文件系统
                         │
                         ▼
[下次对话] ──────→ deeptalk             memory_load            文件系统
                  「上次聊到...」        加载最新画像
```

## 2.3 用户状态机（生命周期）

```
                  ┌──────────┐
      安装后 ──→ │  新用户   │
                  └────┬─────┘
                       │ 完成首次设置向导
                       ▼
                  ┌──────────┐
                  │  活跃用户  │ ←── 每周对话 1-2 次
                  └────┬─────┘
                       │
            ┌──────────┼──────────┐
            ▼                     ▼
       ┌──────────┐         ┌──────────┐
       │  沉默用户  │         │  深度用户  │
       │ >14天未聊  │         │ >20次对话  │
       └────┬─────┘         └────┬─────┘
            │                    │
       cron 提醒             画像预测模式
       「好久没聊了」         画像导出需求
            │
            ▼
       ┌──────────┐
       │  流失用户  │
       │ >30天未聊  │
       └──────────┘
```

---

# 三、技术架构

## 3.1 技术选型总览

| 层级 | 选型 | 版本 | 理由 |
|------|------|------|------|
| 语言 | Python | ≥3.11 | LLM 生态成熟，跨平台 |
| CLI | prompt-toolkit | ≥3.0 | 终端输入体验（历史、补全、多行） |
| 终端渲染 | rich | ≥13.0 | Markdown 渲染、面板、进度条 |
| LLM SDK | openai | ≥1.0 | 兼容 DeepSeek / Claude / OpenAI |
| 数据校验 | pydantic | ≥2.0 | 配置/记忆/工具参数校验 |
| 配置 | PyYAML | ≥6.0 | 人类可读 |
| 会话 | SQLite | 内置 | 零依赖，嵌入式 |
| 打包 | setuptools + pip | — | 标准分发 |
| 测试 | pytest | ≥8.0 | 标准测试框架 |

**不选的技术和理由：**
- FastAPI / Flask：不需要 HTTP 服务，纯 CLI
- PostgreSQL / Redis：单用户本地运行，不需要网络数据库
- Docker：单机 CLI 工具，不需要容器化
- Node.js / TypeScript：LLM 生态 Python 更强

## 3.2 模块结构

```
src/deeptalk/
│
├── cli/                        # ── 表示层 ──
│   ├── __init__.py
│   ├── app.py                  # CLI 主循环（prompt_toolkit Application）
│   ├── renderer.py             # 终端渲染（rich Markdown）
│   └── styles.py               # 终端样式定义
│
├── agent/                      # ── 编排层 ──
│   ├── __init__.py
│   ├── loop.py                 # Agent Loop 状态机（核心）
│   ├── states.py               # 状态枚举 + 转换规则
│   └── context.py              # 上下文窗口管理（token 计数 + 截断）
│
├── tools/                      # ── 工具层 ──
│   ├── __init__.py
│   ├── registry.py             # 工具注册表（ToolRegistry）
│   ├── base.py                 # 工具基类（Tool ABC）
│   ├── memory_tools.py         # memory_load / memory_save
│   ├── interview_tools.py      # question_pick / probe_decide / probe_generate
│   └── analysis_tools.py       # pattern_detect / portrait_update / evolution_track
│
├── memory/                     # ── 记忆层 ──
│   ├── __init__.py
│   ├── system.py               # MemorySystem（统一接口）
│   ├── loader.py               # 冷→热记忆加载
│   ├── saver.py                # 热→冷记忆保存
│   ├── models.py               # Profile / Timeline / Pattern / EvolutionLog 模型
│   └── compressor.py           # 记忆压缩（去重 + 摘要）
│
├── skills/                     # ── 知识层 ──
│   ├── __init__.py
│   ├── library.py              # SkillLibrary（加载 + 查询）
│   ├── questions.py            # 题库管理器（选題 + 进化）
│   ├── probes.py               # 追问引擎（决策树 + 模板）
│   └── synthesis.py            # 画像合成（四家融合）
│
├── llm/                        # ── 模型层 ──
│   ├── __init__.py
│   ├── client.py               # LLM 客户端
│   ├── prompts.py              # 系统提示词模板
│   └── retry.py                # 重试 + 超时策略
│
├── config/                     # ── 配置层 ──
│   ├── __init__.py
│   ├── loader.py               # YAML 配置加载
│   ├── schema.py               # 配置模型（pydantic）
│   └── defaults.py             # 默认值
│
├── session/                    # ── 持久化层 ──
│   ├── __init__.py
│   └── store.py                # SQLite 会话存储
│
└── main.py                     # 入口（deeptalk 命令）
```

## 3.3 核心组件详细设计

### 3.3.1 Agent Loop 状态机

```python
from enum import Enum, auto

class AgentState(Enum):
    WARM = auto()       # 预热：加载记忆
    OPEN = auto()       # 开场：生成开场白
    ASK = auto()        # 提问：选择并发送问题
    LISTEN = auto()     # 倾听：等待用户输入
    DECIDE = auto()     # 判断：分析回答，决定下一步
    PROBE = auto()       # 追问：生成并发送追问
    SWITCH = auto()      # 转向：切换维度
    CLOSE = auto()       # 收尾：总结 + 告别
    REFLECT = auto()     # 反思：后台更新记忆

# 状态转换表
TRANSITIONS = {
    AgentState.WARM:    [AgentState.OPEN],
    AgentState.OPEN:    [AgentState.ASK],
    AgentState.ASK:     [AgentState.LISTEN],
    AgentState.LISTEN:  [AgentState.DECIDE],
    AgentState.DECIDE:  [AgentState.PROBE, AgentState.SWITCH, AgentState.ASK, AgentState.CLOSE],
    AgentState.PROBE:   [AgentState.LISTEN],
    AgentState.SWITCH:  [AgentState.ASK],
    AgentState.CLOSE:   [AgentState.REFLECT],
    AgentState.REFLECT: [],  # 终态
}
```

### 3.3.2 工具注册表

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable

@dataclass
class ToolSchema:
    name: str
    description: str           # LLM 可见的工具描述
    parameters: dict           # JSON Schema
    loop_phase: AgentState     # 工具在哪个阶段可用
    requires_llm: bool         # 是否需要 LLM 辅助

class Tool(ABC):
    schema: ToolSchema

    @abstractmethod
    def execute(self, **params) -> dict:
        """执行工具，返回结构化结果"""
        ...

class ToolRegistry:
    """工具注册表。工具不进 LLM tool_use —— Agent Loop 自己决定何时调用。"""

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.schema.name] = tool

    def get(self, name: str) -> Tool:
        return self._tools[name]

    def for_phase(self, phase: AgentState) -> list[Tool]:
        return [t for t in self._tools.values() if t.schema.loop_phase == phase]
```

### 3.3.3 记忆加载流程

```python
class MemorySystem:
    def load_for_session(self) -> dict:
        """Warm 阶段调用。返回注入 LLM 上下文的记忆摘要。"""
        profile = self._read_md("memory/profile.md")
        timeline = self._read_md("memory/timeline.md")
        patterns = self._read_md("memory/patterns.md")

        # 只注入摘要，不注入全文（节省 token）
        return {
            "profile_summary": self._summarize_profile(profile),
            "last_session": self._last_timeline_entry(timeline),
            "key_patterns": self._active_patterns(patterns),
        }

    def save_after_session(self, session_data: dict):
        """Reflect 阶段调用。"""
        # 1. 更新 profile.md（如有新发现）
        # 2. 追加 timeline.md
        # 3. 更新 patterns.md（如有新规律）
        # 4. 追加 evolution-log.md
```

### 3.3.4 LLM 客户端

```python
class LLMClient:
    def __init__(self, config: LLMConfig):
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,  # 兼容 DeepSeek / 自定义 endpoint
        )
        self.model = config.model
        self.max_tokens = config.max_tokens

    def chat(self, messages: list[dict], system: str = None) -> str:
        """发送消息，返回 LLM 回复文本。

        DeepTalk 不使用 function calling —— LLM 回复就是对话文本。
        工具调用由 Agent Loop 状态机管理，不交给 LLM 决定。
        """
        full_messages = []
        if system:
            full_messages.append({"role": "system", "content": system})
        full_messages.extend(messages)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content
```

## 3.4 部署方案

```
用户机器
│
├── ~/.deeptalk/
│   ├── config.yaml         ← 用户配置（模型、API key）
│   ├── memory/             ← 用户数据（画像、时间线）
│   ├── skills/             ← 系统知识库（安装时写入，用户可扩展）
│   └── sessions/           ← 会话记录（SQLite）
│
├── pip 安装路径
│   └── deeptalk/           ← 系统代码（只读，pip 管理）
│
└── ~/.bashrc / ~/.zshrc
    └── deeptalk 命令        ← 由 pip 自动注册
```

**不使用服务端部署。** 所有数据在用户本地。LLM API 调用走用户自己的 API Key。

## 3.5 测试策略

```
tests/
├── unit/
│   ├── test_states.py          # 状态机转换规则
│   ├── test_memory_models.py   # 记忆数据模型
│   ├── test_tools.py           # 每个工具的输入/输出
│   ├── test_questions.py       # 题库选择逻辑
│   └── test_probes.py          # 追问判定逻辑
├── integration/
│   ├── test_loop.py            # Agent Loop 完整流程（mock LLM）
│   ├── test_memory_flow.py     # 记忆加载→更新 完整流程
│   └── test_skill_flow.py      # 题库→追问→画像 完整流程
└── e2e/
    └── test_cli.py             # CLI 端到端测试（真实 LLM，手动触发）
```

---

# 四、数据架构

## 4.1 数据模型全景

```
                    ┌──────────────┐
                    │   config     │
                    │   .yaml      │  静态配置（安装时创建，用户编辑）
                    └──────────────┘

┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   profile    │   │  timeline    │   │  patterns    │
│   .md        │   │  .md         │   │  .md         │
│              │   │              │   │              │
│ 1:1 用户     │   │ 1:N 对话     │   │ 1:N 维度     │
│ 持续更新     │   │ 追加写入     │   │ 持续更新     │
└──────────────┘   └──────────────┘   └──────────────┘

┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│evolution-log │   │  questions   │   │   session    │
│  .md         │   │  .md         │   │   .db        │
│              │   │              │   │  (SQLite)    │
│ 追加写入     │   │ 持续更新     │   │              │
│ 只增不改     │   │ (含进化)     │   │ 每次对话一条  │
└──────────────┘   └──────────────┘   └──────────────┘
```

## 4.2 核心实体

### 4.2.1 Profile（个人画像）

```
Profile 1:1 User
─────────────────
id: string (uuid)
name: string
created_at: datetime
updated_at: datetime
session_count: int
one_liner: string              # 一句话概括
dimensions: list[Dimension]    # 7 个维度
growth_milestones: list[Milestone]  # 成长轨迹

    Dimension
    ─────────
    index: int (1-7)
    name: string                # 决策逻辑 / 人际交往 / ...
    pattern: string             # 核心模式描述
    signals: list[string]       # 关键信号
    severity: int (1-10)       # 问题严重度
    confidence: float (0-1)    # 确定度（<0.5 → 待确认）
    last_updated: datetime
    findings: list[Finding]     # 按时间排列的发现

        Finding
        ───────
        date: datetime
        session_id: string
        content: string         # 发现了什么
        evidence: string        # 对话中的证据
        status: confirmed | pending | contradicted
```

**存储格式（profile.md）：** 见 PRD §5.3。

### 4.2.2 Timeline（对话时间线）

```
Timeline 1:N Session
───────────────────
entries: list[TimelineEntry]

    TimelineEntry
    ─────────────
    session_id: string
    date: datetime
    session_number: int
    topic: string               # 本次对话主题
    key_findings: list[string]  # 关键发现（最多 3 条）
    dimensions_touched: list[int] # 涉及的维度
    user_self_assessment: string # 用户的自我总结
    new_questions_raised: list[string] # 触发的新问题方向
```

**存储格式（timeline.md）：**
```markdown
## 2026-07-29 第12次对话
- **主题：** 换工作的纠结
- **关键发现：**
  1. 根因不是选A还是B，是怕选完之后后悔
  2. 在重大决定前总是找一个「权威」确认，缺乏自我信任
- **维度：** D1 决策逻辑, D4 价值观动机
- **你的总结：** 「我发现我不是不会做决定，是不敢承担决定的后果」
- **下次可以聊：** 你生命中哪些决定是你完全自己做的？结果如何？
```

### 4.2.3 Patterns（行为模式库）

```
Patterns 1:N Dimension
─────────────────────
patterns: list[Pattern]

    Pattern
    ───────
    id: string                  # D1-001
    dimension: int              # 所属维度
    description: string         # 模式描述
    trigger_conditions: list[string]  # 触发条件
    frequency: int              # 观察次数
    confidence: float           # 确定度
    first_observed: datetime
    last_observed: datetime
    examples: list[string]      # 对话片段（脱敏）
```

**存储格式（patterns.md）：**
```markdown
## D1-001 冲动→复盘→更犹豫 循环
- **描述：** 事前冲动决定 → 事后过度复盘 → 下次更犹豫
- **触发条件：** 时间压力 < 1天 → 直觉主导；> 3天 → 理性分析但拖延
- **观察次数：** 7/12 次对话
- **确定度：** 0.8
- **最近观察：** 2026-07-28 换工作话题
```

### 4.2.4 Evolution Log（演化日志）

```
EvolutionLog 只增不改（append-only audit log）
─────────────────────────────────────────────
entries: list[EvolutionEntry]

    EvolutionEntry
    ──────────────
    timestamp: datetime
    action: created | updated | confirmed | contradicted
    target: string              # 「D1 决策逻辑」/ 「一句话概括」等
    trigger: string             # 触发原因（「第12次对话发现新回避模式」）
    before: string | null       # 变更前
    after: string               # 变更后
    session_id: string          # 哪个会话触发
    validation: pending | confirmed | reverted
```

### 4.2.5 Question Bank（题库）

```
Question
────────
id: string                     # Q001-Q063 为初始题库
dimension: int                 # 1-7
difficulty: int                # 1-3（浅/中/深）
text: string                   # 问题文本
tags: list[string]             # 关键词标签
status: active | deprecated | experimental
    # active: 正式题库
    # deprecated: 低质量，不再使用
    # experimental: 进化候选，20%概率试用
use_count: int                 # 使用次数
avg_response_length: int       # 平均回答长度（质量指标）
avg_response_sentiment: float  # 平均回答情绪（-1到1）
deprecation_reason: string | null
created_by: human | agent      # 人工题 vs Agent 生成
```

**存储格式（questions.md）：**
```markdown
## Q001
- **维度：** D1 决策逻辑
- **难度：** 2
- **问题：** 当你面对一个重大决定时，你的决策过程通常是什么样的？请描述最近一次。
- **标签：** 决策过程, 元认知, 理性vs直觉
- **状态：** active
```

### 4.2.6 Session（会话）

```
Session（SQLite）
────────────────
id: string (uuid)
created_at: datetime
ended_at: datetime | null
mode: interactive | single_query | cron
turn_count: int
state_sequence: json           # 状态转换记录
dimensions_covered: json       # 本次涉及的维度
user_mood_start: string | null # 开场情绪
user_mood_end: string | null   # 收尾情绪
llm_model: string              # 用的哪个模型
llm_tokens_used: int           # token 消耗
summary: string | null         # LLM 生成的摘要
user_self_assessment: string | null  # 用户自评
```

## 4.3 数据流转路径

### 路径 A：一次对话的数据流

```
Session Start
     │
     ├── 读 config.yaml ──────────────────→ LLM 连接配置
     │
     ├── 读 memory/profile.md ────────────→ 热记忆（摘要注入 LLM 上下文）
     ├── 读 memory/timeline.md ───────────→ 热记忆（上次对话要点）
     ├── 读 memory/patterns.md ───────────→ 热记忆（已知行为模式）
     │
     ├── 读 skills/questions.md ──────────→ question_pick 工具使用
     ├── 读 skills/probes.md ─────────────→ probe_decide 工具使用
     │
     ├── 对话循环 ────────────────────────→ LLM API（每次提问/追问/收尾）
     │
     └── Session End
          │
          ├── 写 sessions/*.db ───────────→ 会话记录
          │
          ├── 写 memory/timeline.md ──────→ 追加条目
          ├── 写 memory/profile.md ───────→ 更新维度（如有变化）
          ├── 写 memory/patterns.md ──────→ 更新/新增模式
          └── 写 memory/evolution-log.md ─→ 追加变更记录
```

### 路径 B：画像演化数据流（跨会话）

```
Session 1 → profile.md v1 → evolution-log.md (创建)
    │
Session 3 → 发现矛盾 → profile.md v2 (标记「待确认」) → evolution-log.md
    │
Session 5 → 矛盾确认 → profile.md v3 (提升 confidence) → evolution-log.md
    │
Session 10 → 画像稳定 → profile.md v4 (confidence ≥ 0.8) → evolution-log.md
```

### 路径 C：题库进化数据流

```
初始题库 (63题, status=active)
    │
低质量检测 ← use_count + avg_response_length + sentiment
    │
标记 deprecated (不删除，保留在题库)
    │
对话方向 → Agent 生成新题 → status=experimental
    │
20% 概率试用 → 收集反馈
    │
验证通过 → status=active, created_by=agent
```

## 4.4 存储选型

| 数据 | 格式 | 理由 |
|------|------|------|
| profile.md | Markdown | LLM 原生可读写，用户可以打开看/编辑 |
| timeline.md | Markdown | 追加写入，人类可读的日记格式 |
| patterns.md | Markdown | 结构化但可读，方便人工审查 |
| evolution-log.md | Markdown | audit log，只增不改 |
| questions.md | Markdown | 人工 + Agent 共维护，Markdown 表格 |
| config.yaml | YAML | 配置标准格式 |
| sessions/*.db | SQLite | 结构化查询（按日期/模式/维度统计） |

**为什么不用 PostgreSQL / MongoDB？**
- 单用户、单机、CLI 工具
- 零运维负担
- 数据量极小（profile < 50KB，timeline < 500KB after 100 sessions）

**为什么 sesssions 用 SQLite？**
- 需要按维度、日期、情绪等字段查询统计
- timeline.md 是给人看的摘要，SQLite 是给系统查的原始记录

## 4.5 数据安全

| 数据 | 存储位置 | 访问控制 | 备份建议 |
|------|---------|---------|---------|
| LLM API Key | config.yaml | 文件权限 600 | 用户自行管理 |
| profile.md | ~/.deeptalk/memory/ | 文件权限 600 | 建议定期导出 |
| timeline.md | ~/.deeptalk/memory/ | 文件权限 600 | 建议定期导出 |
| sessions.db | ~/.deeptalk/sessions/ | 文件权限 600 | 可选 |
| LLM 对话内容 | 无本地缓存 | — | 对话内容只在 API 调用时传输，不落盘 |

**关键原则：**
- 没有 DeepTalk 服务器——用户数据从不上传
- LLM API 调用走用户自己的 Key，数据在用户和 LLM Provider 之间
- 所有 ~/.deeptalk/ 下的文件权限默认 600（仅所有者可读写）

## 4.6 数据量与性能估算

| 指标 | 1 个活跃用户 | 100 次对话后 |
|------|-------------|-------------|
| profile.md | ~2 KB | ~5 KB |
| timeline.md | — | ~50 KB |
| patterns.md | — | ~10 KB |
| evolution-log.md | — | ~20 KB |
| sessions.db | — | ~200 KB |
| skills/ | ~100 KB | ~120 KB（含进化新题） |
| **总计** | **~120 KB** | **~400 KB** |

**性能：** 所有操作都是本地文件 I/O + LLM API 调用。本地 I/O < 10ms，瓶颈在 LLM API（通常 1-5 秒/次）。

---

## 附录 A：与 Hermes 的技术对比

| 维度 | Hermes | DeepTalk |
|------|--------|----------|
| Agent Loop | Plan→Execute→Observe→Improve | Warm→Open→Ask→Listen→Decide→Close→Reflect |
| 工具调用 | LLM function calling（运行时决定） | Agent Loop 状态机决定（确定性） |
| 工具类型 | 20+ 通用工具（terminal, browser, web...） | 8 个访谈专用工具 |
| 记忆后端 | 可插拔（内置/Honcho/Mem0） | 文件系统 Markdown（唯一后端） |
| Skill | 可执行脚本 + 模板 + 校验器 | 访谈知识库（规则 + 模板，不执行） |
| 配置 | 多层（config.yaml + .env + profiles） | 单层（config.yaml） |
| 多平台 | Gateway（Telegram/Discord/Slack...） | CLI → Phase 4 加 Gateway |
| Plugin | 支持 | 不支持（不需要） |
| MCP | 支持 | 不支持（不需要） |
| 代码量 | ~50K+ lines | 预计 ~5K lines（Phase 1） |

## 附录 B：关键设计决策记录（ADR）

### ADR-001：LLM 不做 function calling

**决策：** Agent Loop 状态机自己决定何时调用工具，不给 LLM 暴露 tool_use。

**理由：**
1. 访谈工具（question_pick、probe_decide）不是「用户问什么就调什么」，是有明确触发时机的
2. 把工具调用交给 LLM 会增加不确定性——LLM 可能在应该追问的时候切话题
3. 访谈的质量取决于稳定节奏，确定性 > 灵活性

### ADR-002：记忆用 Markdown 不用 JSON/SQLite

**决策：** profile.md、timeline.md、patterns.md 用 Markdown 存储。

**理由：**
1. LLM 原生理解 Markdown，注入上下文时不需要格式转换
2. 用户可以打开直接看/编辑——这是产品功能，不是技术妥协
3. 追加写入不需要解析整个文件（timeline.md 直接 append）
4. SQLite 只用于 sessions.db（需要结构化查询统计时）

### ADR-003：不提供 Web UI

**决策：** DeepTalk 只有 CLI。

**理由：**
1. 访谈需要沉浸式体验——浏览器标签页随时会被关掉
2. CLI 是注意力最集中的环境（对标 Claude Code 的成功）
3. 大幅降低开发复杂度（不需要前后端分离、部署、运维）
4. Phase 4 可以加 Feishu/Telegram Gateway，但不做 Web
