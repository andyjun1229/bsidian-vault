---
来源: 公众号
链接: https://mp.weixin.qq.com/s/EMahAzgfAbRQrYukWE7_IQ
时间: 2026-02-27
平台: 公众号
---

# OpenClaw+Obsidian+CC｜才是AI时代知识管理的神（20 分钟装好全套）

前段时间写了一篇**Obsidian**+**Claudian**的教程，好多朋友看完直接重新下回了 OB 用起来（开心，在此感谢苍何佬，OB 吹哨人）。今天这篇是续集——加上**OpenClaw**这个关键拼图，帮你真正跑通从「收集」到「分享」的完整闭环，把原始信息转化为个人智慧。

## 01 先看效果/三个真实场景

**Case 1 - 爆款笔记拆解：刷到即学习**
刷小红书看到好帖子，直接飞书转发给OpenClaw，它会拆解底层逻辑，你还能顺着聊选题、聊原理——不打断心流，聊完就懂了，经验自动沉淀到OB知识库，下次 AI 直接调用

**Case 2 - 创意前的功课**
去生鲜电商公司交流 AI 制作 TVC，在外面吃饭等桌时突然有些想法，直接用龙虾调研行业和品牌资料，沉淀到OB中，晚上回家速读一遍，再和Claudian深聊，完善调研、探索创意方向，跑出来个 TVC

## 02 安装基建/安装篇

### Step 1 - 下载 Cherry Studio
下载对应系统的安装包（Mac/Windows/Linux 都有），安装后打开。

### Step 2 - 一键安装龙虾（OpenClaw）
在 Cherry Studio 首页找到OpenClaw图标（红色小龙虾），点进去。点「安装 OpenClaw」按钮，自动后台安装。

### Step 3 - 购买阿里云百炼
推荐**阿里云百炼 Coding Plan**，选Lite版本。购买后在百炼控制台找到API Key。

### Step 4 - 在 Cherry Studio 里添加模型
设置 → 模型服务 → 添加提供商：
- 提供商名称：阿里
- 提供商类型：OpenAI
- API 密钥：粘贴百炼 Key
- API 地址：`https://coding.dashscope.aliyuncs.com/v1`

添加4个模型：
1. kimi-k2.5
2. glm-5（稳定可靠）
3. MiniMax-M2.5（响应速度快）
4. qwen3.5-plus（百万上下文）

### Step 5 - 启动龙虾
选模型 kimi-k2.5 | 阿里云百炼，点启动。

### Step 6 - 对接飞书
在 Dashboard 对话框发：「帮我配置飞书，让我能通过飞书手机端跟你对话。一步步引导我，每步做完等我确认再继续」

### Step 7 - 安装 OB + CC
发给龙虾安装指令，它会自动下载 Claudian 插件、cc-switch 等。

## 03 装备技能/给龙虾装必备 Skill

四个地基 Skill：

1. **Multi Search Engine**（免费搜索引擎，17 个引擎覆盖国内外）
   ```
   npx clawhub@latest install multi-search-engine
   ```

2. **x-reader**（国内链接解析：微信公众号、小红书、B 站、X 等）
   ```
   pip install git+https://github.com/runesleo/x-reader.git
   ```

3. **Obsidian**（直接往 OB 知识库存东西）
   ```
   npx clawhub@latest install obsidian
   ```

4. **find-skills**（搜索和发现更多 Skill）
   ```
   npx clawhub@latest install find-skills
   ```

**进阶推荐**：开源 Skill 库 https://github.com/cafe3310/public-agent-skills
覆盖创作与知识管理、在线平台、项目管理、辅助工具四大场景。

## 04 玩起来/实用玩法 + 训练 + 打通

**实用玩法**：
- 随手记：飞书里把碎碎念、文章链接发给龙虾，自动整理存OB
- 定时简报：每天早上推送天气+日程+行业新闻
- 知识库管理：定时让龙虾整理本周笔记，生成周报
- 文件整理：按类型分到不同文件夹

**训练**：龙虾 workspace 有 4 个核心文件：
- USER.md — 你是谁
- SOUL.md — 性格和行事准则
- IDENTITY.md — 名字和形象
- AGENTS.md — 工作手册

第一天就填好 USER.md，其他文件慢慢调。

**打通**：建立软链接让龙虾配置文件出现在 OB 里，双向实时同步。在 OB 编辑 SOUL.md → 龙虾立即生效。

---

以上就完成了：Obsidian + Claude Code + OpenClaw 三者基建的安装，本期就到这。
