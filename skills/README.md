# Oskris Skills & Agents Directory

> Last updated: 2026-02-19
> Total: 30 Skills + 2 Agents

## 📁 Directory Structure

### 🏢 business-workflow/ — 业务运营
| Skill | Description |
|-------|-------------|
| `client-proposal-generator` | 🆕 专业报价单/提案自动生成 |
| `client-onboarding` | 🆕 新客户入职流程自动化 |
| `project-tracker` | 🆕 项目进度追踪和状态报告 |
| `oskris-invoice-manager` | 发票管理和生成 |
| `delivery-calculator` | 🆕 KKH运输费计算器 |

### 📢 marketing/ — 营销获客
| Skill | Description |
|-------|-------------|
| `social-media-content` | 🆕 社交媒体内容生成(FB/IG/TikTok) |
| `seo-optimizer` | 🆕 SEO审计和优化指导 |
| `portfolio-builder` | 🆕 项目案例/作品集生成 |

### 🖥️ devops/ — 服务器运维
| Skill | Description |
|-------|-------------|
| `vps-manager` | 🆕 VPS服务器管理自动化 |
| `site-deployer` | 🆕 网站一键部署(DNS+SSL+上传) |

### 🤖 agents/ — 多技能协调器
| Agent | Orchestrates | Description |
|-------|-------------|-------------|
| `sales-agent` | 🆕 proposal + onboarding + email + tracker | 完整销售流程Agent |
| `site-health-agent` | 🆕 vps-manager + seo + deployer | 网站健康监控Agent |

### 📧 productivity/ — 效率工具
| Skill | Description |
|-------|-------------|
| `email-templates` | 🆕 专业客户邮件模板库 |

### 🌐 web-development/ — 网站开发
| Skill | Description |
|-------|-------------|
| `requirements-analyst` | 需求分析 |
| `design-consultant` | 设计方案 |
| `design-enhancement` | 设计增强 |
| `frontend-builder` | 前端开发 |
| `project-workflow` | 项目工作流 |

### 🎨 web-design-studio/ — 网站设计工作室
| Skill | Description |
|-------|-------------|
| `web-design-studio` | 5-Agent设计协调器 |

### 📝 content/ — 内容处理
| Skill | Description |
|-------|-------------|
| `auto-translate` | 自动翻译(EN↔CN) |
| `smart-info-manager` | 智能信息管理 |

### 🔧 core/ — 核心系统
| Skill | Description |
|-------|-------------|
| `work-rules` | 工作规则 |

### 📱 iOS/设备
| Skill | Description |
|-------|-------------|
| `ios-mobileconfig` | iOS配置描述文件制作 |
| `dns-adblock` | DNS广告屏蔽方案 |

### 📚 knowledge/ — 知识库
| Skill | Description |
|-------|-------------|
| `app-recommendations` | App推荐 |

### 👤 user/ — 用户专属
| Skill | Description |
|-------|-------------|
| `learning` | 持续学习引擎 |
| `professional-web-design` | 专业网站设计知识 |
| `prompt-engineering-enhanced` | 高级提示词工程 |
| `claude-code-mastery` | Claude Code精通 |

---

## 🆕 2026-02-19 更新

新增 **10个Skills + 2个Agents**：
- 业务运营: client-proposal-generator, client-onboarding, project-tracker, delivery-calculator
- 营销获客: social-media-content, seo-optimizer, portfolio-builder
- 服务器运维: vps-manager, site-deployer
- 效率工具: email-templates
- Agent: sales-agent, site-health-agent

## 架构理念

基于 [Anthropic Complete Guide to Building Skills](https://claude.com/blog/complete-guide-to-building-skills-for-claude):

1. **Progressive Disclosure** — YAML frontmatter只占50-100 tokens，完整指令按需加载
2. **Composability** — Skills可以组合使用，Agents协调多个Skills
3. **Portability** — 同一个Skill在claude.ai、Claude Code、API都能用
4. **Problem-First** — 从用户问题出发，不是从工具出发

## Skill vs Agent

| | Skill | Agent |
|---|-------|-------|
| 职责 | 单一专业任务 | 协调多个Skills完成复杂流程 |
| 例子 | seo-optimizer (只做SEO) | site-health-agent (协调SEO+性能+安全) |
| 触发 | 明确的任务关键词 | 更宽泛的业务场景 |
| 复杂度 | 低-中 | 中-高 |
