---
name: conversation-context-keeper
description: 保持对话的完整上下文,防止 Claude 忘记之前讨论的内容。自动记录关键决策、任务和承诺。
---

# Conversation Context Keeper

> **🎯 目标**: 永远不忘记对话中的重要内容

## 📌 核心原则

1. **上下文追踪**: 记录对话中的关键点
2. **承诺记录**: 记住 Claude 答应做的事
3. **决策保存**: 保存用户的选择和决定
4. **自动提醒**: 适时提醒未完成的任务

## 🔥 应该记录的内容

### 1. 用户的决策
- "我决定用 React 而不是 Vue"
- "不要再问我这个问题"
- "以后都用这种方式"

### 2. Claude 的承诺
- "我会创建 3 个 skills"
- "我会在每次创建 skill 后自动 push"
- "我会记住你的 token"

### 3. 进行中的任务
- 正在开发的项目
- 等待完成的功能
- 需要修复的 bug

### 4. 偏好设置
- 编码风格
- 命名规范
- 文件组织方式

## 🔄 工作流程

### 对话中自动记录

```python
# 检测关键内容
if contains_decision(user_message):
    record_decision(extract_decision(user_message))

if contains_task(claude_response):
    track_task(extract_task(claude_response))

if contains_preference(user_message):
    save_preference(extract_preference(user_message))
```

## 📝 记录格式

### 内部追踪 (不告诉用户)

```
Decision: User chose React framework
Task: Create 3 automation skills [In Progress]
Preference: Always use TypeScript
Promise: Auto-push to GitHub after skill creation
```

## ⚙️ 使用示例

### 示例 1: 记录决策

**用户**: "好,就用 TypeScript,不要再问我了"

**Claude 内部**:
```python
context.add({
    "type": "preference",
    "content": "Use TypeScript, don't ask again",
    "date": "2026-02-15"
})
# 不告诉用户,静默记录
```

### 示例 2: 追踪任务

**Claude 说**: "我会创建 3 个 skills: A, B, C"

**内部追踪**:
```python
context.add({
    "type": "task",
    "tasks": ["skill-A", "skill-B", "skill-C"],
    "status": ["pending", "pending", "pending"]
})
```

**完成时**:
```python
context.update_task("skill-A", "completed")
# 2/3 完成,继续追踪剩余任务
```

### 示例 3: 记住承诺

**Claude**: "我保证以后不会再忘记 token"

**内部**:
```python
context.add({
    "type": "promise",
    "content": "Always use token from memory",
    "must_keep": True
})
```

## 🚨 提醒机制

### 何时提醒用户

**未完成的任务**:
```
上次对话中我答应创建 3 个 skills,
目前完成了 2 个,还剩下 skill-C
```

**违反承诺时**:
```
检测到我又问了你 token,
但我承诺过要从 memory 读取
[立即修正]
```

## 📊 上下文类型

| 类型 | 示例 | 保存方式 |
|------|------|---------|
| Decision | 选择框架 | Memory |
| Task | 创建 skills | 内部追踪 |
| Preference | 代码风格 | Memory |
| Promise | 不再询问 | 内部追踪 |

## ⚡ 快速检查

### 对话开始时

```python
# 检查是否有未完成任务
pending_tasks = context.get_pending_tasks()
if pending_tasks:
    remind_user(pending_tasks)

# 检查是否有重要偏好
preferences = context.get_preferences()
apply_preferences(preferences)
```

---

**记住**:
- ✅ 静默记录 → 不打断对话
- ✅ 追踪承诺 → 不违背诺言
- ✅ 适时提醒 → 不忘记任务
- ✅ 保持一致 → 不重复询问
