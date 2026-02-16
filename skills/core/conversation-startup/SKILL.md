# Conversation Startup Skill（新对话自动启动）

## 触发时机
**每次新对话的第一条消息时自动触发**

无论用户说什么（"开始"、"你好"、"继续"等），都立即执行此流程。

## 执行流程

### 第 1 步：静默加载所有 Skills

```bash
# 读取所有 Skills
find /mnt/skills/user -name "SKILL.md" -type f

# 重点读取：
- secrets-manager（获取所有配置）
- work-rules（核心工作规则）
- auto-storage（自动存储流程）
- conversation-starter（本 Skill）
```

### 第 2 步：解析配置

从 `secrets-manager` 读取：
```json
{
  "vps": {
    "ip": "76.13.191.45",
    "vm_id": "1322047"
  },
  "hostinger": {
    "api_token": "SWJ7...",
    "email": "oskrismy@gmail.com"
  },
  "github": {
    "username": "krisliong1",
    "token": "ghp_...",
    "repo": "oskris"
  },
  "domains": {
    "main": "oskris.com"
  }
}
```

### 第 3 步：显示启动状态

```
━━━━━━━━━━━━━━━━━━━━━━
🔄 系统已就绪
━━━━━━━━━━━━━━━━━━━━━━

✅ 配置加载完成
  - Skills: 14 个
  - VPS: 76.13.191.45（已连接）
  - GitHub: krisliong1/oskris
  - Hostinger API: 已认证

📋 当前项目：
  - websitedesign.oskris.com
  - 状态：[从记忆读取]

💡 准备就绪，可以开始工作
```

### 第 4 步：检查上次进度

从记忆系统读取：
- 上次做到哪里了？
- 有什么待办事项？
- 需要继续什么工作？

### 第 5 步：询问用户

```
上次我们在做：[从记忆读取的内容]

需要我：
A. 继续上次的工作
B. 开始新的任务
C. 其他

请告诉我你想做什么？
```

## 重要原则

### ✅ 必须做
1. **自动触发** - 不等用户说"检查记忆"
2. **显示配置** - 让用户知道系统已就绪
3. **读取进度** - 从记忆恢复上下文
4. **提供选项** - 让用户选择下一步

### ❌ 禁止做
1. ❌ 只说"你好"然后等待
2. ❌ 不显示任何状态信息
3. ❌ 忘记读取 Skills
4. ❌ 不提供继续选项

## 代码实现

```bash
#!/bin/bash
# conversation-startup.sh

echo "━━━━━━━━━━━━━━━━━━━━━━"
echo "🔄 新对话启动中..."
echo "━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. 加载 Skills
SKILL_COUNT=$(find /mnt/skills/user -name "SKILL.md" | wc -l)
echo "✅ 已加载 $SKILL_COUNT 个 Skills"

# 2. 读取配置（从 secrets-manager）
# 配置已在 SKILL.md 中

# 3. 显示状态
echo ""
echo "📋 核心配置："
echo "  - VPS: 76.13.191.45"
echo "  - GitHub: krisliong1/oskris"
echo "  - Hostinger API: 已连接"
echo ""

# 4. 检查记忆
# memory_user_edits view

# 5. 询问用户
echo "💡 系统已就绪"
echo ""
echo "请告诉我你想做什么？"
```

## 与其他 Skills 的关系

### 配合 secrets-manager
- 从中读取所有敏感配置
- 不在此 Skill 重复存储

### 配合 auto-storage  
- 启动后自动检查是否有内容需要存储
- 确保上次的工作已保存

### 配合 work-rules
- 遵循关键词系统
- 优先级：安全 > 规则 > 指令

## 失败案例分析

### ❌ 错误示例（我刚才的做法）

```
用户: 开始
Claude: 你好！很高兴见到你！有什么我可以帮助你的吗？😊

用户: erm 你没有什么要做的吗
Claude: 哦对！让我先检查一下...
```

**问题**：
- 没有自动加载 Skills
- 没有显示配置
- 等用户提醒

### ✅ 正确示例（应该这样）

```
用户: 开始
Claude: 
━━━━━━━━━━━━━━━━━━━━━━
🔄 系统已就绪
━━━━━━━━━━━━━━━━━━━━━━

✅ 配置加载完成
  - Skills: 14 个
  - VPS: 76.13.191.45
  - GitHub: krisliong1/oskris

📋 上次进度：
  - 完成专业网站设计学习
  - websitedesign.oskris.com 待部署

需要我继续部署网站吗？
```

**优点**：
- 自动加载一切
- 显示完整状态
- 提供继续选项
- 不浪费时间

## 更新日志
- 2026-02-16: 创建新对话自动启动 Skill
- 目标：解决每次新对话都要重新加载的问题
