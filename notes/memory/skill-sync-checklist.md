# Oskris Skills 同步清单

> 最后更新: 2026-02-19
> 三个存储位置对比 + 同步状态

---

## 📍 三个位置说明

| 位置 | 命名规则 | 用途 | 谁读取 |
|------|---------|------|--------|
| **GitHub** `skills/分类/名称/SKILL.md` | 标准文件夹结构 | 存档+Claude Code+VPS | Claude Code, 手动部署 |
| **claude.ai Skills** `/mnt/skills/user/名称/` | 文件夹名=name字段 | claude.ai对话触发 | claude.ai (本Project) |
| **Project Knowledge** `xxx.md` | 扁平文件，随便命名 | 当前Project对话参考 | claude.ai (仅本Project) |

---

## 🔄 完整同步状态 (65 Skills)

### ✅ 三处都有（最理想状态）— 3个

| Skill Name | GitHub路径 | claude.ai Skills | Project Knowledge |
|------------|-----------|-----------------|-------------------|
| sales-agent | `agents/sales-agent/` | ✅ | ✅ `SKILL.md` |
| web-design-studio | `web-design-studio/` | ❌ | ✅ `web-design-studio-SKILL.md` |
| learning | `user/learning/` | ❌ | ✅ `learning-SKILL.md` |

### ⚡ GitHub + claude.ai Skills（功能正常）— 20个

这些在claude.ai里能正常触发，GitHub有备份，只是Project Knowledge没放副本。

| Skill Name | GitHub路径 | 分类 |
|------------|-----------|------|
| app-recommendations | `knowledge/app-recommendations/` | 知识 |
| auto-translate | `content/auto-translate/` | 内容 |
| client-onboarding | `business-workflow/client-onboarding/` | 业务 |
| client-proposal-generator | `business-workflow/client-proposal-generator/` | 业务 |
| core-work-rules | `ai-automation/core-work-rules/` | 核心 |
| delivery-calculator | `business-workflow/delivery-calculator/` | 业务 |
| design-consultant | `web-development/design-consultant/` | 网站开发 |
| email-templates | `productivity/email-templates/` | 生产力 |
| frontend-builder | `web-development/frontend-builder/` | 网站开发 |
| frontend-design | `web-development/frontend-design/` | 网站开发 |
| portfolio-builder | `marketing/portfolio-builder/` | 营销 |
| product-self-knowledge | `knowledge/product-self-knowledge/` | 知识 |
| project-tracker | `business-workflow/project-tracker/` | 业务 |
| project-workflow | `web-development/project-workflow/` | 网站开发 |
| seo-optimizer | `marketing/seo-optimizer/` | 营销 |
| site-deployer | `devops/site-deployer/` | 运维 |
| site-health-agent | `agents/site-health-agent/` | Agent |
| smart-info-manager | `content/smart-info-manager/` | 内容 |
| social-media-content | `marketing/social-media-content/` | 营销 |
| vps-manager | `devops/vps-manager/` | 运维 |
| work-rules | `core/work-rules/` | 核心 |

### 📦 仅在GitHub（存档，未部署到claude.ai）— 42个

这些skill创建了但没有部署到claude.ai的 `/mnt/skills/user/`，不会被自动触发。

| Skill Name | GitHub路径 | 是否需要部署？ |
|------------|-----------|---------------|
| **Agents** | | |
| conversation-context-keeper | `agents/conversation-context-keeper/` | 🔸 可能重复 |
| github-auto-auth | `agents/github-auto-auth/` | ⚪ 低优先 |
| github-change-tracker | `agents/github-change-tracker/` | ⚪ 低优先 |
| github-skills-sync | `agents/github-skills-sync/` | 🔸 自动同步用 |
| memory-auto-updater | `agents/memory-auto-updater/` | 🔸 可能有用 |
| skill-auto-sync | `agents/skill-auto-sync/` | 🔸 自动同步用 |
| **Core** | | |
| auto-storage | `core/auto-storage/` | 🔸 已整合到规则 |
| brand-guidelines | `core/brand-guidelines/` | ⚪ Anthropic品牌 |
| context-keeper | `core/context-keeper/` | 🔸 可能重复 |
| conversation-starter | `core/conversation-starter/` | 🔸 可能重复 |
| conversation-startup | `core/conversation-startup/` | 🔸 可能重复 |
| github-ops | `core/github-ops/` | ⚪ 低优先 |
| memory-updater | `core/memory-updater/` | 🔸 可能有用 |
| oskris-brand-guidelines | `core/oskris-brand-guidelines/` | 🟢 需要部署 |
| **Web Development** | | |
| design-enhancement | `web-development/design-enhancement/` | ⚪ 低优先 |
| requirements-analyst | `web-development/requirements-analyst/` | 🟢 需要部署 |
| web-artifacts-builder | `web-development/web-artifacts-builder/` | ⚪ 低优先 |
| **Business** | | |
| benepass-reimbursement | `business-workflow/benepass-reimbursement/` | ❌ 不相关 |
| doc-coauthoring | `business-workflow/doc-coauthoring/` | ⚪ 低优先 |
| internal-comms | `business-workflow/internal-comms/` | ⚪ 低优先 |
| oskris-invoice-manager | `business-workflow/oskris-invoice-manager/` | 🟢 需要部署 |
| **Design & Creative** | | |
| algorithmic-art | `design-creative/algorithmic-art/` | ⚪ 低优先 |
| canvas-design | `design-creative/canvas-design/` | ⚪ 低优先 |
| oskris-gif-creator | `design-creative/oskris-gif-creator/` | ⚪ 低优先 |
| slack-gif-creator | `design-creative/slack-gif-creator/` | ❌ 不相关 |
| theme-factory | `design-creative/theme-factory/` | ⚪ 低优先 |
| **Dev Tools** | | |
| mcp-builder | `development-tools/mcp-builder/` | ⚪ 低优先 |
| skill-creator | `development-tools/skill-creator/` | ⚪ 低优先 |
| **iOS** | | |
| dns-adblock | `dns-adblock/` | ⚪ 按需 |
| ios-mobileconfig | `ios-mobileconfig/` | ⚪ 按需 |
| ios-shortcuts-builder | `ios-shortcuts-builder/` | ⚪ 按需 |
| ios-shortcuts-parser | `ios-shortcuts-parser/` | ⚪ 按需 |
| ios-shortcuts-studio | `ios-shortcuts-studio/` | ⚪ 按需 |
| ios-shortcuts | `ios-shortcuts/` | ⚪ 按需 |
| **Documents** | | |
| docx | `documents/docx/` | ⚪ claude.ai已内置 |
| pdf | `documents/pdf/` | ⚪ claude.ai已内置 |
| pptx | `documents/pptx/` | ⚪ claude.ai已内置 |
| xlsx | `documents/xlsx/` | ⚪ claude.ai已内置 |
| **User** | | |
| claude-code-mastery | `user/claude-code-mastery/` | ⚪ 低优先 |
| context-management | `user/context-management/` | 🔸 可能重复 |
| context-monitor | `user/context-monitor/` | 🔸 可能重复 |
| context-window-monitor | `user/context-window-monitor/` | 🔸 可能重复 |
| professional-web-design | `user/professional-web-design/` | 🟢 需要部署 |
| prompt-engineering-enhanced | `user/prompt-engineering-enhanced/` | ⚪ 低优先 |

---

## ⚠️ 发现的问题

### 1. 重复Skills（需要清理）
以下skills功能高度重复，应该合并：

| 功能 | 重复的Skills | 建议保留 |
|------|-------------|---------|
| 对话上下文管理 | context-keeper, conversation-context-keeper, context-management, context-monitor, context-window-monitor | **保留1个**，合并到 `context-monitor` |
| 对话启动 | conversation-starter, conversation-startup | **保留1个**，合并到 `conversation-startup` |
| 记忆更新 | memory-updater, memory-auto-updater | **保留1个**，合并到 `memory-auto-updater` |
| GitHub同步 | github-skills-sync, skill-auto-sync, github-ops | **保留1个**，合并到 `github-skills-sync` |

### 2. 不相关Skills（可删除）
- `benepass-reimbursement` — 这是别人的模板，不是Oskris的
- `slack-gif-creator` — Oskris不用Slack
- `brand-guidelines` — 这是Anthropic品牌，不是Oskris的

### 3. 文档类Skills不需要自定义
claude.ai已内置 `docx`, `pdf`, `pptx`, `xlsx` 在 `/mnt/skills/public/`，GitHub里的副本可以删除或标记为参考。

### 4. Project Knowledge里的文件命名
| 当前名称 | 内容 | 建议改名 |
|---------|------|---------|
| `SKILL.md` | sales-agent | `skill-sales-agent.md` |
| `learning-SKILL.md` | learning | `skill-learning.md` |
| `web-design-studio-SKILL.md` | web-design-studio | `skill-web-design-studio.md` |

---

## 🟢 建议优先部署到claude.ai的Skills

这些在GitHub有但claude.ai没部署，对业务最有价值：

1. **requirements-analyst** — 客户需求分析，web-design-studio需要
2. **oskris-brand-guidelines** — Oskris自己的品牌规范
3. **oskris-invoice-manager** — 发票管理
4. **professional-web-design** — 专业网站设计知识
5. **learning** — 学习引擎（Project Knowledge有但claude.ai Skills没有）
6. **web-design-studio** — 网站设计工作室（同上）

---

## 📋 同步操作指南

### 新建/更新Skill时的操作流程：
```
1. 创建/修改 SKILL.md 内容
2. → 上传 GitHub: skills/分类/名称/SKILL.md
3. → 告知用户去 claude.ai Settings → Skills 添加
     或在 Claude Code 中部署到 /mnt/skills/user/
4. → 如果是重要skill，考虑加到 Project Knowledge
     命名: skill-[name].md
5. → 更新此同步清单
```

### 定期同步检查（每月1次）：
```
1. 比对 GitHub skills/ 目录
2. 比对 /mnt/skills/user/ 目录
3. 比对 Project Knowledge 文件
4. 标记差异，执行同步
```
