---
name: conversation-startup
description: 新对话自动启动流程。每次新对话第一条消息时自动触发，加载Skills、配置、上次进度，显示状态。即使Claude记忆丢失也能通过此Skill恢复完整工作环境。
---

# Conversation Startup

每次新对话第一条消息时自动触发，无论用户说什么。

## 执行流程

### 1. 检测环境

- 能访问 /mnt/skills/user/ → Claude.ai
- 能访问项目目录 + .claude/ → Claude Code
- 用户消息简短口语化 → 可能手机端，优先简洁回复

### 2. 加载Skills

```bash
find /mnt/skills/user -name "SKILL.md" -type f 2>/dev/null | wc -l
```

重点读取顺序：work-rules → context-monitor → github-ops → 与用户请求相关的skill

Skills不足5个时，从GitHub同步：
```bash
cd /tmp && rm -rf oskris
git clone https://krisliong1:{TOKEN}@github.com/krisliong1/oskris.git
cp -r /tmp/oskris/skills/* /mnt/skills/user/ 2>/dev/null || true
```

### 3. 加载配置（从记忆或此Skill获取）

```
GitHub: krisliong1/oskris
VPS: 76.13.191.45 (Ubuntu 25.10, 2核8GB, Malaysia)
域名: oskris.com (Hostinger Cloud Startup, 到期2027)
邮箱: oskrismy@gmail.com / official@oskris.com
业务: 网站设计，定价 RM 1,999/4,999/9,999
语言: 中文沟通，代码保持英文
```

### 4. 检查上次进度

来源：Claude记忆 → recent_chats → conversation_search

提取：上次项目/任务、待办事项、未完成工作。

### 5. 显示状态（简洁，不超过10行）

```
🔄 系统就绪
✅ Skills: XX个  |  GitHub: ✅  |  VPS: ✅
📋 上次: [从记忆/历史提取]
```

### 6. 响应用户

- 用户说了具体任务 → 简化状态(3行) + 立即执行
- 用户打招呼 → 完整状态 + 提供选项
- 用户说「继续」→ recent_chats查找，直接恢复

## 降级策略

```
完整启动 → Skills不可用时用记忆规则 → 记忆也少时直接响应
```

核心原则：**永不因启动失败阻断用户需求**。

## 禁止

- 只说「你好」不加载任何东西
- 显示冗长加载过程
- 暴露完整Token/密码
- 配置缺失就拒绝工作
