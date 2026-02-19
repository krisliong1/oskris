# Anthropic Skills Guide 学习报告

**日期**: 2026-02-19
**来源**: The Complete Guide to Building Skills for Claude (Anthropic, 2026-01-29)

## 核心知识点

### 1. Skill三层架构 (Progressive Disclosure)
- **第一层**: YAML frontmatter → 始终加载在system prompt中 (~50-100 tokens)
- **第二层**: SKILL.md正文 → 当Claude判断相关时加载 (~5000 tokens)
- **第三层**: scripts/references/ → 按需导航发现

### 2. YAML Frontmatter最佳实践
- `name`: 必须kebab-case，匹配文件夹名
- `description`: 必须包含"做什么"+"什么时候用"，≤1024字符
- 禁止XML角括号 `<>`
- 禁止用"claude"或"anthropic"开头命名

### 3. 三大用例类型
1. **Document & Asset Creation** — 创建一致的高质量输出
2. **Workflow Automation** — 多步骤流程自动化
3. **MCP Enhancement** — 增强MCP工具的工作流知识层

### 4. Skills vs Agents
- **Skills**: 单一专业任务，可被多个Agent复用
- **Agents**: 协调多个Skills完成复杂流程（如sales-agent协调proposal+onboarding+email）

### 5. 设计模式 (5种)
1. Sequential Workflow — 按顺序执行多步骤
2. Multi-MCP Coordination — 跨多个服务协调
3. Iterative Refinement — 循环改进直到达标
4. Context-aware Selection — 根据上下文选择工具
5. Domain Intelligence — 嵌入专业领域知识

### 6. 测试方法
- Triggering tests: 确保正确触发/不误触发
- Functional tests: 验证输出正确性
- Performance comparison: 有skill vs 无skill对比

### 7. 社区生态现状 (2026-02)
- Anthropic官方skills仓库: 70.9k stars
- 社区awesome-claude-skills多个集合
- Skill安全风险: ToxicSkills研究发现恶意skills
- LobeHub等平台提供skill发现和安装

## 应用：创建了12个新Skills/Agents

### 已创建并推送GitHub:
1. client-proposal-generator — 报价单生成
2. client-onboarding — 客户入职流程
3. project-tracker — 项目进度追踪
4. social-media-content — 社媒内容
5. seo-optimizer — SEO优化
6. portfolio-builder — 作品集
7. vps-manager — VPS管理
8. site-deployer — 网站部署
9. email-templates — 邮件模板
10. delivery-calculator — KKH运费
11. sales-agent — 销售流程Agent
12. site-health-agent — 网站健康Agent

## 下一步行动
- 在claude.ai Project中上传新skills
- 在实际业务中测试trigger准确性
- 迭代优化description以提高触发率
- 考虑为高频skills添加scripts/目录

---
*学习来源: Anthropic官方32页PDF + 社区生态调研*
