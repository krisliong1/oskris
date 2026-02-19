---
name: smart-info-manager
description: 自动识别对话中的关键信息、任务、记忆,并分类存储到GitHub仓库krisliong1/oskris。支持多维度分类(时间、主题、项目、优先级)和智能关键词提取。
---

# Smart Info Manager — 智能信息管理

自动识别对话中值得保存的信息，分类存储到GitHub。

## 核心原则

1. **主动识别** — 不等用户说"保存"，发现重要信息自动提议
2. **分类清晰** — 每条信息有明确的分类和标签
3. **安全优先** — 敏感信息绝不存GitHub
4. **去重** — 检查是否已存在类似内容

## 触发条件

**自动触发**:
- 用户做了重要决策（价格、技术选型、业务方向）
- 学到了新知识/技能
- 创建了新文件或配置
- 发现了问题和解决方案
- 用户表达了偏好设定

**用户主动触发**:
- "记住这个"、"保存"、"记下来"
- "这很重要"、"别忘了"

## GitHub存储结构

```
krisliong1/oskris/
├── notes/
│   ├── memory/
│   │   └── claude-memory.md      # 核心记忆文件
│   ├── tasks/
│   │   └── YYYY-MM-DD-task.md    # 任务清单
│   ├── decisions/
│   │   └── topic-decision.md     # 决策记录
│   └── references/
│       └── topic-ref.md          # 参考资料
├── learning-reports/
│   └── topic-learning.md         # 学习报告
├── learning-logs/
│   └── YYYY-MM-DD-topic.md       # 学习日志
└── skills/
    └── [category]/[name]/SKILL.md # Skills
```

## 自动分类系统

| 类型 | 存储位置 | 示例 |
|------|---------|------|
| 配置/凭据 | 记忆系统(不存GitHub) | API keys, 密码 |
| 决策 | notes/decisions/ | 技术选型, 价格决定 |
| 任务 | notes/tasks/ | 待办事项, 项目进度 |
| 学习 | learning-reports/ | 新技能, 研究结果 |
| 技能 | skills/[category]/ | 可复用的流程/知识 |
| 参考 | notes/references/ | 有用的链接, 教程 |

## 关键词识别

**技术关键词**: API, SSH, DNS, VPS, GitHub, npm, Docker, SSL, CDN
**业务关键词**: 客户, 报价, 项目, 定价, 合同, 发票
**决策关键词**: 决定, 选择, 确定, 改为, 不再用
**任务关键词**: 需要, 待办, 下一步, 记得, 别忘

## 执行流程

### Step 1: 识别信息类型
分析对话内容，判断是否值得保存，属于哪个分类。

### Step 2: 安全检查
**禁止存GitHub**: API keys, tokens, passwords, SSH私钥, 个人隐私
**可以存GitHub**: 技术笔记, 决策, 学习报告, 任务, 配置说明(不含密钥)

### Step 3: 存储到GitHub
```bash
cd /tmp && git clone [repo] && cd oskris
# 创建/更新文件
git add . && git commit -m "Add: [描述]" && git push
```

### Step 4: 更新记忆
如果涉及核心配置或偏好 → 同步更新 claude-memory.md

### Step 5: 通知用户
```
✅ 已保存到 GitHub:
- 新建: notes/decisions/pricing-update.md
- 更新: notes/memory/claude-memory.md
```

## 敏感信息安全规则

**最高优先级 — 任何情况下都不违反**:

| 信息类型 | 存储位置 | 示例 |
|---------|---------|------|
| API Keys/Tokens | Claude记忆 only | GitHub token, Hostinger API |
| 密码 | Claude记忆 only | VPS密码, 主机密码 |
| SSH私钥 | Claude记忆 only | ed25519私钥 |
| 技术配置(无密钥) | GitHub ✅ | 端口号, 域名, 文件路径 |
| 业务决策 | GitHub ✅ | 定价, 流程 |
| 学习笔记 | GitHub ✅ | 技术报告 |

## 故障处理

**GitHub连接失败**:
1. 重试一次
2. 仍失败 → 内容保存到对话中
3. 告诉用户: "GitHub暂时无法连接，请稍后在Desktop模式同步"
4. 提供完整内容让用户手动保存

**关键词提取不确定**:
- 不确定就问用户: "这个信息需要保存吗？"
- 宁可多存不漏存
