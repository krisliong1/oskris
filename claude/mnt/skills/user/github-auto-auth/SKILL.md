---
name: github-auto-auth
description: 自动从 memory 读取 GitHub token 并配置 Git,无需用户每次提供。每次需要 push 时自动使用保存的 token。
---

# GitHub Auto Auth

> **🎯 目标**: 永远不再要求用户提供 GitHub token

## 📌 核心原则

1. **从 memory 读取 token**: 用户已经保存过了
2. **自动配置**: 需要 push 时自动配置
3. **静默执行**: 不告诉用户在找 token
4. **永不遗忘**: 每次都检查 memory

## 🔑 Token 存储位置

**在 Claude 的 memory 中**:
- 关键词: "GitHub token"
- 格式: `ghp_...`
- 仓库: `krisliong1/oskris`

## 🔄 工作流程

### 每次需要 Git push 时:

```python
# 1. 从 memory 读取 token
token = memory.find("GitHub token")

# 2. 如果找到 → 自动使用
if token:
    git push https://{token}@github.com/krisliong1/oskris.git
else:
    # 3. 如果没找到 → 才询问用户
    ask_user_for_token()
```

## 📝 Memory 格式

**应该存储为**:
```
User's GitHub token: ghp_XXXXX... (actual token stored in memory)
Repo: krisliong1/oskris
```

## 🚀 使用示例

### 场景 1: 用户说 "推送到 GitHub"

```python
# ❌ 错误做法:
"请提供您的 GitHub token"

# ✅ 正确做法:
token = get_token_from_memory()
git_push_with_token(token)
```

### 场景 2: 需要 commit

```python
# 自动流程:
git add .
git commit -m "..."
token = get_token_from_memory()  # 从 memory 自动读取
git push https://{token}@github.com/...
```

## 🔍 查找 Token 的方法

### 方法 1: 检查 memory

```python
# Claude 的 memory 包含用户信息
# 搜索关键词: "GitHub", "token", "ghp_"
```

### 方法 2: 从对话历史

```python
# 如果 memory 里没有,搜索过去的对话
search_past_chats("GitHub token")
```

## ⚠️ 重要规则

### 永远不要:
- ❌ 每次都问用户要 token
- ❌ 说 "我没有你的 token"
- ❌ 说 "请再次提供 token"
- ❌ 忘记检查 memory

### 永远要:
- ✅ 先检查 memory
- ✅ 自动使用找到的 token
- ✅ 静默配置 Git
- ✅ 只在真的找不到时才问

## 🔧 实现代码

### Git Push 标准流程

```bash
#!/bin/bash

# 从 memory 获取 token
TOKEN="ghp_XXXXX..."  # This will be read from Claude's memory

# 配置 Git
cd /path/to/repo
git add .
git commit -m "$MESSAGE"

# Push (带 token)
git push https://${TOKEN}@github.com/krisliong1/oskris.git main
```

### 通用函数

```python
def get_github_token():
    """从 memory 获取 GitHub token"""
    # 检查 memory
    if "GitHub token" in memory:
        return memory["GitHub token"]
    
    # 如果没有,搜索对话历史
    past_token = search_conversations("ghp_")
    if past_token:
        return past_token
    
    # 真的找不到才返回 None
    return None

def git_push(repo_path, message):
    """自动 push 到 GitHub"""
    token = get_github_token()
    
    if not token:
        return "❌ 找不到 GitHub token,请提供"
    
    # 使用 token push
    cmd = f"git push https://{token}@github.com/krisliong1/oskris.git main"
    os.system(cmd)
    
    return "✅ 推送成功"
```

## 📋 检查清单

每次要 push 时,Claude 必须:

- [ ] 检查 memory 是否有 token
- [ ] 如果有 → 直接使用
- [ ] 如果没有 → 搜索对话历史
- [ ] 还是没有 → 才询问用户
- [ ] **永远不要**在有 token 的情况下还问用户

## 🎯 成功标准

**用户应该**:
- ✅ 只提供一次 token
- ✅ 以后永远不用再提供
- ✅ 每次 push 都自动成功

**Claude 应该**:
- ✅ 记住 token
- ✅ 自动使用
- ✅ 不重复询问

## 💾 Memory 示例

```
User Info:
- Name: krisliong1
- GitHub token: ghp_XXXXX... (stored securely in memory)
- Repo: krisliong1/oskris
```

## ⚡ 快速参考

**需要 push 时的完整命令**:
```bash
# Token will be read from memory automatically
git push https://{TOKEN_FROM_MEMORY}@github.com/krisliong1/oskris.git main
```

---

**记住**: 
- Token 在 memory 里
- 永远先检查 memory
- 不要再问用户了!
