---
来源：GitHub
链接：https://github.com/EthanYoQ/agent-xiaohongshu-workbench
时间：2026-07-15
平台：GitHub
作者：EthanYoQ
---

# Agent 小红书工作台

一个依托 Codex CLI 运行的本地小红书图文内容工作台：从热点研究、笔记拆解、原创文稿和去 AI 味，到品牌配图、完整预览与人工确认发布。

面向需要持续运营单账号图文内容的创作者。不接入第三方模型 API，也不托管账号数据；Codex Agent 在本地环境中完成推理和浏览器操作。

## 解决的问题

小红书图文创作常卡在"热点很多，但不知道如何变成符合账号调性的原创内容"。

工作台将过程拆成可检查、可编辑、可暂停的步骤：
1. 输入账号定位，研究当前小红书图文热点，只保留已验证媒体类型和互动数据的爆款图文笔记
2. 给出恰好 5 个可编辑的选题方向，结合已发布主题保持内容故事线连续性
3. 用内置 Lingzao Skill 拆解热点笔记中可借鉴的标题、信息节奏与表达机制（不复制原文/原图）
4. 生成初稿 → 中文去 AI 味形成可编辑终稿
5. 本地上传头像母版 → 提取身份锁 → 生成 6 个系列品牌形象（后续只改变动作、手势和表情）
6. 由选题和拆解推荐动态视觉方向 → 用户选择 1-6 张配图
7. 完整预览 → 确认 → 立即发布或暂缓发布

## 完整工作流

```
账号定位
  → 本地上传头像母版
  → 身份锁与 6 个系列品牌形象
  → 图文爆款检索（排除视频与低互动笔记）
  → 5 个可编辑选题
  → Lingzao 单一 Skill 热点拆解
  → 选择 1-6 张配图
  → 原始文稿
  → 中文去 AI 味
  → 动态视觉推荐与品牌角色配图
  → 完整预览 / 输入修改意见
  → 立即发布 或 暂存离开
  → 可核验发布写入故事线 / 创作后台只读恢复同步
```

## 阶段分工

| 阶段 | 由谁执行 | 关键约束 |
|------|---------|---------|
| 热点研究 | Codex Agent + OpenCLI 浏览器会话 | 仅保留纯图文，赞≥300、藏≥100或赞藏合计≥400；评论不能单独达标 |
| 热点拆解 | Codex Agent + 内置 Lingzao Skill | 只迁移结构和机制，不复制原句/经历/图片/版式 |
| 文稿与去 AI 味 | Codex Agent + 内置中文润色 Skill | 原始文稿和去 AI 味版本均可编辑 |
| 品牌角色 | Codex Agent 内置生图能力 | 本地上传母版；固定身份、发型、穿着、比例与渲染方式 |
| 配图 | Codex Agent 内置生图能力 | 用户选 1-6 张；不把提示词/思考过程写入图片 |
| 发布 | Codex Agent + 用户浏览器会话 | 必须先预览确认；暂缓发布只能点击"暂存离开" |
| 故事线 | Codex Agent + 当前账号只读会话 | 自动发布需 ID/URL 才入档；创作后台回退到已核验主页 |

## 快速开始

### 前置条件
- Node.js >= 22.13
- 已自行安装并登录的 Codex CLI
- Chrome 及小红书登录会话
- OpenCLI Browser Bridge 扩展

### 安装
```bash
git clone https://github.com/EthanYoQ/agent-xiaohongshu-workbench.git
cd agent-xiaohongshu-workbench
npm install
npm run setup
npm run dev
```

打开终端提示的本地地址（默认 http://127.0.0.1:4173）。

### 连接浏览器
首次执行"图文热点检索"或发布前：
1. Chrome 中安装并启用 OpenCLI Browser Bridge 扩展
2. 用自己的账号登录小红书
3. 根据扩展提示连接 Browser Bridge
4. 回到本地工作台，输入账号定位开始检索

## 运行模型与推理强度

默认模型 gpt-5.6-terra（通过 Codex CLI 调用）。
- **medium**：热点检索、头像/配图、纯视觉修改、故事线同步、发布
- **high**：Lingzao 拆解、初稿、去 AI 味、涉及文稿的修改

## 内置 Skill

| 内容 | 用途 | 来源 |
|------|------|------|
| OpenCLI | 通过用户浏览器会话读取热点、填写内容、发布 | @jackwener/opencli |
| Lingzao Skill | 热点笔记结构化拆解与原创仿写边界 | atian-create/lingzao-skill |
| 中文去 AI 味 Skill | 去套话、翻译腔和机械排比 | MIT |
| OpenCLI 浏览器 Skill | Codex Agent 的浏览器操作说明 | jackwener/opencli |

## 隐私边界

- 公开仓库从空白工作区启动，不含任何账号定位、热点 URL、笔记、图片等
- 热点研究排除视频/混合媒体/无法确认媒体类型的内容
- 爆款门槛：赞≥300、藏≥100或赞藏≥400
- 任何发布动作都需要预览确认
- "立即发布"拿到可验证笔记 ID/URL 才记为成功
- 不编辑作品，不读取评论

## 项目结构

```
├─ .agents/skills/          # 工作流 Skill（Lingzao、去AI味、浏览器）
├─ server/                  # 本地 Agent 编排、状态与发布守卫
├─ src/                     # 本地工作台前端
├─ scripts/                 # 媒体探针、图片处理、运行时检查
├─ public/                  # 项目 logo
├─ packages/share-site/     # 可选静态协作预览站点
├─ docs/seo/                # 仓库 SEO 元数据
└─ test/                    # 核心工作流单元测试
```
