---
type: draft
status: sprouting
tags: [AI实操]
---

# OpenClaw配置记录

## 一句话定义
OpenClaw 配置的本质不是"按步骤填表"，而是先对齐套餐能力、模型版本与部署目标，避免静默失败；核心是"理解每个选择背后的原因"。

## 核心要点
- **最大坑点**：默认最新模型不一定被套餐支持。Lite 套餐默认选 GLM-5，实际只支持到 GLM-4.7 → 日志显示 `Message sent` 但无返回（静默失败）
- 日志显示 `Message sent` 不等于模型成功返回——服务商可能返回模糊错误码或静默丢弃
- 本地与云部署取舍取决于是否需要 7x24 在线（云部署约 79 元/年起步）
- Claude Code 最强但需要"魔法"（不推荐新手）；ChatGPT CodeX 同样需要魔法
- Kimi Coding 可作为备选，国产模型中文理解好
- 推荐配置（实战经验）：腾讯云 2核4G + Kimi K2.5 + 飞书，月成本 80-100元，每天省 4小时

## 方法 / 步骤

### 前置准备——先搞清楚三个问题（信息差清单）
1. 你买的套餐具体支持哪些模型版本？（去套餐详情页查，不要相信默认选项）
2. 你需要本地部署还是云部署？（你的电脑能一直开着吗？）
3. 你需要哪些 channel？（你平时用什么软件聊天？）

### 第一步：选择大模型
| 模型 | 推荐人群 | 成本 | 说明 |
|------|---------|------|------|
| 智谱 GLM（Lite） | 新手、预算有限 | 约 ¥15/月 | 支持 GLM-4.6, GLM-4.7，性价比高 |
| Claude Code | 有魔法经验者 | 按量 | 最强但配置门槛高 |
| ChatGPT CodeX | 有魔法经验者 | 按量 | 同样强大，需魔法 |
| Kimi Coding (K2.5) | 国产模型用户 | 约 ¥30-50/月 | 中文理解好，成本可控 |

### 第二步：选择部署方式
| 方式 | 成本 | 优点 | 缺点 |
|------|------|------|------|
| 本地部署 | 0 元（已有电脑） | 简单，只需 API key | 无法 7x24 在线 |
| 云服务器 | ¥50-79/月（腾讯云轻量 2核4G） | 7x24 小时待命 | 需额外费用 |

### 第三步：安装
按官方文档复制粘贴命令，选择对应平台的安装方式即可。

### 第四步：配置——核心战场

#### 启动配置向导
```bash
openclaw onboard
```

#### 配置大模型（注意坑！）
1. 选择供应商（如 Z.AI = 智谱）
2. 选择套餐类型（如 Lite → 对应 Coding-plan-CN）
3. **选择模型版本** — 这是最常见踩坑点
   - 不要选默认的"最新版本"
   - 必须选你套餐明确支持的版本（如 Lite 选 GLM-4.6 或 GLM-4.7）
   - 选错会出现"Message sent 但无返回"的静默失败

大模型配置好后即可使用，channel / web search / skill / hook 可后续补充。

#### 配置 channel（推荐——飞书实战步骤）
飞书通道是生产环境最常用的社交通道。

**1. 创建飞书应用**
- 进入 https://open.feishu.cn/app
- 创建企业自建应用
- 记录 App ID 和 App Secret
- 开启权限（通讯录、消息、群组等 9 项）

**2. 配置 OpenClaw**
```bash
openclaw channels add feishu
# 按提示输入 App ID、App Secret、Encrypt Key、Verification Token
```

**3. 配置事件订阅**
飞书后台 → 事件与回调 → 事件配置，订阅：
- 机器人进群 / 被移出群
- 消息已读 / 接收消息

**4. 启动服务**
```bash
openclaw gateway start
openclaw status
# 应显示：feishu: connected
```

### 第五步：安装 gateway
```bash
openclaw gateway install
```

### 第六步：配置 cron 任务（飞书实战示例）
```bash
# 查看所有任务
openclaw cron list

# 添加新任务
openclaw cron add --name "my_task" \
  --schedule "0 9 * * *" \
  --message "执行xxx任务" \
  --channel feishu \
  --to "your_feishu_user_id"
```

## 实战生产配置（来自 [[raw/2026-02-11--公众号--我的OpenClaw+飞书实战：从]]）

### 推荐配置方案
- **主机**：腾讯云 VM-0-6-ubuntu（2核4G，¥50/月）
- **系统**：Linux 6.8.0
- **模型**：kimi-coding/k2.5（¥30-50/月）
- **通道**：飞书（免费）
- **工作目录**：~/.openclaw/workspace/
- **总成本**：¥80-100/月，每天节省约 4小时（ROI ≈ ¥1.1/小时）

### 投资雷达系统配置（QuantAgent v2.6）
```json
// ~/.openclaw/workspace/quantagent/config/settings.json
{
  "watchlist": {
    "semiconductor": ["688135", "603986", ...],
    "ai_software": ["300229", "300418", ...],
    "new_energy": ["300750", "002594", ...],
    "consumer_electronics": ["002475", ...],
    "gaming_media": ["002517", "300413", ...]
  },
  "portfolio": {
    "holdings": [
      {"code": "300682", "name": "朗新科技", "cost": 17.653}
    ],
    "stop_loss": -5,
    "take_profit": 15
  },
  "ml_config": {
    "enabled": true,
    "weight": 0.20
  }
}
```

### 飞书消息分段处理
```python
# 飞书消息有长度限制（约3000字），需分段发送
if len(content) > 3000:
    chunks = [content[i:i+3000] for i in range(0, len(content), 3000)]
    for chunk in chunks:
        send_to_feishu(chunk)
```

## 故障处理记录

### 故障1：收盘报告未发送
- **现象**：用户反馈报告没收到
- **排查**：检查目录缺对应日期的文件
- **根因**：cron 执行时 API 超时，任务被 kill 后重试未触发
- **解决**：手动补发 + 优化日期逻辑 + 增加任务超时保护

### 故障2：飞书消息长度超限被截断
- **解决**：分段发送，每段 3000 字自动切分

### 故障3：飞书 API 限流
- **解决**：指数退避重试（2s, 4s, 8s）

## 常见误区 / 边界
- **误区**：默认最新版就是最优解 → 不看套餐限制直接选模型导致静默失败
- **误区**：配置就是填表 → 本质是理解每个选择背后的原因
- **误区**：日志不报错就是配置正确 → "Message sent" ≠ 模型成功返回
- **边界**：channel/skill/hook 可先跳过，模型配通就能用
- **边界**：本地部署适合开发测试，生产环境建议云部署

## 关联概念
- [[OpenClaw反思三件事（待补素材）]]
- [[AI脚手架]]
- [[AI从聊天到干活（待补素材）]]
- [[AI应用]]
- [[AI最后一公里]]（新概念——企业级部署需要）

## 来源
- [[raw/20260403--自己-AI应用-openclaw配置.md]]
- [[raw/2026-04-03--公众号--龙虾配置避全坑.md - OpenClaw配置避坑]]
- [[raw/2026-02-11--公众号--我的OpenClaw+飞书实战：从]]

## 内容创作灵感
- "为什么 OpenClaw 配置总失败？其实是信息差。"
- "一次踩坑换来一套 30 分钟配置 SOP。"
- "OpenClaw + 飞书实战：月成本 100 元，每天省 4 小时"
- "投资雷达 + 电网学习 + AI简报：三个 OpenClaw 自动化实战"
- "生产环境的故障处理——自动化系统不是一劳永逸"

## 最近更新
- 2026-04-08：由待 OCR 占位升级为可执行配置条目
- 2026-07-11：补充详细模型选择对比表、避坑清单、飞书配置实战步骤、投资雷达配置示例、故障处理记录
