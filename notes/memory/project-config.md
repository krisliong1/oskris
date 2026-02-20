# Oskris Project — 多平台AI配置

最后更新: 2026-02-20

---

## 平台矩阵

| 平台 | 工作路径 | 存储路径 | 能力 |
|------|---------|---------|------|
| **Claude.ai** | `/home/claude`(临时) | `/mnt/user-data/outputs` | python, bash, web search |
| **Claude Desktop** | `/Users/oskris/` | 同左 + GitHub | filesystem MCP, github MCP |
| **Claude Code** | 项目目录 | 同左 + GitHub | 完整终端, git |
| **OpenClaw** | `/Users/oskris/openclaw/` | 同左 + GitHub | shell, 浏览器, 多平台聊天 |

---

## 通用规则（所有平台必须遵守）

### 文件保护
1. 修改现有文件前必须问用户确认
2. 新文件可直接创建
3. 流程：显示diff → 确认 → 备份 → 修改 → changelog
4. 操作前先检查文件是否存在

### 代码与语言
5. 代码/命令/技术术语英文，其他华文
6. 价格用RM
7. 禁止placeholder，用真实数据（见Project配置）
8. 命令不加注释

### 质量与存储
9. 专业级标准
10. 先验证再执行
11. 创建/修改文件后推送GitHub + 告知用户
12. 敏感信息禁止存GitHub

---

## 平台专属规则

### Claude.ai
- 输出放 `/mnt/user-data/outputs/`
- GitHub用 `/tmp` 克隆操作
- 提醒用户去Desktop同步

### Claude Desktop
- 检测filesystem MCP → Mac本地同步
- 可读写: `/Users/oskris/Desktop`, `Documents`, `Downloads`
- MCP: filesystem, github, hostinger-api-mcp

### Claude Code
- 完整终端，直接git
- OAuth token存Keychain

### OpenClaw
- 工作路径: `/Users/oskris/openclaw/`
- 运行用户: user:openclaw
- Gateway: 18789
- 认证: setup-token(oat01) 优先
- 命令: `openclaw gateway start/stop/restart/status`

---

## 基础设施
- GitHub: krisliong1/oskris (活跃) + krisliong1/backup (存放)
- 域名: oskris.com (2027+), kkh.oskris.com, websitedesign.oskris.com
- 服务器凭据: 见Project配置
- Context Window监控: 30%警告, 40%建议新对话, 50%必须停止

---

## 当前项目
- websitedesign.oskris.com (待部署)
- OskrisAgent Telegram Bot (VPS)
- rl-trading-ai (Claude Code开发中)
