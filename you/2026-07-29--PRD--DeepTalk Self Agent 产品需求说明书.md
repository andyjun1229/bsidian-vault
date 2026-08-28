---
type: prd
status: sprouting
tags: [自我访谈, AI智能体, 产品设计]
---

# DeepTalk — 独立自我访谈智能体 PRD v2

> **版本：** v2.0（重写：独立 Agent 架构）  
> **日期：** 2026-07-29  
> **作者：** 飞叔  
> **产品形态：** 独立 CLI Agent（`deeptalk` 命令）  
> **对标产品：** Claude Code / Codex / Hermes / OpenClaw  
> **一句话：** 一个只做自我访谈的独立智能体——有自己的记忆、技能系统、工具调用循环，不寄生在任何框架上。

---

## 〇、先回答一个问题：为什么不做 Hermes Profile？

Hermes Profile 是正确的「分销方案」，但不是正确的「产品本质」。

- **Profile 受限于 Hermes 的 Agent Loop。** Hermes 的循环是为通用任务设计的（Plan→Execute→Observe→Improve），自我访谈需要的是一个对话循环（暖场→提问→倾听→追问→记录→收尾），两者节奏完全不同。
- **Profile 的工具集是通用的。** 自我访谈不需要 terminal、browser、web search、code execution。它只需要一套专用的访谈工具：读记忆、写记忆、选问题、生成追问、合成画像。
- **Profile 的 Skill 机制是附加的。** DeepTalk 的访谈能力应该是 Agent 的原生能力，不是一个「加载进来的技能」。
- **Profile 的身份感不够。** 用户打开 Hermes 然后加载一个 profile，感觉是「用 Hermes 做了一个访谈插件」。独立 CLI `deeptalk` 本身就是这个产品——打开就是访谈，没有别的功能。

**结论：借鉴 Hermes 的架构模式（Harness / Skill / Memory / Loop），但自成一体。**

---

## 一、产品定义

### 你的私人自我访谈 Agent

```
$ deeptalk

  🪞 DeepTalk — 你的私人自我访谈伙伴

  距上次对话已过 7 天。最近有什么事在你脑子里转？

  > 最近在考虑要不要换工作...
```

没有菜单、没有设置页、没有题库列表。打开就是对话，关上就停了。下次打开，它记得上次聊到哪。

### 它不是什么

- 不是心理咨询师（不说「我理解你的感受」）
- 不是人生导师（不给你建议）
- 不是心理测试（不给你打分贴标签）
- 不是一次性工具（不是做完 63 题就完了）

### 它是什么

- 一个持续的对话伙伴——每次都从上次结束的地方继续
- 一面镜子——帮你看清自己的思考模式
- 一个记录者——你的每一次自我发现都被记住，不会丢
- 一个追问者——不问到你真正想说的不罢休

---

## 二、架构总览

```
┌──────────────────────────────────────────────────┐
│  CLI 入口（deeptalk）                              │
│  - 交互式对话模式                                   │
│  - 单次查询模式（deeptalk -q "聊聊最近的压力"）        │
│  - 定时模式（deeptalk --cron → 被 cron 调用）        │
├──────────────────────────────────────────────────┤
│  Agent Loop（核心循环）                             │
│  Warm → Ask → Listen → Probe → Reflect → Record    │
│  状态机：闲聊 / 访谈 / 深挖 / 收尾 / 后台更新         │
├──────────────────────────────────────────────────┤
│  工具层（专用工具，非通用）                          │
│  memory_read / memory_write / question_pick        │
│  probe_generate / portrait_synthesize              │
│  pattern_detect / evolution_log                    │
├──────────────────────────────────────────────────┤
│  记忆层                                            │
│  热记忆：当前对话上下文（LLM context window）         │
│  温记忆：Skill 知识库（维度定义、追问模板、题库）      │
│  冷记忆：文件持久化画像（profile.md + timeline.md）   │
├──────────────────────────────────────────────────┤
│  模型层                                            │
│  LLM API（DeepSeek / Claude / 任意 OpenAI 兼容）    │
└──────────────────────────────────────────────────┘
```

---

## 三、Agent Loop（核心循环）

这是 DeepTalk 的灵魂。不同于 Hermes 的 Plan→Execute→Observe→Improve 通用循环，DeepTalk 的循环是对话驱动的：

```
┌─────────────────────────────────────────┐
│  1. Warm（预热）                         │
│  - 加载冷记忆（profile.md, timeline.md）  │
│  - 注入系统提示词                         │
│  - 检查距上次对话时间                     │
├─────────────────────────────────────────┤
│  2. Open（开场）                         │
│  - < 3天：「上次聊到XX，有变化吗？」       │
│  - > 7天：「一周没聊了，最近脑子里在想啥？」 │
│  - 新用户：从 D4 价值观切入               │
├─────────────────────────────────────────┤
│  3. Loop（访谈循环）                      │
│  ┌─→ Ask：从题库选下一个问题              │
│  │   Listen：用户回答                     │
│  │   Decide：                             │
│  │   ├─ 需要追问 → Probe（最多2层）        │
│  │   ├─ 自然转折 → 换维度                  │
│  │   ├─ 15分钟/用户累了 → 收尾             │
│  │   └─ 继续 → Ask 下一个问题              │
│  └─── 循环 ←────────────────┘             │
├─────────────────────────────────────────┤
│  4. Close（收尾）                         │
│  - 总结本次核心发现（2-3句）               │
│  - 问：「你觉得今天最重要的发现是什么？」    │
│  - 记录用户自己的总结                     │
├─────────────────────────────────────────┤
│  5. Reflect（后台更新，不影响用户）         │
│  - 更新 profile.md                       │
│  - 追加 timeline.md                      │
│  - 更新 patterns.md                      │
│  - 更新 evolution-log.md                 │
└─────────────────────────────────────────┘
```

### 状态机

```
             ┌──────────┐
   新用户 → │  暖场     │
             └────┬─────┘
                  ↓
             ┌──────────┐
    老用户 → │  开场     │ ← 加载上次画像 + 时间线
             └────┬─────┘
                  ↓
             ┌──────────┐
        ┌─── │  访谈     │ ← 核心循环
        │    │ 问→听→判  │
        │    └────┬─────┘
        │         ↓
        │  ┌──────┴──────┐
        │  ↓              ↓
        │ ┌─────────┐  ┌─────────┐
        │ │ 追问    │  │ 转向    │
        │ │ (≤2层)  │  │ 换维度   │
        │ └────┬────┘  └────┬────┘
        │      └──────┬─────┘
        │             ↓
        │      ┌──────────┐
        │      │ 继续？    │
        │      └────┬─────┘
        │      是   │   否（15min / 用户说累了）
        └──────────┘        ↓
                      ┌──────────┐
                      │  收尾    │
                      └────┬─────┘
                           ↓
                      ┌──────────┐
                      │ 后台更新  │ → 异步执行
                      └──────────┘
```

---

## 四、工具系统（专用，非通用）

DeepTalk 不需要 terminal、browser、web search、code execution。它的工具只做一件事：支持深度对话。

### 工具清单

| 工具 | 触发时机 | 做什么 |
|------|---------|--------|
| `memory_load` | 会话开始时 | 加载 profile.md + timeline.md + patterns.md |
| `memory_save` | 会话结束后 | 更新 profile.md + 追加 timeline.md |
| `question_pick` | 每次提问前 | 从题库中选下一个问题（基于当前话题 + 画像盲区） |
| `probe_decide` | 用户回答后 | 判断是否需要追问、追问什么方向 |
| `pattern_detect` | 后台更新时 | 从对话中提取重复模式，写入 patterns.md |
| `portrait_update` | 后台更新时 | 对比新旧信号，更新 profile.md 对应维度 |
| `session_summarize` | 收尾阶段 | 生成本次对话摘要 |
| `evolution_track` | 后台更新时 | 记录画像变更到 evolution-log.md |

### 工具与 Agent Loop 的对应

```
Loop 阶段          使用的工具
─────────────────────────────────
Warm               memory_load
Open               (内建于 prompt，无需工具)
Ask                question_pick
Listen             (用户输入，无需工具)
Decide             probe_decide
Probe              (内建于 prompt)
Close              session_summarize
Reflect            memory_save + pattern_detect + portrait_update + evolution_track
```

---

## 五、记忆系统

### 5.1 三层记忆

```
热记忆（会话上下文）
  ├─ 当前对话历史
  ├─ 本次加载的 profile 摘要
  └─ 生命周期：一次会话

温记忆（Skill 知识库）
  ├─ 7 维度定义 + 关键词
  ├─ 63 题题库（含维度映射）
  ├─ 追问策略模板
  ├─ 画像融合模板
  └─ 生命周期：系统更新时刷新

冷记忆（文件持久化）
  ├─ profile.md      当前画像
  ├─ timeline.md     对话时间线
  ├─ patterns.md     行为模式库
  └─ evolution-log.md 画像演化日志
  生命周期：永久
```

### 5.2 冷记忆文件结构

```
~/.deeptalk/
├── config.yaml          # 配置（模型、API key、偏好）
├── memory/
│   ├── profile.md       # 当前个人画像
│   ├── timeline.md      # 对话时间线
│   ├── patterns.md      # 行为模式库（ACE 风格）
│   └── evolution-log.md # 画像演化日志
├── skills/
│   ├── dimensions.md    # 7 维度定义 + 关键词体系
│   ├── questions.md     # 题库（63 题 + 自进化新题）
│   ├── probes.md        # 追问策略库
│   └── synthesis.md     # 画像融合模板
├── sessions/            # 会话记录（可选保留）
└── logs/                # 运行日志
```

### 5.3 profile.md 格式

```markdown
# 飞叔的个人画像
最后更新：2026-07-29 22:15
对话次数：12

## 一句话概括
一个在理性与直觉之间反复拉扯的架构师，知道该分析但总是先拍脑袋，事后又用过度复盘来惩罚自己。

## 7 维度画像

### 01 决策逻辑
**模式：** 冲动直觉 → 事后过度复盘 → 下次更犹豫
**关键信号：** 时间压力 < 1天时倾向于直觉；> 3天时会理性分析
**严重度：** 7/10
**最新发现（2026-07-28）：** 在面对A和B选择时，纠结的根因不是选哪个，而是怕选完之后后悔

### 02 人际交往
...
```

---

## 六、Skill 系统

借鉴 Hermes 的 Skill 设计哲学（三层分离：工作流 + 资产库 + 校验器），但更轻量——DeepTalk 的 Skill 就是访谈知识，不需要执行脚本。

```
skills/
├── dimensions.md     ← 资产库：7 维度定义 + 每个维度的关键词映射
├── questions.md      ← 资产库：题库（63 题，含维度/难度/适用场景）
├── probes.md         ← 工作流：追问决策树 + 追问模板
├── synthesis.md      ← 工作流：画像融合的四家哲学对照表
└── quality.md        ← 校验器：访谈质量检查清单 + 画像质量检查清单
```

**与 Hermes Skill 的区别：**
- Hermes Skill = 可执行的工作流 + 模板 + 脚本
- DeepTalk Skill = 访谈知识库，被 Agent Loop 内的工具（question_pick / probe_decide）读取和使用
- 不进 LLM 上下文——工具按需读取后注入

---

## 七、自改进机制（Harness Engineering 应用）

借鉴 Harness Engineering 的 Self-Harness 三阶段循环，但应用于访谈场景：

### 7.1 题库进化

```
阶段1：弱点挖掘（Weakness Mining）
  收集信号：用户敷衍回答的题目、用户跳过的话题、用户说「这个问题没意思」
  → 标记低质量题目

阶段2：补丁提案（Harness Proposal）
  从对话中自然涌现的方向 → LLM 生成新题目候选
  → 标注维度、难度、触发条件

阶段3：验证合并（Proposal Validation）
  候选新题在冷存储中标记为 experimental
  → 在后续对话中以 20% 概率试用
  → 收集用户反馈（回答质量 + 用户情绪）
  → 验证通过 → 正式入库 questions.md
```

### 7.2 追问策略进化

```
阶段1：失败聚类
  收集追问失败：用户回避 / 敷衍 / 切换话题 / 情绪变差
  → 聚类失败模式：
    - 追太急（用户还没说完就追问）
    - 方向错（追问跟用户想说的无关）
    - 时机差（该收尾时还在追问）
    - 情绪冒犯（追问触及了不想谈的领域）

阶段2：策略调整
  基于失败模式 → 修改 probes.md 的追问决策树
  → 新增退让条件：「如果用户连续两次回答 < 10字 → 切换话题」

阶段3：验证
  修改后的策略在后续对话中验证
  → 失败率下降 → 合并
```

### 7.3 画像进化

```
对话次数    画像状态
─────────────────────
第 1 次     粗糙画像（关键词匹配 + LLM 首次生成）
第 3 次     发现矛盾点，标记「待确认」
第 5 次     确认/修正矛盾点，画像趋于稳定
第 10 次    稳定画像 + 可追溯的演化轨迹
第 20 次    画像预测能力（Agent 能预判你在某些场景下的反应）
```

---

## 八、技术方案

### 8.1 技术栈

| 层 | 选型 | 理由 |
|----|------|------|
| 语言 | Python 3.11+ | 生态丰富，LLM SDK 完善 |
| CLI 框架 | prompt_toolkit + rich | 终端交互体验对标 Claude Code |
| LLM SDK | openai（兼容 DeepSeek） | 标准 API，Provider 无关 |
| 记忆存储 | 文件系统（markdown） | Harness 模式 2，LLM 原生可读写 |
| 会话管理 | SQLite | 轻量，无需外部依赖 |
| 配置 | YAML | 人类可读 |
| 打包 | pip / homebrew / 单二进制 | 多分发渠道 |

### 8.2 核心依赖

```toml
[project]
name = "deeptalk"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "openai>=1.0",        # LLM API
    "prompt-toolkit>=3.0", # CLI 交互
    "rich>=13.0",          # 终端美化
    "pyyaml>=6.0",         # 配置
    "pydantic>=2.0",       # 数据模型
]
```

### 8.3 Agent Loop 伪代码

```python
class DeepTalkAgent:
    def __init__(self, config_path: str):
        self.config = load_config(config_path)
        self.llm = LLMClient(self.config.model)
        self.memory = MemorySystem(self.config.memory_dir)
        self.skills = SkillLibrary(self.config.skills_dir)
        self.state = AgentState.WARM

    def run(self):
        """主循环"""
        self._warm()           # 加载记忆
        self._open()           # 开场

        while self.state != AgentState.CLOSE:
            if self.state == AgentState.ASK:
                question = self._pick_question()
                self._ask(question)
                self.state = AgentState.LISTEN

            elif self.state == AgentState.LISTEN:
                answer = self._get_user_input()
                self.context.add(answer)
                decision = self._decide(answer)
                self.state = decision

            elif self.state == AgentState.PROBE:
                probe = self._generate_probe()
                self._ask(probe)
                self.probe_depth += 1
                self.state = AgentState.LISTEN

            elif self.state == AgentState.SWITCH:
                self._switch_dimension()
                self.state = AgentState.ASK

        self._close()
        self._reflect()       # 后台更新记忆

    def _decide(self, answer: str) -> AgentState:
        """决定下一步：追问 / 转向 / 继续 / 收尾"""
        # 检查收尾条件
        if self._should_close():
            return AgentState.CLOSE

        # 检查追问条件
        if self.probe_depth < 2 and self._should_probe(answer):
            return AgentState.PROBE

        # 检查转向条件
        if self._should_switch():
            return AgentState.SWITCH

        # 默认继续
        return AgentState.ASK

    def _should_probe(self, answer: str) -> bool:
        """判断是否需要追问"""
        signals = [
            len(answer) < 10,                    # 敷衍
            any(w in answer for w in ["还好", "还行", "差不多", "不知道"]),
            self._detect_contradiction(answer),   # 跟之前说的矛盾
            self._detect_emotion(answer),         # 情绪信号
        ]
        return any(signals)

    def _should_close(self) -> bool:
        """判断是否该收尾"""
        return (
            self.elapsed > 15 * 60 or            # 超过 15 分钟
            self.turn_count > 15 or              # 超过 15 轮
            self._user_shows_fatigue()           # 用户表现出疲劳
        )
```

### 8.4 项目结构

```
deeptalk/
├── pyproject.toml
├── README.md
├── src/
│   └── deeptalk/
│       ├── __init__.py
│       ├── cli.py              # CLI 入口（prompt_toolkit）
│       ├── agent.py            # Agent Loop 核心
│       ├── loop.py             # 状态机
│       ├── memory/
│       │   ├── __init__.py
│       │   ├── loader.py       # memory_load 工具
│       │   ├── saver.py        # memory_save 工具
│       │   └── models.py       # Profile, Timeline, Pattern 数据模型
│       ├── skills/
│       │   ├── __init__.py
│       │   ├── questions.py    # question_pick 工具
│       │   ├── probes.py       # probe_decide / probe_generate 工具
│       │   └── synthesis.py    # portrait_update 工具
│       ├── llm/
│       │   ├── __init__.py
│       │   └── client.py       # LLM API 封装
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── registry.py     # 工具注册
│       │   ├── memory_tools.py
│       │   ├── interview_tools.py
│       │   └── analysis_tools.py
│       └── config.py           # 配置加载
├── skills/                     # 默认 Skill 知识库
│   ├── dimensions.md
│   ├── questions.md
│   ├── probes.md
│   └── synthesis.md
└── tests/
    ├── test_agent.py
    ├── test_memory.py
    └── test_tools.py
```

---

## 九、CLI 设计

### 命令

```bash
# 交互式对话（默认）
deeptalk

# 单次对话
deeptalk -q "最近压力很大，帮我理一理"

# 查看画像
deeptalk portrait

# 查看对话历史
deeptalk timeline

# 导出画像
deeptalk export --format pdf

# 定时模式（被 cron 调用）
deeptalk --cron

# 配置
deeptalk config set model deepseek-chat
deeptalk config set api_key sk-xxx
```

### 交互界面

```
╔══════════════════════════════════════════════╗
║  🪞 DeepTalk                                 ║
║  你的私人自我访谈伙伴                           ║
║                                              ║
║  第 12 次对话 | 上次：2026-07-28               ║
╚══════════════════════════════════════════════╝

距上次对话已过 7 天。

最近有什么事在你脑子里转？

> 我在想要不要换工作...

  你提到了「要不要」——这种二选一的状态持续多久了？

> 大概两个月了吧，一直下不了决心。

  两个月里，你做了哪些尝试来做这个决定？

> 我列过 pros and cons，也问过几个朋友...

  你列 pros and cons 的时候，哪一边更长？

> ...

─────────────────────────────────────────────
💡 提示：随时可以说「我想换个话题」「今天就到这」
   对话记录仅供你个人使用，不上传云端
```

---

## 十、分发方案

### 10.1 安装

```bash
# pip 安装
pip install deeptalk

# 或 homebrew
brew install deeptalk

# 或一行脚本
curl -fsSL https://deeptalk.sh/install | bash
```

### 10.2 配置

```bash
# 首次运行自动引导配置
deeptalk
# → 检测到未配置，进入首次设置向导
# → 1. 选择 LLM Provider（DeepSeek / Claude / OpenAI）
# → 2. 输入 API Key
# → 3. 创建你的名字（用于画像，不联网）
# → 4. 开始第一次对话
```

### 10.3 变现

```
免费层：每月 10 次对话 + 基础画像 + 对话历史 30 天
Pro 层（$9.9/月）：无限对话 + 完整画像 + 演化轨迹 + 数据导出
团队层（$49/月）：团队画像 + 组织文化诊断 + 管理者看板
```

---

## 十一、与 Hermes / Claude Code 的本质区别

| | Hermes / Claude Code | DeepTalk |
|---|---|---|
| **定位** | 通用 Agent 框架 | 垂直 Agent 产品 |
| **用户** | 开发者 | 任何想做自我探索的人 |
| **工具** | terminal, browser, file, web, code... | 访谈专用工具（读记忆、选问题、生成追问） |
| **循环** | Plan→Execute→Observe→Improve | Warm→Open→Ask→Listen→Decide→Close→Reflect |
| **记忆** | 通用上下文 + 可选 memory | 三层访谈记忆（热/温/冷），核心功能 |
| **技能** | 可插拔的通用工作流 | 访谈知识库（维度/题库/追问模板），固化在系统里 |
| **交互** | 命令行 + 多平台 gateway | CLI 对话，未来可扩展 gateway |
| **扩展** | plugin + MCP + custom tools | 不需要扩展——做好一件事 |

---

## 十二、MVP 范围

### Phase 1：能对话（2 周）

- [ ] CLI 入口 `deeptalk`
- [ ] Agent Loop（Warm→Open→Ask→Listen→Decide→Close）
- [ ] LLM 对接（DeepSeek API）
- [ ] 基础追问（基于信号检测）
- [ ] 冷记忆：profile.md + timeline.md
- [ ] 63 题题库（从现有 App 迁移）

### Phase 2：有记忆（2 周）

- [ ] 追问优化（2 层深挖 + 退让机制）
- [ ] patterns.md（行为模式库）
- [ ] evolution-log.md（画像演化日志）
- [ ] portrait_update 工具（会话后自动更新画像）
- [ ] session_summarize 工具

### Phase 3：能进化（2 周）

- [ ] 题库自进化（低质量标记 + 新题生成）
- [ ] 追问策略自进化（失败聚类 + 策略迭代）
- [ ] 画像预测能力（预判用户反应模式）
- [ ] 配置系统（config.yaml）

### Phase 4：能分发（2 周）

- [ ] pip 安装包
- [ ] 首次设置向导
- [ ] 画像导出（Markdown / PDF）
- [ ] Feishu/Telegram gateway（可选）

---

## 十三、关键设计决策

1. **不做通用 Agent 框架。** 代码里没有 plugin 系统，没有 MCP，没有可扩展工具集。所有工具都是访谈专用的。
2. **文件系统 = 唯一的记忆后端。** 不用 PostgreSQL、不用 Redis、不用向量数据库——就是 `~/.deeptalk/memory/` 下的几个 .md 文件。LLM 原生可读，用户也能直接打开看。
3. **Agent Loop 是对话驱动的，不是任务驱动的。** Hermes 的循环是「完成任务」，DeepTalk 的循环是「持续对话」。没有成功/失败状态，只有继续聊还是收尾。
4. **追问有上限，有退让。** 最多 2 层深挖。用户说「算了」立刻停。这是产品设计，不是技术限制。
5. **不做诊断，不贴标签。** Agent 说「我注意到一个模式」而不是「你有 XX 问题」。
6. **用户数据完全本地。** 画像、对话记录全在用户机器上。API Key 是用户自己的，LLM 调用走用户自己的账号。没有任何数据上传到 DeepTalk 服务器。

---

## 十四、风险

| 风险 | 缓解 |
|------|------|
| 追问像审讯 | 2 层上限 + 退让话术 + 「不想聊可以跳过」 |
| 画像过度确定 | 「待确认」标记 + 矛盾保留 + 用户可以编辑 profile.md |
| 情感依赖 | 定期提醒「我是一个 AI，不是心理咨询师」 |
| 记忆泄露（不同用户共用机器） | `~/.deeptalk/` 是 per-user 的，操作系统权限隔离 |
| 用户不想装 Python | 未来提供单二进制打包（PyInstaller / Nuitka） |
| 题库质量退化 | 自进化机制有「实验候选 → 验证 → 入库」三道门 |

---

## 十五、接下来的动作

1. **今天确定：** 这个方向 OK？有没有要调整的？
2. **本周：** 我搭建项目骨架 + Agent Loop + 对接 DeepSeek
3. **下周：** 导入现有 63 题 + 追问引擎 + 冷记忆
4. **两周后：** 你跑第一轮完整对话 → 反馈 → 迭代
