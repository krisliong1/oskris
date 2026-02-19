---
name: skill-auto-sync
description: 每次创建或修改 skill 后自动同步到 GitHub。无需手动 commit 和 push,完全自动化。
---

# Skill Auto Sync

> **🎯 目标**: 创建/修改 skill 后自动推送到 GitHub

## 📌 核心原则

1. **自动检测**: skill 创建或修改后立即触发
2. **自动同步**: 无需用户要求,自动 commit + push
3. **智能命名**: 自动生成有意义的 commit 信息
4. **错误处理**: Push 失败时通知用户

## 🔥 触发条件

**何时自动同步:**
- ✅ 创建了新的 skill
- ✅ 修改了现有 skill
- ✅ 在 `/home/claude/oskris/skills/` 或 `claude/mnt/skills/user/` 有变更

## 🔄 工作流程

### 完整的自动同步流程

```bash
#!/bin/bash

# 1. 检测变更
cd ~/oskris
CHANGES=$(git status --porcelain | grep -E "skill|SKILL.md")

if [ -n "$CHANGES" ]; then
    # 2. 自动 add
    git add skills/ claude/mnt/skills/
    
    # 3. 生成 commit 信息
    NEW_SKILLS=$(git diff --cached --name-only | grep "SKILL.md" | wc -l)
    COMMIT_MSG="auto: Sync $NEW_SKILLS skill(s) to GitHub"
    
    # 4. Commit
    git commit -m "$COMMIT_MSG"
    
    # 5. Push (使用 memory 中的 token)
    TOKEN=$(get_from_memory "GitHub token")  # Read from Claude's memory
    git push https://${TOKEN}@github.com/krisliong1/oskris.git main
    
    echo "✅ Skills 已自动同步到 GitHub"
fi
```

## 💬 Commit 信息模板

### 自动生成的格式

```
# 新增 skill
feat: Add {skill-name} skill

# 修改 skill  
update: Modify {skill-name} skill

# 删除 skill
remove: Delete {skill-name} skill

# 批量更新
auto: Sync {count} skill(s) to GitHub
```

## 📝 同步清单

### 每次同步都检查:

- [ ] `skills/` 目录的变更
- [ ] `claude/mnt/skills/user/` 的变更
- [ ] VERSION.md 文件
- [ ] README.md 更新 (如果需要)

## ⚙️ 配置

### 从 Memory 读取配置

```python
# 1. GitHub Token
token = memory.get("GitHub token")

# 2. 仓库信息
repo = "krisliong1/oskris"
branch = "main"

# 3. 同步路径
sync_paths = [
    "skills/",
    "claude/mnt/skills/user/"
]
```

## 🚨 错误处理

### 常见错误及处理

**1. Push 失败 (网络问题)**
```bash
if ! git push ...; then
    echo "⚠️ GitHub 同步失败,请检查网络"
    echo "变更已保存在本地,稍后会自动重试"
fi
```

**2. Token 过期**
```bash
if [[ $ERROR == *"authentication"* ]]; then
    echo "❌ GitHub token 已过期,请更新"
fi
```

**3. 冲突**
```bash
if [[ $ERROR == *"conflict"* ]]; then
    git pull --rebase
    git push
fi
```

## 📊 使用示例

### 示例 1: 创建新 skill

```
用户: "创建一个 skill 叫做 test-skill"
Claude: [创建 skill]
       [自动执行]
       cd ~/oskris
       git add skills/test-skill/
       git commit -m "feat: Add test-skill"
       git push https://{token}@...
       ✅ 完成
```

### 示例 2: 修改现有 skill

```
用户: "修改 app-recommendations 的描述"
Claude: [修改文件]
       [自动执行]
       git add skills/agents/app-recommendations/
       git commit -m "update: Modify app-recommendations skill"  
       git push
       ✅ 完成
```

## ⚡ 性能优化

### 批量处理

如果同时修改多个 skills:
```bash
# 不要每个 skill 都 push 一次
# 而是收集所有变更,一次性 push

git add skills/
git commit -m "auto: Sync 5 skills to GitHub"
git push
```

## 🔐 安全

### Token 安全

- ✅ 从 memory 读取 token
- ✅ 不在日志中显示 token
- ✅ 使用 HTTPS 而不是 SSH
- ❌ 不在代码中硬编码 token

---

**记住**:
- ✅ 创建/修改 skill → 自动同步
- ✅ 无需用户确认 → 直接 push
- ✅ 失败时通知 → 不静默失败
- ✅ Token 从 memory → 永不过期
