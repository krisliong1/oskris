---
name: openclaw-manager
description: >-
  管理和配置OpenClaw个人AI助手。当用户说"openclaw"、"open claw"、
  "配置openclaw"、"openclaw token"、"openclaw重启"、"openclaw技能"、
  "openclaw channel"、"openclaw模型"时触发。涵盖安装、认证、模型配置、
  channel管理、skills管理、故障排除。OpenClaw装在Mac Mini的user:openclaw用户下。
---

# OpenClaw Manager

管理运行在Mac Mini M4 `user:openclaw` 上的OpenClaw个人AI助手。

## 环境信息

- **安装位置**: Mac Mini M4, 用户 `openclaw`
- **日常用户**: `oskris`（从这里管理openclaw用户的设置）
- **认证方式**: Claude Max订阅 OAuth token (sk-ant-oat01-...)
- **配置目录**: `/Users/openclaw/.openclaw/`
- **主配置文件**: `/Users/openclaw/.openclaw/openclaw.json`

## 核心命令速查

### 认证（最常用）

```bash
# 第1步：生成token（在有claude命令的终端）
claude setup-token

# 第2步：粘贴到OpenClaw（在user:openclaw终端）
openclaw models auth paste-token --provider anthropic

# 检查认证状态
openclaw models status
```

### Gateway管理

```bash
openclaw gateway start        # 启动
openclaw gateway stop         # 停止
openclaw gateway restart      # 重启
openclaw gateway status       # 状态
```

### 配置管理

```bash
openclaw config get <key>     # 读取配置
openclaw config set <key> <value>  # 修改配置
openclaw doctor               # 诊断问题
openclaw onboard              # 重新走设置向导
```

### Skills管理

```bash
openclaw skills list          # 查看已安装skills
openclaw skills install <name> # 安装skill
openclaw skills remove <name>  # 移除skill
```

### 模型管理

```bash
openclaw models list          # 查看可用模型
openclaw models status        # 查看认证状态
openclaw models set <model>   # 切换默认模型
```

## 跨用户操作

从 `user:oskris` 终端操作 `user:openclaw` 的OpenClaw：

```bash
# 方法1: sudo -u
sudo -u openclaw openclaw gateway restart
sudo -u openclaw openclaw models status

# 方法2: 切换用户
su - openclaw
# 执行命令后 exit 回来
```

## 认证详解

### Token类型

| Token | 前缀 | 有效期 | 来源 |
|-------|------|--------|------|
| Access Token | sk-ant-oat01-... | 8小时 | keychain提取/refresh刷新 |
| Refresh Token | sk-ant-ort01-... | 长期 | 一次性，用后失效 |
| Setup Token | sk-ant-oat01-... | 长期(最长1年) | `claude setup-token` ✅推荐 |
| API Key | sk-ant-api03-... | 永久 | console.anthropic.com（按量付费）|

**推荐**: 用 `claude setup-token` 生成长期token给OpenClaw。

### Token过期处理

```bash
# 检查是否过期
openclaw models status

# 重新生成并粘贴
claude setup-token
openclaw models auth paste-token --provider anthropic

# 重启生效
openclaw gateway restart
```

### Keychain提取（备用方案）

```bash
security find-generic-password -s "Claude Code-credentials" -w
```

输出JSON含accessToken和refreshToken。

### Refresh Token刷新（紧急方案）

```bash
curl -s -X POST https://console.anthropic.com/v1/oauth/token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "refresh_token",
    "refresh_token": "你的sk-ant-ort01-...",
    "client_id": "9d1c250a-e61b-44d9-88ed-5944d1962f5e"
  }'
```

⚠️ refresh token一次性，用完旧的失效。

## Channel配置

### Telegram

```bash
openclaw config set channels.telegram.accounts.main.token "<BOT_TOKEN>"
```

### WhatsApp

```bash
openclaw onboard  # 选WhatsApp，扫码连接
```

## 常见问题

### 401 Unauthorized
- Token过期 → 重新 `claude setup-token` + `paste-token`
- OAuth token不被支持 → 用 `sk-ant-api03-...` API key替代

### gateway token missing
- 没粘贴token → 跑 `openclaw models auth paste-token --provider anthropic`

### 命令找不到
- PATH没配好 → `export PATH="$HOME/.npm-global/bin:$PATH"`
- 或找到完整路径: `find / -name "openclaw" -type f 2>/dev/null`

### 跨用户权限问题
- 用 `sudo -u openclaw` 前缀
- 或 `su - openclaw` 切换用户

## 架构概览

```
WhatsApp / Telegram / Discord
         │
         ▼
┌─────────────────┐
│  OpenClaw       │
│  Gateway        │  ← ws://127.0.0.1:18789
│  (user:openclaw)│
└────────┬────────┘
         │
         ├─ Claude API (anthropic/claude-opus-4-6)
         ├─ Skills (文件操作、浏览器控制等)
         ├─ Memory (MEMORY.md, SOUL.md)
         └─ Workspace (~/.openclaw/workspace/)
```

## 安全注意事项

- 永远不要用root运行OpenClaw
- 限制文件访问范围（Allowlist）
- 监控日志: `tail -f ~/.openclaw/logs/gateway.log`
- 社区skills有安全风险，安装前审查
- Anthropic已确认Max订阅用于OpenClaw不违反TOS

## 与OskrisAgent的区别

| 对比 | OskrisAgent | OpenClaw |
|------|------------|----------|
| 架构 | Python + Telegram Bot | Node.js + 多平台Gateway |
| 部署 | VPS 76.13.191.45 | Mac Mini user:openclaw |
| 模型 | Claude API (API key) | Claude Max (OAuth token) |
| 功能 | 基础工具调用 | 完整Agent系统(Skills/Memory/Browser) |

**最后更新**: 2026-02-20
