---
name: core-rules
description: >-
  Oskris项目核心规则总集。所有环境（claude.ai、Claude Code、Telegram Agent）通用。
  包含：双仓库工作流、自动存储规则、手动更新提醒、文件保护、代码规则、Context Window监控、
  Skills触发词速查。每次新对话自动应用。当需要确认工作规则、检查流程、或在新环境初始化时触发。
---

# Core Rules — Oskris项目核心规则

所有环境通用的工作规则。Project Instructions的skill备份版。

## 身份与语言

- 用户零代码基础，Claude负责学习+执行
- 代码/命令/技术术语保持英文，其他用华文回复
- 所有价格用RM（马来西亚令吉）
- 质量标准：专业级（Level 4），不接受初级操作

## 双仓库工作流

| 仓库 | 用途 | Claude行为 |
|------|------|-----------|
| `krisliong1/oskris` | 🟢 活跃工作区 | 正常读写、触发skill |
| `krisliong1/backup` | 🔒 存放/备份 | **不触发skill**，用户要求查历史版本时才搜索 |

- 凭据从Claude记忆或Project Instructions读取
- 只推main分支，用/tmp克隆操作
- Git credentials: user.email "oskrismy@gmail.com", user.name "oskris"

## 自动存储规则（每次创建/修改文件后）

1. 推送到 krisliong1/oskris（活跃区）
2. 推送到 krisliong1/backup/YYYY-MM-DD_HHMMSS/（存放区，完整快照）
3. Desktop模式时同时写入Mac本地
4. claude.ai模式提醒用户去Desktop同步
5. 敏感信息禁止存GitHub，只存VPS+记忆
6. 每步告诉用户同步了哪些文件到哪里

## 手动更新提醒规则（每次推送后必须检查）

1. Project Instructions是否需要同步更新
2. Project Knowledge文件是否需要新增/改名
3. /mnt/skills/user/ 是否需要部署新skill
4. 记忆(memory edits)是否需要用户确认
如有需要用户手动操作的，列出具体步骤，不能省略。

## 文件保护系统

- 新文件可直推
- 修改现有文件必须：显示diff → 用户确认 → 自动备份到 backups/ → 记录 logs/changelog.md
- 改任何东西前必须先告诉用户确认才改，不能直接改

## 代码规则

- 先验证再执行：搜索确认方案可行后再写代码
- 操作文件前先检查是否存在，已存在用str_replace修改
- 提供命令不加#注释，只给纯代码
- 禁止placeholder，用真实数据
- 工具失败最多重试2次，立即告知用户+给替代方案
- Skill行数标准: ≤1000行

## 环境自动检测

**检测到 `filesystem:` MCP工具 → Mac Desktop模式**
- 读写 /Users/oskris/Desktop、Documents、Downloads
- 文件同时写入Mac本地 + 上传GitHub

**没有MCP工具 → claude.ai/iOS模式**
- 上传GitHub
- 创建文件到 /mnt/user-data/outputs/

## Context Window监控

- 每10轮主动报告估计用量%
- 30% → 警告
- 40% → 强烈建议开新对话
- 50% → 必须停止
- 降级是悬崖式非线性的

## Skills存放位置与读取规则

| 位置 | Claude自动读取？ | 说明 |
|------|-----------------|------|
| `/mnt/skills/user/` | ✅ 自动触发 | claude.ai根据触发词读取 |
| Project Knowledge | ✅ 每次都在context | 当前Project参考 |
| GitHub `krisliong1/oskris/skills/` | ⚡ 被指令要求时搜索 | 活跃区 |
| GitHub `krisliong1/backup/` | 🔒 不主动搜索 | 存放区 |

## 基础设施速查

- VPS: root@76.13.191.45 (Ubuntu 25.10, 2核8GB, Malaysia)
- Hosting: u212717065@76.13.178.156:65002
- Hostinger API: 见Claude记忆
- 域名: oskris.com(2027+), kkh.oskris.com, websitedesign.oskris.com
- Telegram Bot: [见Claude记忆] (@oskrismy ID:8552991398)
- 用户设备: iPhone 15 Pro (iOS 26.1), Mac Mini M4

## iOS快捷指令系统

- 签名: AEA1 → LZVN/LZFSE解压 → bplist, `shortcuts sign -m anyone`
- WFCondition: 100=有值, 101=没值
- 4个skill: ios-shortcuts, ios-shortcuts-builder, ios-shortcuts-parser, ios-shortcuts-studio
- 工具链: Shortcut Source Helper(#10060), Shortcut Source Tool(#5256)
- 触发: "做快捷指令"、"创建shortcut"、"分析shortcut"、"修改快捷指令"

## iOS mobileconfig

- 格式: plist XML, PayloadType: com.apple.dnsSettings.managed
- 多DNS payload一个文件, Duplicates allowed: True
- 组织名: oskris.com
- 触发: "描述文件"、"mobileconfig"、"DNS/VPN/Wi-Fi配置"

## 活跃Skills触发词（22个，/mnt/skills/user/）

| Skill | 触发词 |
|-------|--------|
| sales-agent | "new lead"、"potential client"、"sales pipeline"、"close deal" |
| site-health-agent | "check website"、"site health"、"website audit"、"security scan" |
| vps-manager | "check server"、"server status"、"VPS health"、"restart service" |
| site-deployer | "deploy site"、"go live"、"DNS setup"、"SSL setup" |
| seo-optimizer | "SEO audit"、"check SEO"、"improve ranking"、"keyword research" |
| social-media-content | "create post"、"social media"、"Facebook/Instagram/TikTok" |
| portfolio-builder | "case study"、"portfolio"、"showcase project" |
| email-templates | "write email"、"email client"、"follow up email"、"payment reminder" |
| client-proposal-generator | "create proposal"、"quotation"、"write quote" |
| client-onboarding | "new client"、"onboard"、"client intake"、"kickoff" |
| project-tracker | "project status"、"track progress"、"milestone check" |
| delivery-calculator | "delivery fee"、"运费"、"运输费"、"KKH delivery"、"送货费" |
| project-workflow | 管理客户项目全流程 |
| design-consultant | 需求→设计方案、配色、布局 |
| frontend-builder | 建网站、mockup→代码 |
| frontend-design | web组件、landing page、dashboard |
| app-recommendations | App推荐、应用对比 |
| product-self-knowledge | Claude/Anthropic产品问题 |
| auto-translate | 英文消息自动中文回复 |
| smart-info-manager | 自动识别关键信息分类存储 |
| core-work-rules | 基础工作原则（自动） |
| work-rules | 核心工作规则（自动） |

## GitHub未部署Skills（需手动搜索）

| 分类 | Skills |
|------|--------|
| iOS快捷指令 | ios-shortcuts, ios-shortcuts-builder, ios-shortcuts-parser, ios-shortcuts-studio |
| iOS配置 | ios-mobileconfig, dns-adblock |
| 网站设计 | web-design-studio, requirements-analyst, design-enhancement, web-artifacts-builder |
| 品牌 | oskris-brand-guidelines |
| 业务 | oskris-invoice-manager, doc-coauthoring, internal-comms |
| 创意 | algorithmic-art, canvas-design, oskris-gif-creator, theme-factory |
| 开发 | mcp-builder, skill-creator |
| 学习 | learning, professional-web-design, claude-code-mastery, prompt-engineering-enhanced |
| Core存放 | auto-storage, context-keeper, conversation-starter, conversation-startup, github-ops, memory-updater |
| Agents存放 | conversation-context-keeper, github-auto-auth, github-change-tracker, github-skills-sync, memory-auto-updater, skill-auto-sync |
| 文档(内置) | docx, pdf, pptx, xlsx |

## 用户说"继续"时

立即用recent_chats或conversation_search查找上下文继续，不说"这是对话的开始"。

---
最后更新: 2026-02-19
