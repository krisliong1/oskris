# 快速开始 - Smart Info Manager

## 立即开始使用

### 1️⃣ 准备工作(5分钟)

```bash
# 克隆你的 GitHub 仓库
git clone https://github.com/krisliong1/oskris.git
cd oskris

# 创建基本目录结构
mkdir -p memories/{personal,preferences,conversations}
mkdir -p tasks/{urgent,important,normal}
mkdir -p notes/{tech,work,learning}
mkdir -p projects
mkdir -p archive
mkdir -p index

# 初始化索引文件
echo "{}" > index/keywords.json
echo "{}" > index/tech-keywords.json
echo "{}" > index/timeline.json

# 提交初始结构
git add .
git commit -m "Initialize Smart Info Manager structure"
git push origin main
```

### 2️⃣ 设置 GitHub Token

```bash
# 访问 https://github.com/settings/tokens
# 创建新 token,授予 'repo' 权限
# 设置环境变量
export GITHUB_TOKEN="ghp_your_token_here"

# 或永久保存到 ~/.bashrc
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.bashrc
```

### 3️⃣ 测试运行

```bash
# 进入 skill 目录
cd smart-info-manager/scripts

# 测试关键词提取
python3 keyword_extractor.py

# 你应该看到类似输出:
# 测试文本: 明天要完成网站的 React 首页设计...
# {
#   "keywords": ["React", "Next.js"],
#   "priority": "urgent",
#   ...
# }
```

### 4️⃣ 开始使用

#### 方式 A: 在对话中使用

只需在对话中说:

```
你: "记住明天要完成 React 项目,很紧急!"
Claude: ✓ 已保存到 tasks/urgent/20240115-143022-task.md
       GitHub: https://github.com/krisliong1/oskris/blob/main/tasks/urgent/...
```

**触发词**:
- 记住...
- 保存到 oskris
- 添加任务...
- 这个很重要
- 存到 GitHub

#### 方式 B: 使用 Python 脚本

```python
from scripts.keyword_extractor import KeywordExtractor
from scripts.github_manager import GitHubManager

# 创建实例
extractor = KeywordExtractor()
manager = GitHubManager()

# 处理文本
text = "学习 Python Django,做了博客项目"
info = extractor.extract(text)
result = manager.process_and_save(text, info)

print(result['github_url'])
```

#### 方式 C: 命令行工具(即将推出)

```bash
oskris save "明天开会讨论新功能"
oskris search "React"
oskris list --date today
```

## 常见使用场景

### 📝 保存任务

```
你: "下周一要和张三开会,准备演示文稿,这个很重要"

自动处理:
✓ 识别人名: 张三
✓ 时间: 下周一
✓ 优先级: important
✓ 任务: 开会, 准备演示文稿
✓ 保存到: tasks/important/20240115-meeting.md
```

### 💻 保存技术笔记

```
你: "今天学了 React Hooks,用 useState 和 useEffect 很方便"

自动处理:
✓ 技术关键词: React, Hooks, useState, useEffect
✓ 分类: learning
✓ 保存到: notes/tech/20240115-react-hooks.md
✓ 更新技术索引
```

### 🧠 保存个人偏好

```
你: "我喜欢喝拿铁,工作时听轻音乐,用 VS Code 编程"

自动处理:
✓ 类型: 个人偏好
✓ 保存到: memories/preferences/lifestyle.md
✓ 记录: 饮品偏好, 工作习惯, 工具选择
```

### 📦 保存项目信息

```
你: "项目 Alpha 用 Go + MongoDB,部署在 AWS,团队5人"

自动处理:
✓ 项目名: Alpha
✓ 技术栈: Go, MongoDB, AWS
✓ 保存到: projects/Alpha/overview.md
```

## 查看和搜索

### 查看最近记录

```bash
cd oskris

# 查看今天的记录
ls archive/2024/01/15/

# 查看所有紧急任务
ls tasks/urgent/

# 查看学习笔记
ls notes/learning/
```

### 搜索关键词

```bash
# 搜索所有包含 "React" 的文件
grep -r "React" .

# 搜索技术关键词索引
cat index/tech-keywords.json | grep "React"

# 查看时间线
cat index/timeline.json | grep "2024-01-15"
```

### 使用 Git 查看历史

```bash
# 查看最近提交
git log --oneline -10

# 查看某个文件的历史
git log --follow tasks/urgent/20240115-task.md

# 查看某天的更改
git log --since="2024-01-15" --until="2024-01-16"
```

## 高级技巧

### 1. 批量导入

```python
# 从文件批量导入
with open('notes.txt', 'r') as f:
    for line in f:
        if line.strip():
            info = extractor.extract(line)
            manager.process_and_save(line, info)
```

### 2. 自定义分类

编辑 `config.yaml`:

```yaml
categories:
  custom:
    - name: "fitness"
      keywords: ["健身", "运动", "跑步"]
    - name: "finance"
      keywords: ["投资", "理财", "股票"]
```

### 3. 设置提醒

```bash
# 使用 cron 定期检查紧急任务
0 9 * * * cat ~/oskris/tasks/urgent/*.md | mail -s "今日紧急任务" your@email.com
```

### 4. 数据分析

```python
import json
from collections import Counter

# 统计最常用技术
with open('index/tech-keywords.json') as f:
    tech = json.load(f)

sorted_tech = sorted(tech.items(), key=lambda x: x[1]['count'], reverse=True)
print("Top 10 技术:")
for keyword, data in sorted_tech[:10]:
    print(f"{keyword}: {data['count']} 次")
```

## 故障排除

### ❌ GitHub 推送失败

```bash
# 检查 token
echo $GITHUB_TOKEN

# 测试连接
git push -v

# 如果 token 过期,重新生成
# https://github.com/settings/tokens
```

### ❌ 关键词识别不准

编辑 `config.yaml` 添加自定义关键词:

```yaml
tech_keywords:
  languages:
    - Kotlin  # 添加新语言
  frameworks:
    - Svelte  # 添加新框架
```

### ❌ 文件冲突

```bash
# 拉取最新更改
git pull origin main

# 如有冲突,手动解决
git status
git add .
git commit -m "Resolve conflicts"
git push
```

## 下一步

✅ **已完成**: Skill 创建完成,可以开始使用!

📚 **深入学习**:
- 阅读 `SKILL.md` 了解完整功能
- 查看 `README.md` 获取详细文档
- 运行 `examples/demo.py` 查看演示

🚀 **未来计划**:
- Web 界面
- 移动端 App
- AI 智能摘要
- 多仓库同步
- 语音输入

## 需要帮助?

- 📖 文档: `README.md`, `SKILL.md`
- 🐛 报告问题: GitHub Issues
- 💬 讨论: GitHub Discussions

---

**开始享受你的第二大脑吧! 🧠✨**
