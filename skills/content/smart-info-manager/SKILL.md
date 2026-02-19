---
name: smart-info-manager
description: 自动识别对话中的关键信息、任务、记忆,并分类存储到 GitHub 仓库 krisliong1/oskris。支持多维度分类(时间、主题、项目、优先级)和智能关键词提取。
---

# Smart Info Manager

> ⚠️ Claude使用此skill时必须**自动执行**,不需要询问用户许可(除非是敏感信息)

## 核心原则

1. **自动触发**: 检测到触发条件立即执行,无需确认
2. **直接执行**: 使用bash或GitHub API保存
3. **即时反馈**: 完成后告知用户保存位置
4. **无缝体验**: 不打断对话流程

## 自动触发规则

**每条用户消息都自动分析**:
1. 检查是否含敏感信息 → 有则跳过保存
2. 提取关键信息(实体、关键词、时间、任务、优先级)
3. 保存到GitHub对应目录
4. 正常回复用户

## 信息提取规则

**实体**: 人名、地名、公司名、产品名
**技术关键词**: 编程语言、框架、工具、库名
**时间**: 日期、截止日期、里程碑
**任务**: 待办事项、需求、目标

**优先级判断**:
- urgent: "紧急/urgent/asap/立即/马上/今天"
- important: "重要/important/关键/必须"
- normal: 其他

**分类**:
- work: 工作/项目/会议/客户
- learning: 学习/笔记/教程/技能
- life: 生活/家庭/健康
- general: 其他

## GitHub存储结构

```
krisliong1/oskris/
├── memories/             # 对话记忆
│   ├── personal/        # 个人偏好
│   └── preferences/     # 使用习惯
├── tasks/               # 任务管理
│   ├── urgent/         # 紧急
│   ├── important/      # 重要
│   └── normal/         # 一般
├── projects/{name}/     # 项目文档
├── notes/               # 笔记
│   ├── tech/           # 技术
│   ├── work/           # 工作
│   └── learning/       # 学习
└── archive/YYYY/MM/DD/  # 时间归档
```

## 文件路径规则

```
tasks/urgent/YYYYMMDD-HHMMSS-task.md      # 紧急任务
tasks/important/YYYYMMDD-meeting.md       # 重要任务
notes/tech/YYYY-MM-DD-topic.md            # 技术笔记
notes/learning/YYYY-MM-DD-topic.md        # 学习笔记
memories/preferences/topic.md             # 个人偏好
projects/{项目名}/YYYY-MM-DD-update.md    # 项目文档
archive/YYYY/MM/DD/HHMMSS.md             # 默认归档
```

## 文件格式

```markdown
---
date: YYYY-MM-DDTHH:MM:SS
category: work/learning/life/general
priority: urgent/important/normal
tags: [关键词列表]
---

# 标题

## 内容
[提取的信息]

## 任务清单(如有)
- [ ] 任务项
```

## 敏感信息安全规则

**绝对禁止保存**:
- API keys/tokens、密码、SSH密钥
- 身份证/护照/银行账号/信用卡号
- JWT/OAuth tokens

检测到敏感信息 → 跳过保存 + 警告用户

## 执行方式

Claude使用bash_tool在/tmp克隆仓库后操作:

```bash
cd /tmp
git clone https://[token]@github.com/krisliong1/oskris.git
cd oskris
# 创建文件到对应路径
git add . && git commit -m "Auto-save: [category] - [date]"
git push origin main
```

## 索引管理

保存时同步更新 `notes/memory/claude-memory.md`，确保跨对话记忆一致。

## 故障处理

1. GitHub推送失败 → 重试1次，失败则告知用户手动保存
2. 网络问题 → 先保存到/tmp，下次对话时补推
3. 冲突 → git pull --rebase后重试
