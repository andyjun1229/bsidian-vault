---
来源：公众号
链接：https://mp.weixin.qq.com/s/rmS1mtEBMdb_png2Nvddvg
时间：2026-08-30
平台：公众号
tags: [AI技术, Agent, Skill设计, 知识库]
---

# Google Research 发布 WikiSkill：三层知识架构让 Agent 技能自我进化（Datawhale 转载）

> 论文：https://arxiv.org/abs/2608.27454

一个 Agent 到底凭什么越来越强？有人靠更大的模型，有人靠更多数据。Google Research 最新发布的 WikiSkill 给出了另一条答案：给 Agent 搭一套三层知识架构，让技能自己进化。

核心是把「经验」和「知识」分开。以前的技能进化方法（EvoSkill、Trace2Skill、SkillOpt）分析完执行轨迹就直接改 Skill，经验用一次就丢。WikiSkill 在中间加了一层持久知识库，让经验先沉淀、再复用。

## 一、三层架构：把经验、知识和技能分开

### 第一层 Raw Layer：保留原始轨迹，给进化留下事实依据

存储每次迭代的执行轨迹：Agent 的完整推理过程、工具调用、输出结果。这一层不可变，保留「到底发生了什么」的原始记录。

为什么单独存一层？后续两层都需要回溯原始轨迹来分析问题：Wiki Maintainer 要从中提取成功/失败模式，Skill Proposer 要按需查阅具体任务的执行方式。原始数据被覆盖或丢失，整个进化过程就失去了事实基础。

### 第二层 Wiki Layer：让一次性经验变成可复用知识（核心层）

把原始轨迹编译成结构化知识，跨迭代持续积累。包含三个部分：
- `patterns/`：每个模式一个 markdown 文件，记录具体的失败原因或成功策略，带可操作的修复方案
- `logs.md`：进化日志，按迭代记录发现了什么、改了什么
- `skill-impact.md`：哪些 Skill 改动被接受、哪些被拒绝，带完整 diff

两个关键设计：
1. **Wiki 永不回滚。** Skill 被拒绝时，Skills Layer 回到上一版本，但 Wiki 保留所有积累的知识。下一轮 Proposer 能看到「上次这个改法为什么被拒」，避免重复踩坑。
2. **Knowledge 和 Skill 分离。** 知识回答「我们知道什么」，技能回答「我们该怎么做」。以前的方法把两者混在一起，改技能时丢失了背后的推理上下文。WikiSkill 让知识持续积累，技能从知识里生长。

### 第三层 Skills Layer：可执行技能，带溯源

当前生效的技能集合。每个技能目录两个文件：
- `SKILL.md`：技能内容，Agent 执行任务时直接读取
- `PURPOSE.md`：记录这个技能是为了解决 Wiki 里的哪个 Pattern 而创建

PURPOSE.md 解决「这个技能为什么存在」。技能需要修改时，Proposer 通过它回溯到对应的知识模式，理解设计意图，而不是盲目打补丁。

## 二、进化循环：从执行轨迹到 Skill 更新

每轮迭代四步：

1. **Inference Agent**：用当前 Skill 在训练集上跑 rollout，产出轨迹到 Raw Layer。训练时不能访问 Wiki（否则 Agent 直接查答案，轨迹失去参考价值）
2. **Wiki Maintainer**：分析采样后的成功/失败轨迹，做根因分析，更新 Wiki 的 Pattern 目录和日志
3. **Skill Proposer**：以 ReAct 方式读 Wiki 索引、查 skill-impact 历史、按需读具体 Pattern 页面和轨迹，提出 Skill 创建或补丁
4. **Gating**：在验证集上评估候选 Skill，分数提升就接受，否则回滚。Wiki 不受影响

关键在第二步和第三步的配合：Wiki Maintainer 把零散轨迹编译成结构化知识，Skill Proposer 从结构化知识生成技能更新。没有 Wiki 层，Proposer 每次都从零开始分析原始轨迹。

## 三、实验结果：9B + Skill 超过 27B 裸模型

五个基准、五个模型：
- **技能进化与模型规模互补**：Qwen 家族，WikiSkill 提升随规模递增——4B +12.3 分、9B +17.5 分、27B +23.9 分。越强的模型获益越多
- **技能弥补规模差距**：Qwen-3.5-9B + WikiSkill 平均 47.4%，超过 Qwen-3.6-27B 无技能的 39.4%
- **技能跨模型家族迁移**：Qwen-3.5-9B 用 27B 进化的技能达 70.2%，用它自己的只有 63.4%——「发现策略」和「执行策略」是两种能力，可以跨模型分工
- **消融实验确认 Wiki 价值**：去掉 Wiki 访问，平均分从 63.7% 降至 48.7%，回落约 15 个百分点

## 写在最后

WikiSkill 的贡献不是新算法，是架构设计：把经验、知识、技能分成三层，让知识在中间持续积累，技能从知识里生长出来。

对做 Agent 的人：别只盯着模型规模和 prompt 调优。搭一套三层知识架构，让经验沉淀为知识，让知识指导进化，才是 Agent 持续变强的底层逻辑。

## 关联

- [[2026-07-13--AI技术--Skill设计法则]]、[[2026-04-24--公众号--如何写好skill的真相]]
- [[2026-07-13--AI技术--Self-Improvement]]、[[2026-07-13--AI技术--Loop Engineering]]
- [[2026-04-14--github--karpathy-llm-wiki]]（raw/ llm-wiki 概念同源）
- [[2026-07-11--方法论--个人知识库演进方案]]
