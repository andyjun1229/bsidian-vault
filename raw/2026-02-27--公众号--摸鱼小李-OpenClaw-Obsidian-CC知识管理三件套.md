---
来源：公众号
链接：https://mp.weixin.qq.com/s/EMahAzgfAbRQrYukWE7_IQ
时间：2026-02-27
平台：公众号
作者：摸鱼小李
---

# OpenClaw+Obsidian+CC｜才是AI时代知识管理的神（20 分钟装好全套）

2026 年最顺手的知识管理三件套，OPC必备。

前段时间写了一篇 Obsidian + Claudian 的教程，好多朋友看完直接重新下回了 OB 用起来。今天这篇是续集——加上 OpenClaw 这个关键拼图，帮你真正跑通从「收集」到「分享」的完整闭环，把原始信息转化为个人智慧。

## 01 先看效果 / 三个真实场景

### Case 1：爆款笔记拆解：刷到即学习
刷小红书看到好帖子，直接飞书转发给 OpenClaw，它会拆解底层逻辑，你还能顺着聊选题、聊原理——不打断心流，聊完就懂了，经验自动沉淀到 OB 知识库，下次 AI 直接调用。

### Case 2：创意前的功课
要去一家生鲜电商公司交流 AI 制作 TVC，在外面吃饭等桌时突然有些想法，直接用龙虾调研行业和品牌资料，沉淀到 OB 中，晚上回家速读一遍，再和 Claudian 深聊，完善调研、探索创意方向，跑出来个 TVC。

除了这些，还有对热点的抓取等等，OpenClaw 的玩法很多，下期单独讲。本期聚焦一件事：OpenClaw 怎么融入你的知识管理闭环，解决信息处理环节低效（如阅读耗时、知识难以调用）。

## 02 安装基建 / 安装篇

首先是 OpenClaw 的安装，使用 Mac。推荐使用 Cherry Studio 免命令安装。

### Step 1：下载 Cherry Studio
下载对应系统的安装包（Mac / Windows / Linux 都有），安装后打开。

### Step 2：一键安装龙虾
在 Cherry Studio 首页找到 OpenClaw 图标（红色小龙虾），点进去 → 点「安装 OpenClaw」按钮。Cherry Studio 会自动在后台装好龙虾（不需要碰终端）。安装完成后，页面会变成启动界面——但先别急着启动，因为龙虾需要一个 AI 模型才能工作。

### Step 3：购买阿里云百炼
推荐用阿里云百炼 Coding Plan，性价比最高。选 Lite 版本，点「立即购买」。购买完成后在百炼控制台找到你的 API Key。

### Step 4：在 Cherry Studio 里添加模型
Cherry Studio 右上角 ⚙️ 设置 → 「模型服务」→「+ 添加」

- 提供商名称：填「阿里」
- 提供商类型：选 OpenAI
- API 密钥：粘贴百炼 Key
- 地址：https://coding.dashscope.aliyuncs.com/v1

添加以下 4 个模型：
1. kimi-k2.5
2. glm-5（稳定可靠）
3. MiniMax-M2.5（响应速度快）
4. qwen3.5-plus（百万上下文）

### Step 5：启动龙虾
回到 Cherry Studio 左侧，点 OpenClaw 图标 → 模型选 kimi-k2.5 | 阿里云百炼 → 点「▶ 启动」。

### Step 6：对接飞书（让龙虾上手机）
在 Dashboard 对话框里发：帮我配置飞书，让我能通过飞书手机端跟你对话。一步步引导我，每步做完等我确认再继续。

### Step 7：安装 OB + CC
同样在 Dashboard（或飞书）里发给龙虾，让它一步步引导安装 Obsidian、Claudian 插件、cc-switch。

## 03 装备技能 / 给龙虾装必备 Skill

### 4 个必备 Skill（地基）
在 Dashboard 或飞书里发给龙虾依次安装：

1. **Multi Search Engine**（免费搜索引擎，17 个搜索引擎覆盖国内外）
   `npx clawhub@latest install multi-search-engine`

2. **x-reader**（国内链接解析：微信公众号、小红书、B站、X 等）
   `pip install git+https://github.com/runesleo/x-reader.git`

3. **Obsidian**（存知识库）
   `npx clawhub@latest install obsidian`

4. **find-skills**（发现更多 Skill）
   `npx clawhub@latest install find-skills`

装完这 4 个，龙虾具备了：搜索 → 解析链接 → 存进 OB → 发现新能力的完整链路。

### 进阶：开源 Skill 库
推荐：https://github.com/cafe3310/public-agent-skills
覆盖四大场景：创作与知识管理、在线平台、项目管理、辅助工具。

💡 Agent Skill 本质是提示词和代码的集合。装之前建议让龙虾帮你审核一下内容。

### 实用玩法
- **随手记**：在飞书里把碎碎念、文章链接、截图发给龙虾，它帮你整理存进 OB
- **定时简报**：设定每天早上推送天气 + 日程 + 行业新闻
- **知识库管理**：定时让龙虾整理本周笔记，生成周报
- **文件整理**："帮我把桌面上的文件按类型分到不同文件夹里"

### 训练你的龙虾
龙虾的 workspace 里有 4 个核心文件，每次对话都会读取：
- **USER.md**：你是谁：名字、职业、工作时间、沟通偏好
- **SOUL.md**：龙虾的性格和行事准则
- **IDENTITY.md**：龙虾的名字和形象
- **AGENTS.md**：工作手册：记忆规则、文件结构、工作流程

大多数人装好后这些文件只有默认模板，所以龙虾只能用最通用的方式回复你。第一天就把 USER.md 填好。

### 建立软链接：打通 OB 和龙虾
让龙虾的核心配置文件出现在 OB 里，以后直接在 OB 里调教龙虾的「性格」。给龙虾发：帮我建一个软链接，把你的工作区链接到我的 OB 仓库里，建一个叫「龙虾工作区」的文件夹。

建好后：OB 里出现「龙虾工作区」文件夹。你在 OB 编辑 SOUL.md → 龙虾立即生效；龙虾更新配置 → OB 里立即看到。双向实时同步。

---

以上就完成了：Obsidian + Claude Code + OpenClaw 三者基建的安装。
