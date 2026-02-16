---
name: conversation-startup
description: 新对话自动启动 Skill。每次新对话的第一条消息时自动触发，加载所有 Skills、配置和上次进度，显示完整状态，提供继续选项。合并自原 conversation-starter + conversation-startup 并完善。
---

# Conversation Startup — 新对话自动启动

## 触发时机

每次新对话的第一条消息时自动触发，无论用户说什么（"开始"、"你好"、"继续"、任何内容）都立即执行此流程。不等用户提醒，不只说"你好"然后等待。

---

## 执行流程

### 第 1 步：静默加载环境

**检测当前环境**（决定后续步骤的具体操作方式）：

```
判断方法：
- 如果能访问 /mnt/skills/user/ → Claude.ai 网页/App 环境
- 如果能访问项目目录 + .claude/ → Claude Code 环境
- 如果用户消息来自移动端特征（简短、无代码、口语化）→ 可能在手机上

环境影响：
- Claude.ai：通过 bash_tool 执行，Skills 在 /mnt/skills/user/
- Claude Code：通过终端执行，Skills 在项目 .claude/ 目录
- 手机端：优先简洁回复，减少长代码输出
```

**加载 Skills**：

```bash
find /mnt/skills/user -name "SKILL.md" -type f 2>/dev/null | wc -l
```

**重点读取的 Skills**（按优先级）：
1. work-rules — 核心工作规则（必读，影响所有行为）
2. context-monitor — 上下文管理（必读，影响对话质量）
3. auto-storage — 自动存储流程
4. 与用户当前请求相关的 Skill

**如果 Skills 目录为空或少于 5 个**：尝试从 GitHub 同步（参考 github-skills-sync Skill），同步失败则告知用户并继续工作。

### 第 2 步：加载配置

**从记忆（userMemories）获取**：
- GitHub: krisliong1/oskris + Token
- VPS: 76.13.191.45 + 凭证
- Hostinger API Token
- 域名: oskris.com
- 邮箱: oskrismy@gmail.com

**验证配置可用性**（静默执行，不显示详细过程）：

```bash
# 快速检查 GitHub 连通性（可选，如果网络可用）
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: token TOKEN" \
  https://api.github.com/repos/krisliong1/oskris 2>/dev/null
```

**如果某项配置不可用**：不阻断流程，标记为"⚠️ 需检查"并继续，在状态面板中提示。

### 第 3 步：检查上次进度

**搜索来源**（按优先级）：
1. Claude 记忆系统（userMemories）→ 查看"Top of mind"和"Recent months"
2. recent_chats 工具 → 获取最近对话的主题和状态
3. conversation_search → 搜索特定项目关键词

**提取信息**：
- 上次在做什么项目/任务？
- 有什么待办事项？
- 有什么未完成的工作？
- 用户最近关注什么？

### 第 4 步：显示启动状态

```
━━━━━━━━━━━━━━━━━━━━━━
🔄 系统已就绪
━━━━━━━━━━━━━━━━━━━━━━

✅ 配置
  - Skills: XX 个已加载
  - GitHub: krisliong1/oskris ✅
  - VPS: 76.13.191.45 ✅
  - Hostinger: 已认证 ✅

📋 上次进度
  - [从记忆/历史读取的最近工作内容]
  - [待办事项]

💡 准备就绪
```

**状态面板规则**：
- 简洁，不超过 10 行
- 配置项只显示「✅」或「⚠️ 需检查」，不显示具体 Token 值
- 进度信息从记忆中提取，如果没有就显示「首次对话」
- 不显示详细的加载过程（静默执行）

### 第 5 步：响应用户

根据用户第一条消息的内容决定：

**如果用户说了具体任务**（例如"帮我做个报价单"）：
- 显示简化状态面板（3-5 行）
- 立即开始执行任务
- 不问"要继续还是新任务"

**如果用户只是打招呼**（例如"你好"、"开始"）：
- 显示完整状态面板
- 提供选项：继续上次工作 / 开始新任务

**如果用户说"继续"**：
- 立即用 recent_chats 查找最近对话
- 直接恢复上次工作，不重新显示状态

---

## 错误处理

### Skills 加载失败

```
情况：/mnt/skills/user/ 为空或不可访问
处理：
1. 尝试从 GitHub 克隆：git clone ... /tmp/oskris
2. 从 /tmp/oskris/skills/ 读取 Skills
3. 如果 GitHub 也失败 → 告知用户，基于记忆中的规则继续工作
4. 不阻断对话，降级运行
```

### 配置缺失

```
情况：记忆中找不到某项配置
处理：
1. 标记该项为 ⚠️
2. 需要使用时才询问用户
3. 不在启动时就连续追问所有缺失项
```

### 网络不可用

```
情况：无法访问 GitHub/VPS/Hostinger API
处理：
1. 跳过连通性检查
2. 基于本地 Skills 和记忆工作
3. 需要网络操作时才提示
```

---

## 降级策略

当无法完成完整启动流程时，按以下顺序降级：

```
完整启动（所有步骤）
    ↓ Skills 不可用
简化启动（跳过 Skills 加载，用记忆中的规则）
    ↓ 记忆也很少
最小启动（直接响应用户，不显示状态面板）
```

核心原则：**永远不因为启动流程失败而阻断用户的实际需求**。启动是辅助，用户的任务是核心。

---

## 禁止行为

1. ❌ 只说"你好"然后等待，不加载任何东西
2. ❌ 显示冗长的加载过程（每一步都报告）
3. ❌ 在状态面板中暴露完整 Token/密码
4. ❌ 因为某项配置缺失就拒绝工作
5. ❌ 用户说了具体任务还在问"要做什么"
6. ❌ 每次都执行完全相同的启动输出（应根据用户消息调整详细程度）

---

## 与其他 Skills 的配合

- **work-rules**：启动后所有行为遵循工作规则
- **auto-storage**：启动时检查是否有上次未存储的内容
- **context-monitor**：启动时初始化上下文监控（记录第 1 轮）
- **github-skills-sync**：Skills 缺失时触发同步
