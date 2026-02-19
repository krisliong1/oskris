---
name: memory-auto-updater  
description: 自动更新 Claude 的记忆。任何提到 "GitHub", "记忆", "memory" 的对话都会触发记忆更新,确保永远不会忘记重要信息。
---

# Memory Auto Updater

> **🎯 目标**: 永远不忘记用户的信息,自动更新记忆

## 📌 核心原则

1. **自动触发**: 检测到关键词立即更新记忆
2. **静默执行**: 不询问用户,直接更新
3. **永久保存**: 使用 memory_user_edits 工具
4. **不重复**: 检查是否已存在,避免重复

## 🔥 触发关键词

**立即触发记忆更新的关键词**:
- "GitHub" / "github"
- "记忆" / "memory" / "记住" / "别忘了"
- "永远" / "always" / "forever"
- "token" / "密码" / "password"
- "重要" / "important"
- "以后" / "later" / "下次"

## 🔄 工作流程

### 检测 → 提取 → 保存

```python
# 1. 检测触发词
if any(keyword in user_message for keyword in ['GitHub', '记忆', 'token']):
    # 2. 提取关键信息
    info = extract_key_info(user_message)
    
    # 3. 检查是否已存在
    if not exists_in_memory(info):
        # 4. 保存到记忆
        memory_user_edits(command="add", control=info)
```

## 💾 应该保存的信息

### 1. GitHub 相关
- Token: `ghp_...`
- 仓库名: `krisliong1/oskris`
- 分支: `main`
- 用户名: `krisliong1`

### 2. 技术偏好
- 编程语言偏好
- 框架选择
- 工具使用习惯

### 3. 工作流程
- 提交流程
- 测试要求
- 代码规范

### 4. 个人信息
- 语言偏好: 中文
- 时区
- 常用路径

## ⚙️ 使用示例

### 示例 1: GitHub Token

**用户说**: "ghp_ABC123 这是我的 GitHub token,永远记住"

**Claude 应该**:
```python
memory_user_edits(
    command="add",
    control="User's GitHub token: ghp_ABC123 for krisliong1/oskris"
)
# ✅ 保存成功,不告诉用户
```

### 示例 2: 工作偏好

**用户说**: "记住,我的代码都要用 TypeScript,不要用 JavaScript"

**Claude 应该**:
```python
memory_user_edits(
    command="add", 
    control="User prefers TypeScript over JavaScript for all projects"
)
```

### 示例 3: 路径信息

**用户说**: "我的项目都在 ~/oskris,别忘了"

**Claude 应该**:
```python
memory_user_edits(
    command="add",
    control="User's projects location: ~/oskris"
)
```

## 🚫 不应该保存的

- ❌ 临时信息(今天吃什么)
- ❌ 一次性任务
- ❌ 对话中的闲聊
- ❌ 已经存在的信息

## 🔍 检查流程

### 每次触发时:

1. **查看现有记忆**
```python
memory_user_edits(command="view")
```

2. **检查是否重复**
```python
if new_info not in existing_memory:
    save_to_memory(new_info)
```

3. **静默完成**
- 不说"我已经保存了"
- 不说"记忆已更新"
- 直接执行,继续对话

## 📋 标准格式

**保存格式要简洁**:
```
✅ 好的格式:
"User's GitHub token: ghp_ABC123"
"Prefers TypeScript over JavaScript"
"Projects location: ~/oskris"

❌ 不好的格式:  
"用户在2024年2月15日告诉我他的GitHub token是ghp_ABC123..."
```

## ⚡ 快速参考

### 触发关键词列表
```
GitHub, github
记忆, 记住, memory, remember
永远, always, forever  
Token, token
重要, important
以后, later, 下次
密码, password
别忘了, don't forget
```

### 自动保存示例

| 用户说的话 | 保存内容 |
|-----------|---------|
| "我的 GitHub 是 krisliong1" | "GitHub username: krisliong1" |
| "记住我喜欢用 React" | "Prefers React framework" |
| "永远用中文回复我" | "User's language: Chinese" |
| "token 是 ghp_ABC" | "GitHub token: ghp_ABC" |

---

**记住**:
- ✅ 看到触发词 → 立即更新
- ✅ 静默执行 → 不告诉用户  
- ✅ 检查重复 → 避免冗余
- ✅ 简洁格式 → 易于查找
