# 安装指南 - Smart Info Manager

## 🚀 5 分钟快速安装

### 第 1 步: 准备 GitHub 仓库

```bash
# 1. 在 GitHub 创建仓库 'oskris'
# 访问: https://github.com/new
# 仓库名: oskris
# 设置为 Private (推荐)

# 2. 克隆到本地
git clone https://github.com/krisliong1/oskris.git
cd oskris

# 3. 创建基本目录结构
mkdir -p memories/{personal,preferences,conversations}
mkdir -p tasks/{urgent,important,normal}
mkdir -p notes/{tech,work,learning}
mkdir -p projects
mkdir -p archive
mkdir -p index

# 4. 创建 README
cat > README.md << 'EOF'
# My Second Brain - oskris

智能信息管理系统,自动保存所有重要对话、任务、笔记。

## 目录结构

- `memories/` - 个人记忆和偏好
- `tasks/` - 任务管理(按优先级)
- `notes/` - 学习笔记和工作记录
- `projects/` - 项目文档
- `archive/` - 时间归档
- `index/` - 搜索索引

---

*由 Smart Info Manager 自动管理*
EOF

# 5. 初始化索引文件
echo '{}' > index/keywords.json
echo '{}' > index/tech-keywords.json
echo '{}' > index/timeline.json

# 6. 提交初始结构
git add .
git commit -m "Initialize Smart Info Manager"
git push origin main
```

### 第 2 步: 设置 GitHub Token

```bash
# 1. 创建 Personal Access Token
# 访问: https://github.com/settings/tokens/new
# 
# 设置:
# - Note: Smart Info Manager
# - Expiration: No expiration (或自定义)
# - Scopes: ✓ repo (完整权限)
#
# 点击 Generate token,复制 token

# 2. 设置环境变量 (临时)
export GITHUB_TOKEN="ghp_your_token_here"

# 3. 或永久保存 (推荐)
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.bashrc
source ~/.bashrc

# 4. 验证 token
echo $GITHUB_TOKEN
```

### 第 3 步: 安装 Skill 到 Claude

有两种方式:

#### 方式 A: 直接复制 (推荐)

```bash
# 1. 下载 smart-info-manager 文件夹
# (从上面的下载链接)

# 2. 上传到 Claude
# - 在 Claude.ai 对话中上传整个文件夹
# - 或将文件放到 /mnt/skills/user/smart-info-manager/
```

#### 方式 B: 手动创建

```bash
# 1. 创建 skill 目录
mkdir -p /mnt/skills/user/smart-info-manager/{scripts,evals,examples}

# 2. 复制文件
# - SKILL.md
# - config.yaml
# - scripts/auto-save.sh
# - scripts/keyword_extractor.py
# - scripts/github_manager.py
# - evals/evals.json

# 3. 给脚本执行权限
chmod +x /mnt/skills/user/smart-info-manager/scripts/auto-save.sh
```

### 第 4 步: 测试

在 Claude 对话中测试:

```
你: "记住明天要完成 React 项目首页,很紧急!"

Claude 应该自动:
✓ 识别关键词和优先级
✓ 保存到 GitHub
✓ 返回保存位置和链接
```

## 🔍 验证安装

### 检查 GitHub Token

```bash
# 确认 token 已设置
echo $GITHUB_TOKEN

# 测试 GitHub 连接
git clone https://${GITHUB_TOKEN}@github.com/krisliong1/oskris.git /tmp/test-oskris
```

### 测试保存脚本

```bash
# 进入 skill 目录
cd /mnt/skills/user/smart-info-manager

# 运行测试
bash scripts/auto-save.sh \
  "测试保存功能 - 学习 Python" \
  "learning" \
  "normal" \
  "Python"

# 检查输出
# 应该看到:
# ✓ 文件已创建
# ✅ 保存成功!
# 📍 GitHub 链接: https://github.com/...
```

### 在 GitHub 查看结果

```bash
# 访问你的仓库
# https://github.com/krisliong1/oskris

# 应该看到:
# - notes/learning/2024-02-15-note.md (新文件)
# - 最新的 commit: "Auto-save: learning - ..."
```

## ⚙️ 配置选项

### 自定义分类

编辑 `config.yaml`:

```yaml
categories:
  custom:
    - name: "fitness"
      keywords: ["健身", "运动", "跑步", "瑜伽"]
    - name: "finance"
      keywords: ["投资", "理财", "股票", "基金"]
```

### 添加技术关键词

```yaml
tech_keywords:
  languages:
    - Kotlin
    - Swift
    - Scala
  frameworks:
    - Flutter
    - SwiftUI
    - Gin
```

### 优先级规则

```yaml
priority_detection:
  urgent_keywords:
    - "ASAP"
    - "立刻"
    - "火速"
  important_keywords:
    - "关键"
    - "核心"
    - "crucial"
```

## 🐛 故障排除

### 问题 1: GitHub 推送失败

```bash
# 检查 token 权限
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user

# 重新生成 token
# https://github.com/settings/tokens
```

### 问题 2: 文件未创建

```bash
# 检查目录权限
ls -la /tmp/oskris

# 手动创建目录
cd /tmp/oskris
mkdir -p tasks/urgent
```

### 问题 3: Git 配置错误

```bash
# 设置 Git 用户
cd /tmp/oskris
git config user.email "your@email.com"
git config user.name "Your Name"
```

### 问题 4: 脚本无执行权限

```bash
# 添加执行权限
chmod +x /mnt/skills/user/smart-info-manager/scripts/auto-save.sh

# 验证
ls -la /mnt/skills/user/smart-info-manager/scripts/
```

## 📊 使用统计

安装完成后,你可以:

```bash
# 查看所有保存的任务
ls /tmp/oskris/tasks/*/*.md

# 统计文件数量
find /tmp/oskris -name "*.md" | wc -l

# 查看最近的保存
cd /tmp/oskris
git log --oneline -10

# 搜索关键词
grep -r "React" /tmp/oskris
```

## 🎉 完成!

你现在可以:

1. ✅ 在对话中说"记住..."自动保存
2. ✅ 所有信息自动分类到 GitHub
3. ✅ 随时查看和搜索历史记录
4. ✅ 数据安全存储在你的 GitHub

## 下一步

- 📖 阅读 [QUICKSTART.md](QUICKSTART.md) 了解更多用法
- 🔧 查看 [SKILL.md](SKILL.md) 了解技术细节  
- 💡 运行 `examples/demo.py` 查看完整演示

---

**问题反馈**: 如遇到问题,请检查:
1. GitHub token 是否正确设置
2. 仓库权限是否足够
3. 脚本是否有执行权限
4. Git 用户配置是否正确

**需要帮助?** 查看 README.md 或提交 GitHub Issue
