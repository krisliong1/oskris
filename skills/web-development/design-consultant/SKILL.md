---
name: design-consultant
description: Professional web design consultation and proposal creation. Use when translating requirements into design solutions, creating design proposals, selecting color schemes, planning layouts, or presenting design concepts to clients. Works with output from requirements-analyst skill.
---

# Design Consultant Skill

创建专业设计方案，将业务需求转化为视觉解决方案。

## 使用时机

- 需求收集完成后(来自requirements-analyst)
- 创建设计提案给客户
- 选择视觉风格和配色
- 规划网站布局
- 设计评审和决策

## 输入要求

- 完整需求文档
- 客户业务类型和目标受众
- 预算约束
- 品牌资产(如有logo/品牌色)

## 风格分析框架

根据客户业务类型推荐设计风格:

| 业务类型 | 风格 | 特点 |
|---------|------|------|
| 电商/游戏 | 现代科技感 | 深色主题+霓虹强调色,高对比CTA,网格布局 |
| 企业/专业服务 | 简洁专业 | 信任元素,蓝灰配色,清晰层级 |
| 创意/作品集 | 大胆独特 | 展示为主,艺术字体,大留白,交互元素 |
| 本地零售 | 实用功能型 | 清晰导航,产品为主,移动优先,WhatsApp集成 |
| 餐饮/服务 | 温暖亲切 | 暖色调,大图片,简单预订流程 |

## 配色方案

### 选择流程
1. 分析现有品牌色(如有)
2. 考虑行业标准和文化含义
3. 测试无障碍(WCAG对比度≥4.5:1)
4. 创建明暗主题变体

### 推荐配色(按类型)

**科技/游戏**: Primary #0A192F, Accent #00D1FF, CTA #F97316
**专业服务**: Primary #1E40AF, Secondary #059669, Background #F8FAFC
**创意**: Primary #7C3AED, Accent #EC4899, Background #FAFAFA
**本地零售**: Primary #DC2626, Secondary #F59E0B, Background #FFFFFF

### 马来西亚文化配色
- 红色=吉祥(华人市场)
- 金色=高端
- 绿色=伊斯兰意义
- 避免全白(丧事联想)

## 配色架构模板

```
Primary   — 品牌核心色(CTA、重要元素)
Secondary — 支撑色(次要按钮、信息链接)
Accent    — 点缀色(吸引注意力)
Background— 页面底色、卡片背景
Surface   — 输入框、卡片
Text      — 标题色 + 正文色 + 次要文字色
Semantic  — 成功(绿)/警告(黄)/错误(红)/信息(蓝)
```

## 字体选择

### 推荐组合

| 用途 | 标题字体 | 正文字体 |
|------|---------|---------|
| 专业 | Montserrat / Poppins | Open Sans / Inter |
| 创意 | Playfair Display / DM Serif | Lora / Source Serif |
| 科技 | Space Grotesk / JetBrains Mono | DM Sans / Manrope |
| 本地化 | Noto Sans SC(中文) | Noto Sans(多语言) |

规则: 最多2种字体，标题和正文形成对比。

## 布局结构

### 7大必备板块
1. **Header** — Logo + 导航 + CTA按钮
2. **Hero Section** — 标题 + 副标题 + CTA + 高质量图片
3. **Pain Points** — 客户面临的3-4个核心问题
4. **Services/Solution** — 服务如何解决问题
5. **Social Proof** — 评价/案例/合作品牌
6. **About** — 简短品牌故事
7. **CTA + Footer** — 最终行动号召 + 联系方式

### 响应式断点
- Mobile: < 640px (单列)
- Tablet: 640-1024px (双列)
- Desktop: > 1024px (多列)

## 设计提案模板

向客户展示时包含:

1. **设计概念**: 整体风格方向和理由
2. **配色方案**: 带色块展示的完整配色
3. **字体方案**: 标题和正文字体预览
4. **布局结构**: 线框图展示页面结构
5. **关键设计元素**: CTA按钮、卡片、表单等组件
6. **响应式行为**: 不同设备的适配说明
7. **时间线**: 设计→开发→上线预估
8. **修改政策**: 含X次免费修改

## CTA设计规则

- 颜色: 与背景强对比(红/橙=紧迫,绿=行动,蓝=信任)
- 位置: Above the fold必须有一个,页尾必须有一个
- 文案: 动作导向("立即咨询"不是"提交"),第一人称
- 大小: 字号=正文的2倍,不过大(banner blindness)
- 周围留白让CTA呼吸
- 每页一个主CTA

## 整合其他Skills

```
requirements-analyst → 输出需求文档
  ↓
design-consultant (本skill) → 输出设计方案+品牌系统
  ↓
frontend-builder → 将设计转化为代码
```

## 质量检查

- [ ] 配色通过WCAG 2.2 AA对比度测试
- [ ] 字体在所有设备可读
- [ ] 布局Mobile-first响应式
- [ ] CTA位置和文案清晰
- [ ] 设计风格与客户业务匹配
- [ ] 马来西亚文化适配
