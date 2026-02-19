# Oskris Skills 同步清单

> 最后更新: 2026-02-19

---

## 📍 两个仓库分工

| 仓库 | 用途 | Claude行为 |
|------|------|-----------|
| `krisliong1/oskris` | 🟢 活跃工作区 | 正常读写、触发skill |
| `krisliong1/backup` | 🔒 存放/备份 | **不触发**，用户要求时才搜索 |

## 📍 三个读取位置

| 位置 | Claude自动读取？ | 说明 |
|------|-----------------|------|
| `/mnt/skills/user/` (22个) | ✅ 自动触发 | claude.ai对话时根据触发词读取 |
| Project Knowledge | ✅ 每次都在context | 当前Project的参考文件 |
| GitHub `krisliong1/oskris` | ⚡ 被指令要求搜索 | 活跃skills + 项目文件 |
| GitHub `krisliong1/backup` | 🔒 不主动搜索 | 纯存放，找历史版本时才去 |

---

## 🟢 活跃Skills (claude.ai /mnt/skills/user/) — 22个

这些是Claude真正会自动触发的：

| # | Skill Name | 分类 | GitHub路径 |
|---|------------|------|-----------|
| 1 | app-recommendations | 知识 | knowledge/app-recommendations/ |
| 2 | auto-translate | 内容 | content/auto-translate/ |
| 3 | client-onboarding | 业务 | business-workflow/client-onboarding/ |
| 4 | client-proposal-generator | 业务 | business-workflow/client-proposal-generator/ |
| 5 | core-work-rules | 核心 | ai-automation/core-work-rules/ |
| 6 | delivery-calculator | 业务 | business-workflow/delivery-calculator/ |
| 7 | design-consultant | 网站 | web-development/design-consultant/ |
| 8 | email-templates | 生产力 | productivity/email-templates/ |
| 9 | frontend-builder | 网站 | web-development/frontend-builder/ |
| 10 | frontend-design | 网站 | web-development/frontend-design/ |
| 11 | portfolio-builder | 营销 | marketing/portfolio-builder/ |
| 12 | product-self-knowledge | 知识 | knowledge/product-self-knowledge/ |
| 13 | project-tracker | 业务 | business-workflow/project-tracker/ |
| 14 | project-workflow | 网站 | web-development/project-workflow/ |
| 15 | sales-agent | Agent | agents/sales-agent/ |
| 16 | seo-optimizer | 营销 | marketing/seo-optimizer/ |
| 17 | site-deployer | 运维 | devops/site-deployer/ |
| 18 | site-health-agent | Agent | agents/site-health-agent/ |
| 19 | smart-info-manager | 内容 | content/smart-info-manager/ |
| 20 | social-media-content | 营销 | marketing/social-media-content/ |
| 21 | vps-manager | 运维 | devops/vps-manager/ |
| 22 | work-rules | 核心 | core/work-rules/ |

## 📄 Project Knowledge文件 — 当前3个

| 文件名 | 内容 | 建议改名 |
|--------|------|---------|
| `SKILL.md` | sales-agent | `skill-sales-agent.md` |
| `learning-SKILL.md` | learning | `skill-learning.md` |
| `web-design-studio-SKILL.md` | web-design-studio | `skill-web-design-studio.md` |

## 🔒 仅在GitHub存放 — 43个

这些在 `krisliong1/oskris/skills/` 有，但没部署到claude.ai。
完整备份在 `krisliong1/backup/` 带时间戳。

<details>
<summary>点击展开完整列表</summary>

| Skill Name | GitHub路径 | 备注 |
|------------|-----------|------|
| conversation-context-keeper | agents/ | 存放 |
| github-auto-auth | agents/ | 存放 |
| github-change-tracker | agents/ | 存放 |
| github-skills-sync | agents/ | 存放 |
| memory-auto-updater | agents/ | 存放 |
| skill-auto-sync | agents/ | 存放 |
| auto-storage | core/ | 已整合到规则 |
| brand-guidelines | core/ | Anthropic品牌参考 |
| context-keeper | core/ | 存放 |
| conversation-starter | core/ | 存放 |
| conversation-startup | core/ | 存放 |
| github-ops | core/ | 存放 |
| memory-updater | core/ | 存放 |
| oskris-brand-guidelines | core/ | Oskris品牌 |
| design-enhancement | web-development/ | 存放 |
| requirements-analyst | web-development/ | 存放 |
| web-artifacts-builder | web-development/ | 存放 |
| benepass-reimbursement | business-workflow/ | 参考模板 |
| doc-coauthoring | business-workflow/ | 存放 |
| internal-comms | business-workflow/ | 存放 |
| oskris-invoice-manager | business-workflow/ | 存放 |
| algorithmic-art | design-creative/ | 存放 |
| canvas-design | design-creative/ | 存放 |
| oskris-gif-creator | design-creative/ | 存放 |
| slack-gif-creator | design-creative/ | 参考模板 |
| theme-factory | design-creative/ | 存放 |
| mcp-builder | development-tools/ | 存放 |
| skill-creator | development-tools/ | 存放 |
| dns-adblock | dns-adblock/ | 按需 |
| ios-mobileconfig | ios-mobileconfig/ | 按需 |
| ios-shortcuts-builder | ios-shortcuts-builder/ | 按需 |
| ios-shortcuts-parser | ios-shortcuts-parser/ | 按需 |
| ios-shortcuts-studio | ios-shortcuts-studio/ | 按需 |
| ios-shortcuts | ios-shortcuts/ | 按需 |
| docx | documents/ | claude.ai内置 |
| pdf | documents/ | claude.ai内置 |
| pptx | documents/ | claude.ai内置 |
| xlsx | documents/ | claude.ai内置 |
| claude-code-mastery | user/ | 存放 |
| context-management | user/ | 存放 |
| context-monitor | user/ | 存放 |
| context-window-monitor | user/ | 存放 |
| professional-web-design | user/ | 存放 |
| prompt-engineering-enhanced | user/ | 存放 |
| learning | user/ | Project Knowledge有 |
| web-design-studio | web-design-studio/ | Project Knowledge有 |

</details>

---

## 📋 备份操作流程

### 每次修改时自动执行：
```
1. 修改/创建文件
2. → 推送到 krisliong1/oskris (活跃区)
3. → 推送到 krisliong1/backup/YYYY-MM-DD_HHMMSS/ (存放区)
4. → 告知用户完成
```

### 备份历史
| 时间戳 | 文件数 | 大小 | 说明 |
|--------|--------|------|------|
| 2026-02-19_145013 | 565 | 13MB | 第一次完整快照 |

