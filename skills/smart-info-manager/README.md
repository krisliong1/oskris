# Smart Info Manager - 使用指南

智能信息管理系统,自动提取、分类并存储对话中的重要信息到 GitHub。

## 快速开始

### 1. 安装依赖

```bash
pip install pyyaml gitpython
```

### 2. 配置 GitHub Token

创建 GitHub Personal Access Token:
1. 访问 https://github.com/settings/tokens
2. 生成新 token(repo 权限)
3. 设置环境变量:

```bash
export GITHUB_TOKEN="your_token_here"
```

### 3. 初始化仓库

```bash
# 克隆或创建 oskris 仓库
git clone https://github.com/krisliong1/oskris.git

# 或创建新仓库
mkdir oskris && cd oskris
git init
git remote add origin https://github.com/krisliong1/oskris.git
```

## 使用方式

### 方式一:对话触发

在对话中使用触发词:

```
用户: "记住明天要完成网站首页,这个很紧急"
系统: ✓ 已保存到 tasks/urgent/20240115-143022-task.md
```

**触发词列表**:
- "记住这个"
- "保存到 oskris"
- "添加任务"
- "这个很重要"
- "存到 GitHub"

### 方式二:显式命令

```python
from scripts.keyword_extractor import KeywordExtractor
from scripts.github_manager import GitHubManager

# 提取信息
extractor = KeywordExtractor()
info = extractor.extract("明天要完成 React 项目")

# 保存到 GitHub
manager = GitHubManager()
result = manager.process_and_save("明天要完成 React 项目", info)

print(result["github_url"])
```

### 方式三:批量处理

```python
texts = [
    "学习 Python Django 框架",
    "开会讨论新功能",
    "记住我喜欢喝咖啡"
]

for text in texts:
    info = extractor.extract(text)
    manager.process_and_save(text, info)
```

## 功能详解

### 1. 自动关键词识别

系统会自动识别:

**实体类型**:
- 人名: 张三、李四
- 公司: 阿里巴巴、腾讯
- 地点: 北京、上海
- 产品: iPhone、ChatGPT

**技术关键词**:
- 语言: Python, JavaScript, Go
- 框架: React, Django, Vue
- 工具: Git, Docker, VS Code
- 数据库: MySQL, MongoDB

**时间信息**:
- 相对时间: 明天、下周、下个月
- 绝对时间: 2024-01-15、1月15日

**任务识别**:
- "要完成..."
- "需要做..."
- "TODO: ..."

### 2. 智能分类

**按优先级**:
- **urgent**: 紧急、asap、立即、马上
- **important**: 重要、关键、必须
- **normal**: 其他

**按主题**:
- **work**: 工作、项目、会议、任务
- **life**: 生活、家庭、健康
- **learning**: 学习、笔记、课程

**按时间**:
- 自动按日期归档: `archive/2024/01/15/`

### 3. 文件结构

保存的文件会自动生成 Markdown 格式:

```markdown
---
{
  "date": "2024-01-15T14:30:22",
  "category": "work",
  "priority": "urgent",
  "tags": ["网站", "React", "首页"],
  "tech_keywords": ["React"],
  "sentiment": "neutral"
}
---

# Work - 2024-01-15

## 内容
明天要完成网站的 React 首页设计,这个很紧急!

## 任务清单
- [ ] 完成网站的 React 首页设计

## 技术栈
**Frameworks**: React

## 时间信息
- 明天 (relative)
```

### 4. 索引系统

系统会自动维护三个索引文件:

#### keywords.json
```json
{
  "React": {
    "count": 15,
    "files": [
      "tasks/urgent/20240115-task.md",
      "notes/tech/20240115-react.md"
    ],
    "last_updated": "2024-01-15T14:30:22"
  }
}
```

#### tech-keywords.json
技术关键词专用索引,按技术类别分类。

#### timeline.json
```json
{
  "2024-01-15": {
    "tasks": 3,
    "notes": 5,
    "memories": 2,
    "files": [...]
  }
}
```

## 高级用法

### 自定义分类

编辑 `config.yaml`:

```yaml
categories:
  custom:
    - name: "fitness"
      keywords: ["健身", "运动", "锻炼"]
```

### 扩展技术关键词库

```yaml
tech_keywords:
  languages:
    - Kotlin
    - Swift
  frameworks:
    - Flutter
    - SwiftUI
```

### 设置优先级规则

```yaml
priority_detection:
  urgent_keywords:
    - "急"
    - "emergency"
  important_keywords:
    - "核心"
    - "critical"
```

## 查看和搜索

### 查看最近保存

```bash
cd oskris
git log --oneline -10
```

### 搜索关键词

```bash
# 搜索所有包含 "React" 的文件
grep -r "React" .

# 查看某个日期的所有记录
ls archive/2024/01/15/
```

### 使用索引查询

```python
import json

# 读取关键词索引
with open('index/keywords.json', 'r') as f:
    keywords = json.load(f)

# 查找 React 相关文件
react_files = keywords.get('React', {}).get('files', [])
print(react_files)
```

## 故障排除

### GitHub 推送失败

```bash
# 检查 token 权限
echo $GITHUB_TOKEN

# 手动推送测试
cd /tmp/oskris
git push origin main
```

### 关键词识别不准确

1. 编辑 `config.yaml` 添加自定义关键词
2. 调整停用词列表
3. 增加技术关键词库

### 文件重复

系统使用时间戳命名,不会重复。如需合并:

```bash
# 查找重复内容
fdupes -r oskris/
```

## 最佳实践

### 1. 定期备份

```bash
# 克隆完整仓库作为备份
git clone https://github.com/krisliong1/oskris.git backup/
```

### 2. 清理旧文件

```bash
# 归档 3 个月前的文件
find archive/ -mtime +90 -exec gzip {} \;
```

### 3. 优化索引

```bash
# 定期重建索引
python scripts/rebuild_index.py
```

### 4. 数据分析

```python
# 统计你最常用的技术
with open('index/tech-keywords.json') as f:
    tech = json.load(f)
    
sorted_tech = sorted(tech.items(), key=lambda x: x[1]['count'], reverse=True)
print("Top 10 技术:")
for keyword, data in sorted_tech[:10]:
    print(f"{keyword}: {data['count']} 次")
```

## 隐私和安全

### 敏感信息保护

系统会自动检测以下敏感信息:
- API keys
- Passwords
- Tokens
- 个人身份信息

遇到敏感信息时会:
1. 提示用户确认
2. 可选择不保存
3. 或加密保存(需配置)

### 访问控制

建议设置 GitHub 仓库为 Private:
```bash
# 在 GitHub 网站上设置仓库为 Private
Settings -> General -> Danger Zone -> Change visibility
```

## 贡献指南

欢迎贡献代码和改进建议!

1. Fork 仓库
2. 创建功能分支
3. 提交 Pull Request

## 许可证

MIT License

## 支持

遇到问题?
- 查看文档: `SKILL.md`
- 提交 Issue: GitHub Issues
- 联系作者: [你的邮箱]

---

**记住**: 这个系统是你的第二大脑,让它帮你记录、整理、检索所有重要信息! 🧠✨
