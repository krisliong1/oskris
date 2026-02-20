---
name: openclaw-agent
description: >-
  OpenClaw全生命周期管理Agent。协调安装、配置、认证、故障排除、升级的完整流程。
  当用户说"安装openclaw"、"openclaw坏了"、"openclaw连不上"、"升级openclaw"、
  "openclaw设置"、"重装openclaw"时触发。自动诊断问题并执行修复，协调
  openclaw-manager skill完成具体操作。
---

# OpenClaw Agent — 全生命周期管理

协调OpenClaw从安装到日常维护的完整工作流。

## Agent架构

```
OpenClaw Agent (协调者)
    ├── 安装流程 → [openclaw-manager] 基础配置
    ├── 认证流程 → [openclaw-manager] token管理
    ├── 诊断流程 → 自动检测+修复
    ├── 升级流程 → 版本管理+迁移
    └── Channel流程 → 平台连接管理
```

## 工作流

### 1. 首次安装

```
检测环境 → 安装Node.js → 安装OpenClaw → 创建用户 → 配置认证 → 连接Channel → 测试
```

**Mac安装命令：**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard
```

**需要准备：**
- Claude Max/Pro订阅（用claude setup-token获取token）
- Telegram Bot Token（从@BotFather获取）
- Node.js 18+

### 2. 认证流程（最常见操作）

```
检测token状态 → 过期？→ 重新生成 → 粘贴 → 重启 → 验证
```

**完整步骤：**
```bash
# 1. 检查当前状态
openclaw models status

# 2. 生成新token（需要claude命令可用）
claude setup-token

# 3. 粘贴token
openclaw models auth paste-token --provider anthropic

# 4. 重启gateway
openclaw gateway restart

# 5. 验证
openclaw models status
```

**跨用户操作（从oskris操作openclaw）：**
```bash
su - openclaw
# 或
sudo -u openclaw openclaw models status
```

### 3. 故障诊断流程

```
用户报告问题 → 收集信息 → 分类 → 执行修复 → 验证
```

**诊断命令：**
```bash
openclaw doctor                              # 全面诊断
openclaw gateway status                      # gateway状态
openclaw models status                       # 认证状态
tail -20 ~/.openclaw/logs/gateway.log        # 最近日志
```

**常见问题速查：**

| 症状 | 原因 | 修复 |
|------|------|------|
| 401 Unauthorized | Token过期 | `claude setup-token` → `paste-token` |
| gateway token missing | 没配token | `openclaw models auth paste-token --provider anthropic` |
| 命令找不到 | PATH问题 | `export PATH="$HOME/.npm-global/bin:$PATH"` |
| 连不上Telegram | Bot token问题 | 检查 `openclaw config get channels.telegram` |
| gateway启动失败 | 端口占用 | `lsof -i :18789` 然后kill进程 |
| SQLITE_CANTOPEN | macOS TMPDIR问题 | 已在新版修复，升级OpenClaw |

### 4. 升级流程

```bash
# 检查当前版本
openclaw --version

# 升级
npm update -g openclaw

# 重启
openclaw gateway restart

# 验证
openclaw doctor
```

### 5. Channel管理

**添加Telegram：**
```bash
openclaw config set channels.telegram.accounts.main.token "<BOT_TOKEN>"
openclaw gateway restart
```

**添加WhatsApp：**
```bash
openclaw onboard  # 选WhatsApp选项，扫码
```

## 环境信息

| 项目 | 值 |
|------|-----|
| Mac用户 | openclaw |
| 日常用户 | oskris |
| 配置路径 | /Users/openclaw/.openclaw/ |
| 认证方式 | Claude Max OAuth (sk-ant-oat01-...) |
| 推荐模型 | anthropic/claude-opus-4-6 |
| Gateway端口 | 18789 |

## Token类型对比

| 类型 | 前缀 | 有效期 | 推荐 |
|------|------|--------|------|
| setup-token | oat01 | 长期(最长1年) | ✅ 给OpenClaw用 |
| access token | oat01 | 8小时 | ❌ 太短 |
| refresh token | ort01 | 一次性 | ❌ 用完失效 |
| API key | api03 | 永久 | ⚠️ 按量付费 |

## 与其他Skill的关系

- **openclaw-manager** → 具体命令和配置参考
- **vps-manager** → VPS端部署时的服务器管理
- **learning** → 学习OpenClaw新功能时的研究流程

## 安全要点

- Anthropic已确认：Max订阅用于OpenClaw不违反TOS
- 不要用root运行
- 监控日志防止prompt injection攻击
- 社区skills安装前审查代码

**最后更新**: 2026-02-20
