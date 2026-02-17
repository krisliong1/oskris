---
name: web-design-studio
description: Complete website design and creation agent system. Use when designing websites for clients, from discovery to launch. Coordinates 5 specialized agents - Discovery, Designer, Creator, Reviewer, Launcher - to deliver professional websites. Triggers on any web design project, client website request, or website creation task.
---

# Web Design Studio

A complete agent system for designing and creating professional websites for clients. Like skill-creator has 4 agents (executor, grader, comparator, analyzer), this skill has 5 specialized agents that work together to deliver client websites from concept to launch.

## Architecture Overview

The **coordinator** (this skill) manages the full website project lifecycle by delegating to specialized agents:

| Agent | Role | Reference |
|-------|------|-----------|
| **Discovery Agent** | 客户调研、需求分析、竞争对手研究 | `agents/discovery.md` |
| **Designer Agent** | 视觉设计、品牌系统、UI/UX决策 | `agents/designer.md` |
| **Creator Agent** | 代码实现、网站构建、功能开发 | `agents/creator.md` |
| **Reviewer Agent** | 质量检查、性能测试、SEO审计 | `agents/reviewer.md` |
| **Launcher Agent** | 部署上线、DNS配置、上线后监控 | `agents/launcher.md` |

## Building Blocks

Each agent has well-defined inputs and outputs that chain together:

| Building Block | Input | Output | Agent |
|---------------|-------|--------|-------|
| **Client Discovery** | client brief / conversation | requirements.md, competitor-analysis.md | `agents/discovery.md` |
| **Brand & Design** | requirements.md | brand-kit.md, wireframes, design-spec.md | `agents/designer.md` |
| **Site Creation** | design-spec.md + brand-kit.md | working website (HTML/CSS/JS or WordPress) | `agents/creator.md` |
| **Quality Review** | working website | review-report.md, fixes applied | `agents/reviewer.md` |
| **Deploy & Launch** | reviewed website | live site, launch-checklist.md | `agents/launcher.md` |

## Mode Workflows

| Mode | Purpose | Workflow |
|------|---------|----------|
| **Full Project** | 从零到上线的完整项目 | Discovery → Designer → Creator → Reviewer → Launcher |
| **Design Only** | 只做设计不做开发 | Discovery → Designer → 输出设计稿 |
| **Build Only** | 有设计稿直接开发 | Creator → Reviewer → Launcher |
| **Redesign** | 现有网站改版 | Discovery(审计现有站) → Designer → Creator → Reviewer → Launcher |
| **Quick Site** | 快速建站(模板) | Discovery(简化) → Creator(模板) → Reviewer(快速) → Launcher |

## Coordinator Responsibilities

1. **判断项目阶段** — 用户可能在任何阶段进入，先确定从哪开始
2. **按顺序调度Agent** — 每个Agent的输出是下一个的输入
3. **管理客户沟通** — 在关键节点获取客户确认
4. **追踪项目进度** — 记录已完成和待完成的步骤
5. **质量把关** — 确保每个阶段的输出达到专业级
6. **处理变更** — 客户改需求时评估影响并调整

## Project Lifecycle

```
客户联系 → [Discovery Agent]
              ↓
         需求确认 ← 客户确认
              ↓
         [Designer Agent]
              ↓
         设计确认 ← 客户确认
              ↓
         [Creator Agent]
              ↓
         [Reviewer Agent]
              ↓
         修复问题 (循环直到通过)
              ↓
         预览确认 ← 客户确认
              ↓
         [Launcher Agent]
              ↓
         上线完成 → 交付客户
```

## Workspace Structure

```
project-name/
├── discovery/
│   ├── requirements.md          # 需求文档
│   ├── competitor-analysis.md   # 竞争对手分析
│   ├── sitemap.md              # 网站地图
│   └── client-brief.md         # 客户简报
│
├── design/
│   ├── brand-kit.md            # 品牌工具包(颜色/字体/风格)
│   ├── design-spec.md          # 设计规格说明
│   ├── wireframes/             # 线框图
│   │   ├── homepage.html
│   │   ├── about.html
│   │   └── services.html
│   └── mockups/                # 高保真设计稿
│       └── homepage-mockup.html
│
├── build/
│   ├── index.html              # 首页
│   ├── about.html
│   ├── services.html
│   ├── contact.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│
├── review/
│   ├── review-report.md        # 审查报告
│   ├── lighthouse-scores.md    # 性能评分
│   ├── seo-audit.md           # SEO审计
│   └── accessibility-check.md  # 无障碍检查
│
└── launch/
    ├── launch-checklist.md     # 上线清单
    ├── dns-config.md           # DNS配置记录
    └── post-launch-monitor.md  # 上线后监控
```

## Quick Start

### 新客户项目
```
用户: "帮我的客户[业务名]设计一个网站"
→ 读取 agents/discovery.md
→ 执行客户调研流程
→ 输出 requirements.md
→ 继续到 Designer Agent
```

### 直接建站
```
用户: "帮我做一个[类型]的网站，要求是[需求]"
→ 快速Discovery(从对话提取需求)
→ 读取 agents/designer.md
→ 执行设计流程
→ 读取 agents/creator.md
→ 开始构建
```

### 改版现有站
```
用户: "帮我改版[URL]这个网站"
→ 读取 agents/discovery.md
→ 审计现有网站
→ 提出改进方案
→ 走完整流程
```

## Design Knowledge Base

### 7大设计原则
1. **清晰(Clarity)** — 用户不该猜网站是做什么的
2. **视觉层级(Visual Hierarchy)** — 用大小/颜色/对比度引导注意力
3. **一致性(Consistency)** — 颜色/字体/按钮/间距全站统一
4. **响应式(Responsive)** — Desktop/Tablet/Mobile全适配
5. **可访问性(Accessibility)** — WCAG 2.2 AA，对比度≥4.5:1
6. **速度(Performance)** — 页面加载<3秒，Core Web Vitals达标
7. **转化导向(Conversion)** — 每页有明确CTA，减少用户操作步骤

### UI/UX法则
- **Hick's Law**: 选项越少决策越快 → 简化导航
- **Fitts' Law**: 目标越大越近越容易点 → CTA按钮大且显眼
- **Gestalt接近性**: 靠近的元素被视为一组 → 用间距分组
- **F型阅读**: 用户F型扫描页面 → 重要内容放左上
- **3秒法则**: 3秒内抓住注意力 → Hero Section极度清晰

### 每个网站必须有的7个区块
1. **Header** — Logo + 导航 + CTA按钮
2. **Hero Section** — 标题 + 副标题 + CTA + 高质量图片
3. **Pain Points** — 客户面临的3-4个核心问题
4. **Solution/Services** — 服务如何解决问题
5. **Social Proof** — 评价/案例/合作品牌
6. **About** — 简短品牌故事
7. **CTA + Footer** — 最终行动号召 + 联系方式

### 配色架构
```
├── Primary — 品牌核心色(CTA、重要元素)
├── Secondary — 支撑色(次要按钮、信息链接)
├── Accent — 点缀色(吸引注意力)
├── Background — 页面底色、卡片背景
├── Surface — 输入框、卡片
├── Text — 标题色 + 正文色 + 次要文字色
└── Semantic — 成功(绿)/警告(黄)/错误(红)/信息(蓝)
```

### CTA设计规则
- **颜色**: 与背景形成强对比，红/橙=紧迫，绿=行动，蓝=信任
- **位置**: Above the fold必须有一个，页尾必须有一个
- **文案**: 动作导向("立即咨询"不是"提交")，第一人称("开始我的免费试用")
- **大小**: 按钮字号=正文的2倍，不能太大(banner blindness)也不能太小
- **间距**: 周围留白让CTA呼吸
- **每页一个主CTA**: 清晰胜过杂乱

### 转化7原则(Conversion-Centered Design)
1. **注意力**: 用对比色和留白聚焦CTA
2. **上下文**: CTA与页面内容一致
3. **清晰度**: 用户一眼看懂该做什么
4. **一致性**: 广告→Landing Page信息一致
5. **信任**: 社会证明、安全徽章、评价在CTA附近
6. **紧迫感**: "限时优惠"、"仅剩3个名额"
7. **减少摩擦**: 表单字段越少越好

## Technology Options

### 选择建站技术

| 场景 | 推荐技术 | 原因 |
|------|---------|------|
| 简单展示站(5-10页) | 纯HTML/CSS/JS | 快、轻、便宜 |
| 需要客户自己更新内容 | WordPress + Elementor | 客户友好的CMS |
| 电商 | WordPress + WooCommerce | 成熟的电商生态 |
| 高性能单页 | React/Next.js | SPA体验 |
| 快速原型/Landing Page | Claude直接生成HTML | 最快速度 |

### Claude直接创建网站的能力
Claude可以直接生成完整的网站代码：
- 纯HTML + Tailwind CSS + Vanilla JS
- React组件(.jsx)
- 完整的多页面网站
- 响应式设计
- 动画和交互效果

对于Oskris的业务模式(用Claude替代开发团队)，推荐：
- **小型项目**: Claude直接生成HTML/CSS/JS
- **需要CMS**: Claude生成WordPress主题 + 部署到VPS
- **复杂项目**: Claude Code + WordPress

## Malaysia Market Context

- 82%马来西亚人每天上网，大部分用手机
- 必须支持: FPX、Boost、TNG、GrabPay支付
- 多语言考虑: EN/BM/CN
- 文化色彩: 红=吉祥, 金=高端, 绿=伊斯兰意义
- WhatsApp集成是标配
- 本地托管优先(延迟低)

## Delegating Work

**With subagents (Claude Code)**:
Spawn independent agents with reference file instructions for parallel work.

**Without subagents (Claude.ai)**:
Read agent reference files and follow procedures sequentially in main loop.

## Coordinator Checklist

每个项目必须确保：
- [ ] 客户需求完整记录
- [ ] 竞争对手已分析
- [ ] 设计方向已确认
- [ ] 品牌系统已建立
- [ ] 线框图已通过
- [ ] 视觉设计已通过
- [ ] 网站已构建
- [ ] 响应式已测试
- [ ] 性能已优化
- [ ] SEO已配置
- [ ] 无障碍已检查
- [ ] 客户已预览确认
- [ ] 网站已部署上线
- [ ] 上线后监控已设置
