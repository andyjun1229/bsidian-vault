---
来源: GitHub
链接: https://github.com/jackbauerxu/workbuddy-xhs-skills
时间: 2026-07-20
平台: GitHub
type: note
status: growing
tags: [GitHub, 小红书, AI实操, 方法]
---

# workbuddy-xhs-skills — 小红书冷启动 Agent Skills

## 基本信息
- **仓库**: [jackbauerxu/workbuddy-xhs-skills](https://github.com/jackbauerxu/workbuddy-xhs-skills)
- **星**: 71
- **语言**: Shell / Markdown
- **更新**: 2026-07-16
- **核心来源**: 文子 (@Eejoylove) X Article《别不信！WorkBuddy 就可以把你的小红书从0粉干到1000》

## 项目定位
一套面向 Codex / Claude / WorkBuddy 等 Agent 的小红书冷启动与图文生产 Skills。不是文章摘要，而是一套可以被 Agent 调用的内容运营工作流，覆盖小红书账号从0到稳定迭代的关键环节。

融合了 yanliudreamer 小红书系列、dbskill、xhs-visual-director-skill 等多套方法论。

## 10个 Skill 列表

### 定位与对标
- **wb-xhs-monetization-backsolve** — 从可售卖资产、目标用户和信任路径反推账号方向（先确定 Offer 再倒推定位）
- **wb-xhs-low-follower-pattern** — 拆解低粉高数据内容的标题、封面、停留和互动结构

### WorkBuddy 生产系统
- **wb-xhs-account-profile** — 建立账号档案：定位、口吻、可信主张、内容边界、视觉身份
- **wb-xhs-topic-bank** — 七类标题公式、五类用户需求、封面钩子 → 可持续选题库

### 发布与迭代
- **wb-xhs-humanize-compliance** — 去 AI 味：强化开头、结构、真人感和平台表达检查
- **wb-xhs-schedule-review** — 前10条/30天排期 + 数据复盘闭环

### 视觉生产
- **wb-xhs-visual-router** — 视觉请求分流路由
- **wb-xhs-cover-anchor** — 3:4 完成封面（可诊断旧封面）
- **wb-xhs-xiaohei-illustration** — 16:9 小黑正文配图
- **wb-xhs-material-illustration** — 材质解释图、图表美化

## 核心工作流
```
变现倒推定位 → 建立账号档案 → 规划前10条 → 生成选题库和标题 
→ 校准初稿与图文结构 → 视觉交付 → 学习低粉高数据样本 
→ 10-20条数据复盘 → 写回账号档案
```

## 关键理念
- 先确定变现方式，否则定位和选题会失焦（变现倒推）
- 新手更适合拆**低粉爆款**（反映内容结构本身的力量，不是大号案例）
- Agent 的价值不只是生成文案，而是**保留账号上下文**
- AI 初稿必须经过**真人口吻 + 平台规则**双重检查
- 周期性复盘把个别爆款经验变成**账号资产**

## 来源文档
| 文件 | 说明 |
|------|------|
| README.md | 项目整体说明 |
| INDEX.md | 技能索引 + 引用图 + 推荐使用顺序 |
| BOOK_OVERVIEW.md | 对原文方法论的深度理解和批判 |
| DIGEST.md | 面向读者的精华说明 |
| FUSION_NOTES.md | 融合多套方法的补丁说明 |
| GLOSSARY.md | 术语表 |
| verified.md | 通过三验证的方法论单元 |
| candidates/ | 候选方法论单元 |
| rejected/ | 未独立成 skill 的候选及原因 |

## 对我自己的参考价值
- 我的公众号「飞叔AI沉思录」也面临冷启动问题，这套工作流逻辑可迁移到公众号
- **变现倒推定位**的思路可以用于规划公众号的变现路径
- **humanize-compliance**（去AI味）与我已有的 writing-anchor skill 思路互补
- 视觉生产流程（封面/插图/材质图）对公众号配图也有参考价值
- 融合多套方法论的方式（BOOK_OVERVIEW + FUSION_NOTES）值得借鉴
