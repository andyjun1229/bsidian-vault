---
type: experience
status: growing
tags: [操作经验]
---

# 逆向分析 gzh-design 并重构 self-interview

听了 [甲木的 gzh-design 排版 skill]，用在 [逆向分析 skill 设计哲学 → 重构自己的 self-interview 自我访谈框架]，产出 [self-interview skill 从单文件提示词改为三段分离系统：SKILL.md (344行) + references/ (169行问题库 + 28行防御模式) + scripts/validate_progress.py (77行校验器) + data/ (60行进度状态)]。

理论来源：甲木、摸鱼小李、藏师傅（Skill 即系统的设计哲学）。

**关键收获：**
1. 把 LLM 当复读机用，不当设计师——给精确模板让 AI 填空，不是让 AI 自己设计
2. 三段分离——决策流 / 资产库 / 校验脚本，各管各的
3. 单一权威来源——颜色/字号/间距只在一个文件定义
4. Gotchas 清单——踩过的坑写成显式规则
5. 校验脚本做确定性兜底——能确定的事不要交给模型猜

**后续动作：**
- 把这个设计哲学提炼成了独立的 skill-design-philosophy skill（已存在 Hermes 系统中）
- 这个三步法可以复用到其他项目：找 reference → 量化参数 → 校验脚本兜底
