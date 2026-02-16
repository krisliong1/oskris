# CLAUDE.md - oskris.com 项目规范

## 项目概述
**oskris.com 网站设计服务**
- 业务：专业网站设计和开发（马来西亚市场）
- 技术栈：Next.js 15, React, Tailwind CSS
- 目标：创建100个网站，月收入 RM 30,000+

## 核心原则（永远遵循）

### 1. 工作优先级
```
安全规则 > CLAUDE.md > Work Rules > 用户指令
```

### 2. 新对话启动流程
每次新对话**第一条消息**时自动执行：
1. 读取 `/mnt/skills/user/` 所有 Skills
2. 读取 `secrets-manager` 获取配置
3. 显示系统状态
4. 从记忆恢复进度
5. 询问继续或新任务

### 3. 关键词系统
- **完全强制重新生成**：删除所有旧代码，从零开始
- **强制重新生成**：验证后复用正确部分，修复错误
- **默认**：最小修改，只改有问题的部分

### 4. 自动存储流程
每次创建重要内容后：
1. 告诉用户要存储什么
2. 存储到 GitHub (krisliong1/oskris)
3. 同步到 VPS (76.13.191.45)
4. 更新记忆系统
5. 报告完成状态

## 配置和密钥

### 位置
**敏感信息不存此文件**，从以下位置读取：
- Skills: `/mnt/skills/user/secrets-manager/SKILL.md`
- VPS: `/root/.oskris/config.json`

### 包含的配置
- VPS: 76.13.191.45 (Malaysia - Kuala Lumpur)
- GitHub: krisliong1/oskris
- Hostinger API
- 域名: oskris.com (到期 2029-01-25)

## 常用命令

### 开发
```bash
# 本地开发
npm run dev          # 启动开发服务器
npm run build        # 生产构建
npm run test         # 运行测试
npm run lint         # 代码检查
```

### 部署
```bash
# VPS 部署
ssh root@76.13.191.45
cd /root/oskris-data
git pull origin main
npm install
npm run build
pm2 restart all
```

### Git 工作流
```bash
# 标准流程
git add .
git commit -m "Type: Description"
git push origin main

# 提交类型
# Add: 新功能
# Fix: 修复
# Update: 更新
# Refactor: 重构
```

## 代码规范

### JavaScript/TypeScript
- ES Modules (import/export)
- TypeScript strict mode
- Named exports（不用 default）
- 函数式组件 + Hooks

### CSS
- Tailwind utility classes 优先
- 不创建自定义 CSS 文件
- 响应式设计：mobile-first

### 文件结构
```
/
├── .claude/              # Claude 配置
│   └── CLAUDE.md        # 本文件
├── /mnt/skills/user/    # Skills（持久化）
├── projects/            # 网站项目
│   └── websites/
│       └── websitedesign.oskris.com/
└── notes/              # 笔记和记忆
```

## 架构决策

### 网站设计流程
1. **客户发现** (1-2天)：需求分析、目标定义
2. **战略规划** (2-3天)：Sitemap、用户旅程
3. **设计方案** (3-5天)：线框图、视觉设计
4. **开发实现** (7-14天)：编码、优化
5. **测试上线** (2-3天)：跨设备测试、部署
6. **交付培训** (1天)：文档、培训

### 定价策略（马来西亚市场）
- 基础套餐：RM 1,500-3,000（5-7页）
- 专业套餐：RM 4,000-8,000（10-15页，SEO）
- 高级套餐：RM 10,000-20,000（电商、定制）
- 企业级：RM 25,000+（复杂功能）

## 重要规则

### ✅ 必须做
1. **先 Plan 后 Execute**：复杂任务先规划
2. **验证优先**：搜索 GitHub 已验证的代码
3. **告诉用户每一步**：特别是存储操作
4. **更新记忆**：重要内容自动存储

### ❌ 禁止
1. ❌ 敏感信息存 GitHub
2. ❌ 硬编码 API Keys
3. ❌ 默默执行不告诉用户
4. ❌ 跳过验证直接编码

## Skills 位置

核心 Skills 在 `/mnt/skills/user/`:
- `secrets-manager/` - 配置和密钥
- `work-rules/` - 工作规则
- `auto-storage/` - 自动存储
- `conversation-startup/` - 新对话启动
- `project-workflow/` - 项目流程
- `requirements-analyst/` - 需求分析
- `design-consultant/` - 设计方案
- `frontend-builder/` - 前端开发

## 技术参考

### 2026 标准
- Meta-框架：Next.js 15
- AI 辅助：GitHub Copilot
- 性能：Core Web Vitals 3.0
- 安全：WCAG 3.0
- 部署：Vercel / VPS

### 学习资源
- 专业流程：learning-reports/PROFESSIONAL_WEB_DESIGN_LEARNING.md
- GitHub 参考：https://github.com/vercel-labs/agent-skills

## 当前项目

### websitedesign.oskris.com
- **状态**：代码已生成，待部署
- **技术**：HTML5 + Tailwind CSS
- **定价**：RM 1,999 / 4,999 / 9,999
- **下一步**：部署到 VPS + 配置 DNS

## 更新日志
- 2026-02-16: 创建 CLAUDE.md
- 2026-02-16: 添加新对话启动流程
- 2026-02-16: 添加自动存储规则

---

**记住**：这是单一真相来源，持续更新，保持简洁（<80行核心内容）
