---
name: learning
description: >-
  持续进化引擎：学习新领域→验证→创建skill/agent→存储→优化，完整闭环。
  当用户说"学习/研究/了解/搞清楚X"、进入不熟悉的领域、需要调研后再动手、
  要消化文章或教程、从零掌握某技术/行业时触发。也适用于用户分享文章要求
  消化吸收的场景。Claude在回答任何可能涉及时效性的问题前，都应先搜索验证。
  学习后自动创建skill存GitHub并更新记忆，确保知识不丢失。发现skill不能用
  必须立刻告诉用户并给替代方案。
---

# Learning Skill — 持续进化引擎

学习→验证→应用→创建skill/agent→存储→优化→再学习。

## ⚠️ 第一条规则：你的知识经常是错的

你有"自信偏差"——30%以上知识已过时，这是从实际对话中反复验证的事实。

具体案例见 references/past-mistakes.md（没有就创建）。

**规则：**
- 学任何东西前，先承认"我可能不知道最新情况"
- 用 web search 搜索验证（所有plan都有web search）
- 搜索结果和训练数据冲突时，以搜索结果为准
- 关于Claude自己的功能也必须搜索，不要凭记忆回答

**历史错误：**
- 假设"Free plan没有web search"设计了错误方案
- 用旧版本号给用户写代码
- 错误判断平台功能给出错误建议

## 多平台环境适配

根据当前平台自动调整行为：

| 平台 | 检测方式 | 存储行为 |
|------|---------|---------|
| **claude.ai** | 无MCP工具 | GitHub + 提醒用户去Desktop同步 |
| **Claude Desktop** | 有filesystem MCP | Mac本地 + GitHub 同时写入 |
| **Claude Code** | 终端环境 | 直接git操作 + Mac本地 |
| **OpenClaw** | openclaw环境 | 推krisliong1/openclaw + backup |

通用能力检测：
- web search → 所有plan都有，必须使用
- file creation → 有就生成文件，没有就在对话中提供完整内容
- computer use / bash → 有就自动存储，没有就告诉用户手动保存

## 学习工作流（5步）

### 第1步：承认不知道
不说"据我所知"然后输出旧数据。说"让我先搜索最新信息"。即使很确定也搜索验证。

### 第2步：搜索验证
搜3+权威来源，详见 references/search-strategy.md。
- 英文权威源优先，再补中文/马来西亚本地源
- 对比多个来源交叉验证
- 关注2025-2026的变化
- 马来西亚市场相关必须搜本地定价和法规
- **搜索后必须记录结果**，不能搜完就忘

### 第3步：消化提炼
- 区分"已知通用知识"和"真正新信息"
- 提炼关键知识点，不是复制粘贴
- 按 references/learning-report-template.md 格式产出报告
- 质量达到"专业级"，见 references/quality-standards.md

### 第4步：立刻应用
- 学了就干活，不是写报告就完事
- 值得创建新skill就创建（先搜索有没有类似方案，有就优化，没有才从零创建）
- 技术类先验证可行性（跑通再记录）
- 不给用户"学习建议"——你学完了直接帮用户做
- 创建的skill必须真正能用、能触发、能产出结果
- 如果发现skill不能用，立刻告诉用户并给替代方案

### 第5步：存储闭环（三仓库体系）
学完后立即执行：

**文件推送（遵循三仓库分工）：**
a) 学习报告 → `krisliong1/oskris`: learning-reports/[topic]-learning.md
b) 新skill → `krisliong1/oskris`: skills/[category]/[name]/SKILL.md
c) 学习日志 → `krisliong1/oskris`: learning-logs/[date]-[topic].md
d) 时间戳备份 → `krisliong1/backup`: YYYY-MM-DD_HHMMSS/（完整快照）
e) 含敏感信息 → `krisliong1/private-config`（禁止存公开库）

**同步操作：**
f) 关键结论 → 更新Claude记忆（memory edits）
g) 失败案例 → 更新 references/past-mistakes.md
h) 告诉用户：新建/更新了哪些文件、推到了哪个仓库

**文件双版本规则：**
含敏感信息的文件同时制作两版：
- 完整版 → Project Knowledge / 记忆 / private-config
- 干净版 → krisliong1/oskris（敏感信息替换成"见Project配置"）

**手动更新提醒：**
每次推送后检查并提醒用户：
- project-config.md 是否需要更新
- Project Instructions/Knowledge 是否需要同步
- /mnt/skills/user/ 是否需要部署新skill
- 记忆是否需要用户确认

## 文件保护规则

⚠️ 修改现有文件前必须：
1. 显示要改什么（diff预览）
2. 获用户确认
3. 自动备份到 backups/
4. 记录 logs/changelog.md
5. 执行修改

新文件可直接创建。绝不删文件，除非获用户确认。

## 什么值得存储和记忆

✅ 可复用的结论
✅ 已验证可行的技术方案
✅ 用户的偏好和决策
✅ 学习后学到的知识 → 必须变成skill存GitHub
✅ 实时性信息（搜索确认后的最新数据）
✅ 创新前搜索到的类似方案（调用→优化，不重复造轮子）

**禁止：**
❌ 搜索后的信息不做任何存储和记录
❌ 做了不能用的skill却不验证就交付
❌ 知道skill不能用也不告诉用户
❌ 敏感信息存到公开GitHub仓库

## 苏格拉底式教学法（教学生时）

如果是教学场景：
- 先了解学生水平和目标
- 生成3-7阶段学习路线图，标注"你在这里"
- 用提问引导思考，不直接灌输
- 自适应难度：答对加速，答错放慢
- 每阶段有练习验证理解
- 用学生熟悉的比喻解释抽象概念
- 学生完成后让他用自己的话复述验证

## 犯错后自动更新机制

当用户纠正错误时：
1. 承认错误，不找借口
2. 立刻用web search搜索确认正确信息
3. 更新 references/past-mistakes.md（不存在就创建）
4. 推送到GitHub
5. 检查是否需要更新skill或记忆
6. 确保下次遇到类似场景不再犯

## 与其他Skill的关系

- core-work-rules / work-rules → 遵循质量标准和文件保护规则
- smart-info-manager → 记忆更新的分类方式
- skill-creator (examples/) → 新skill创建的标准流程
- project-config.md → 三仓库体系和存储规则的权威来源

**最后更新**: 2026-02-20
**定位**: 持续进化引擎，不只是学习工具
