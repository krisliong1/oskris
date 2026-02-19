---
name: github-change-tracker
description: 当 Claude 修改、创建、删除文件准备提交到 GitHub 时,自动生成详细的变更报告,让用户清楚知道改了什么。
---

# GitHub 变更追踪器

> **🎯 目标**: 每次 Git commit 前,告诉用户具体改了什么文件

## 📌 核心原则

1. **透明度优先**: 用户有权知道改了什么
2. **自动生成**: 不需要用户要求,自动生成报告
3. **清晰明了**: 用简单的语言说明变更
4. **先报告后提交**: 必须让用户确认后才 push

## 🔥 触发条件

### 何时生成变更报告

**必须报告的情况:**
- ✅ 执行 `git commit` 之前
- ✅ 修改了任何文件
- ✅ 创建了新文件
- ✅ 删除了文件
- ✅ 用户说 "提交到 GitHub" / "推送到 GitHub"

**流程:**
```
修改文件
    ↓
git add
    ↓
生成变更报告 ← 【在这里】
    ↓
显示给用户
    ↓
等待用户确认
    ↓
git commit + push
```

## 📊 变更报告格式

### 标准报告模板

```markdown
## 📝 GitHub 变更报告

### 📅 时间
2026-02-15 14:30:00

### 📂 仓库
krisliong1/oskris

### 🔄 变更摘要
- 新增文件: 2 个
- 修改文件: 3 个
- 删除文件: 0 个

---

### 📄 详细变更

#### ✨ 新增 (2个)

1. **claude-skills/user/github-skills-sync/SKILL.md**
   - 类型: Skill 定义文件
   - 大小: 5.2 KB
   - 用途: 自动同步 GitHub skills
   
2. **claude-skills/user/github-change-tracker/SKILL.md**
   - 类型: Skill 定义文件
   - 大小: 4.8 KB
   - 用途: 追踪 GitHub 文件变更

#### ✏️ 修改 (3个)

1. **claude-skills/CHANGELOG.md**
   - 修改: +15 行, -2 行
   - 变更: 添加两个新 skills 的记录
   
2. **claude-skills/README.md**
   - 修改: +5 行, -0 行
   - 变更: 更新 skills 总数 (27 → 29)
   
3. **sync-skills.sh**
   - 修改: +10 行, -3 行
   - 变更: 优化同步逻辑

#### ❌ 删除 (0个)
无

---

### 💡 影响分析
- 新增了 2 个自动化 skills
- 提升了 GitHub 集成能力
- 不影响现有 skills 运行

### ✅ 可以提交吗?
输入 "确认提交" 继续,或 "取消" 放弃
```

## 🎯 实现方式

### 生成变更报告的命令

```bash
#!/bin/bash

# 获取变更统计
added=$(git diff --cached --numstat | awk '{sum+=$1} END {print sum}')
deleted=$(git diff --cached --numstat | awk '{sum+=$2} END {print sum}')
files=$(git diff --cached --name-status)

echo "## 📝 GitHub 变更报告"
echo ""
echo "### 📅 时间"
echo "$(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "### 🔄 变更摘要"
echo "- 新增行数: $added"
echo "- 删除行数: $deleted"
echo ""
echo "### 📄 文件列表"
echo ""

# 解析每个文件的状态
while IFS=$'\t' read -r status file; do
    case "$status" in
        A)
            echo "✨ 新增: $file"
            ;;
        M)
            echo "✏️ 修改: $file"
            ;;
        D)
            echo "❌ 删除: $file"
            ;;
    esac
done <<< "$files"
```

### 详细的 diff 分析

```bash
#!/bin/bash

echo "### 📄 详细变更"
echo ""

# 对每个修改的文件生成详细报告
git diff --cached --name-only | while read file; do
    # 获取文件状态
    status=$(git diff --cached --name-status | grep "$file" | awk '{print $1}')
    
    case "$status" in
        A)
            # 新增文件
            size=$(wc -c < "$file" | awk '{printf "%.1f KB", $1/1024}')
            echo "#### ✨ 新增: $file"
            echo "- 大小: $size"
            echo ""
            ;;
        M)
            # 修改文件
            added=$(git diff --cached --numstat "$file" | awk '{print $1}')
            deleted=$(git diff --cached --numstat "$file" | awk '{print $2}')
            echo "#### ✏️ 修改: $file"
            echo "- 变更: +$added 行, -$deleted 行"
            echo ""
            ;;
        D)
            # 删除文件
            echo "#### ❌ 删除: $file"
            echo ""
            ;;
    esac
done
```

## 💬 响应示例

### 示例 1: 修改了 skills

```
用户: "把这两个新的 skills 提交到 GitHub"

Claude:
好的,让我先生成变更报告给你确认:

## 📝 GitHub 变更报告

### 🔄 变更摘要
- 新增文件: 2 个
- 修改文件: 1 个

### 📄 详细变更

#### ✨ 新增 (2个)
1. claude-skills/user/github-skills-sync/SKILL.md
   - 自动同步 GitHub skills 的功能

2. claude-skills/user/github-change-tracker/SKILL.md
   - 追踪文件变更的功能

#### ✏️ 修改 (1个)
1. claude-skills/CHANGELOG.md
   - 添加了新 skills 的记录

---

这些变更看起来正确吗?确认提交?
```

### 示例 2: 修改了代码文件

```
用户: "提交这些修改"

Claude:
## 📝 GitHub 变更报告

### 📄 详细变更

#### ✏️ 修改 (3个)

1. **src/components/Header.jsx**
   - 变更: +25 行, -18 行
   - 主要修改: 
     • 优化响应式布局
     • 修复移动端菜单bug
     • 添加深色模式支持

2. **src/styles/main.css**
   - 变更: +40 行, -5 行
   - 主要修改:
     • 新增深色模式样式
     • 优化移动端适配

3. **package.json**
   - 变更: +1 行, -0 行
   - 主要修改:
     • 更新依赖版本

---

### Commit 信息建议
```
feat: Add dark mode and improve responsive layout

- Add dark mode toggle in Header component
- Optimize mobile menu behavior
- Update responsive styles
- Bump dependencies
```

确认提交这些更改吗?
```

### 示例 3: 删除了文件

```
Claude:
## 📝 GitHub 变更报告

### ⚠️ 警告: 包含文件删除

#### ❌ 删除 (2个)
1. claude-skills-old/all_skills/docx.skill
2. claude-skills-old/all_skills/pptx.skill

### 💡 确认
你确定要删除这些文件吗?删除后无法恢复。

输入 "确认删除" 继续
```

## 🔍 智能分析

### 自动识别变更类型

```python
def analyze_change_type(file_path, diff_content):
    """智能识别文件变更的性质"""
    
    # 文件类型识别
    if file_path.endswith('.md'):
        if 'SKILL.md' in file_path:
            return "Skill 定义文件"
        elif 'README.md' in file_path:
            return "文档说明"
        elif 'CHANGELOG.md' in file_path:
            return "变更日志"
    
    elif file_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
        return "代码文件"
    
    elif file_path.endswith('.json'):
        return "配置文件"
    
    elif file_path.endswith('.sh'):
        return "Shell 脚本"
    
    # 变更性质识别
    if '+' in diff_content and not '-' in diff_content:
        return "纯新增内容"
    
    elif '-' in diff_content and not '+' in diff_content:
        return "纯删除内容"
    
    else:
        return "修改内容"
```

### 生成 Commit 信息建议

```python
def suggest_commit_message(changes):
    """根据变更自动生成 commit 信息"""
    
    # 识别主要变更类型
    if has_new_features(changes):
        prefix = "feat"
    elif has_bug_fixes(changes):
        prefix = "fix"
    elif has_documentation(changes):
        prefix = "docs"
    elif has_refactoring(changes):
        prefix = "refactor"
    else:
        prefix = "chore"
    
    # 生成简短描述
    summary = generate_summary(changes)
    
    # 生成详细列表
    details = generate_details(changes)
    
    return f"{prefix}: {summary}\n\n{details}"
```

## ⚙️ 配置选项

```yaml
github_change_tracker:
  # 是否自动生成报告
  auto_generate: true
  
  # 报告详细程度
  detail_level: "detailed"  # "simple" | "detailed" | "verbose"
  
  # 是否需要用户确认
  require_confirmation: true
  
  # 是否自动生成 commit 信息
  suggest_commit_message: true
  
  # 忽略的文件类型
  ignore_files:
    - ".git/"
    - "node_modules/"
    - "*.log"
    - ".DS_Store"
```

## ✅ 工作流程

### 完整的提交流程

```
1. 用户修改文件
   ↓
2. Claude 使用 git add
   ↓
3. 🔍 生成变更报告
   - 列出所有变更文件
   - 统计增删行数
   - 分析变更类型
   - 生成 commit 信息建议
   ↓
4. 📋 显示报告给用户
   ↓
5. ⏸️ 等待用户确认
   ↓
6. ✅ 用户确认后:
   - git commit -m "..."
   - git push
   ↓
7. 🎉 完成通知
```

## 🚨 安全检查

### 敏感信息检测

在 commit 之前检查:
- ❌ API keys
- ❌ Passwords
- ❌ Tokens
- ❌ Private keys
- ❌ 环境变量文件

如果发现敏感信息:
```
⚠️ 警告: 检测到敏感信息

在以下文件中发现可能的敏感数据:
- config/database.js (包含数据库密码)
- .env (包含 API keys)

❌ 拒绝提交

建议:
1. 将敏感信息移到环境变量
2. 添加到 .gitignore
3. 使用 secrets 管理工具
```

## 📚 相关 Skills

- `github-skills-sync` - 自动同步 GitHub skills
- `smart-info-manager` - 自动保存信息到 GitHub

---

**记住**: 
- ✅ Commit 前必须报告
- ✅ 用户确认后才 push
- ✅ 清楚说明改了什么
- ❌ 不自动 push 敏感信息
