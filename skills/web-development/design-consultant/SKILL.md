---
name: design-consultant
description: Professional web design consultation and proposal creation. Use when translating requirements into design solutions, creating design proposals, selecting color schemes, planning layouts, or presenting design concepts to clients. Works with output from requirements-analyst skill.
---

# Design Consultant — 网站设计顾问

将需求转化为视觉设计方案，输出品牌系统和设计规格。

## When to Use
- 制定设计方案
- 选择配色和字体
- 规划页面布局
- 创建设计提案
- 回应客户设计反馈

## Input
- requirements.md (from requirements-analyst)
- 客户品牌资料（logo, 现有材料）
- 竞争对手参考
- 客户偏好和禁忌

## Core Design Framework

### 1. Style Analysis
分析客户行业、目标受众、竞对风格，确定设计方向:
- **企业/专业**: 深蓝+白, 简洁线条, 大量留白
- **创意/时尚**: 大胆用色, 非对称布局, 动效丰富
- **本地商业**: 温暖配色, 友好图片, WhatsApp显眼
- **电商**: 产品突出, 信任标志, 快速结算

### 2. Color Scheme

**配色架构**:
- Primary — 品牌核心色 (CTA, 重要元素)
- Secondary — 支撑色 (次要按钮, 链接)
- Accent — 点缀色 (吸引注意力)
- Background — 页面底色, 卡片背景
- Text — 标题色 + 正文色 + 次要文字色
- Semantic — 成功(绿) / 警告(黄) / 错误(红) / 信息(蓝)

**行业配色参考**:
| 行业 | 推荐主色 | 理由 |
|------|---------|------|
| 科技 | 蓝+白 | 信任、专业 |
| 餐饮 | 红/橙+暖白 | 食欲、温暖 |
| 健康 | 绿+白 | 自然、健康 |
| 金融 | 深蓝/金 | 稳重、高端 |
| 教育 | 蓝+绿 | 智慧、成长 |
| 零售 | 品牌色为主 | 品牌识别 |

**马来西亚文化色彩**: 红=吉祥, 金=高端, 绿=伊斯兰意义, 避免全黑(丧事)

### 3. Typography

**原则**: 最多2种字体 — 标题字体 + 正文字体

**推荐搭配**:
- 专业: Montserrat + Inter
- 现代: Poppins + Open Sans
- 优雅: Playfair Display + Lato
- 科技: Space Grotesk + DM Sans

**层级**: H1 48-64px → H2 36-48px → H3 24-36px → Body 16-18px → Small 14px
**行高**: 标题 1.2 | 正文 1.6 | 长文 1.8

### 4. Layout Planning

**标准页面布局**:

**Homepage**: Hero → Pain Points → Services → Social Proof → About → CTA → Footer
**About**: Hero → Story → Team → Values → Timeline → CTA
**Services**: Hero → Overview → Service Details → Process → Pricing → FAQ → CTA
**Contact**: Hero → Form + Info → Map → FAQ

**Grid System**: 12-column, max-width 1280px, gutters 24-32px

### 5. Component Design

**必须有的组件**:
- Navigation (desktop + mobile hamburger)
- Hero Section (headline + CTA + trust indicators)
- Service/Feature Cards (icon + title + description)
- Testimonial Cards (avatar + quote + name)
- Contact Form (name, email, phone, message)
- WhatsApp Float Button (fixed bottom-right)
- Footer (multi-column + social links)

**CTA设计规则**:
- 颜色与背景强对比
- 文案动作导向 ("立即咨询" 不是 "提交")
- Above the fold必有一个, 页尾必有一个
- 按钮够大(min 44x44px touch target)
- 周围留白让CTA呼吸

### 6. Mobile-First
- 所有设计先做手机版
- 手机上内容纵向堆叠
- 触摸目标 ≥44x44px
- 简化导航（hamburger menu）
- 电话号码可点击拨打

### 7. Malaysia Adaptations
- WhatsApp是首选联系方式
- 支持多语言（EN/BM/CN）
- 本地支付标志（FPX, Boost, TNG）
- Google Maps嵌入
- 马来西亚商业注册号显示

## Design Proposal Template

```markdown
# [Client Name] 网站设计方案

## 1. Design Concept — 设计理念
[一段话描述整体设计方向和为什么适合客户]

## 2. Visual Style — 视觉风格
- 风格: [Modern/Classic/Minimal/Bold]
- 参考: [2-3个参考网站URL]

## 3. Color Palette
- Primary: [色值] — [用途]
- Secondary: [色值] — [用途]
- Accent: [色值] — [用途]
- Background: [色值]
- Text: [色值]

## 4. Typography
- Heading: [字体名]
- Body: [字体名]

## 5. Page Structure
[列出每个页面的板块]

## 6. Key Design Elements
[特殊设计元素: 动画, 图标风格, 图片风格]

## 7. Responsive Behavior
[Mobile/Tablet/Desktop 差异]

## 8. Timeline
- Wireframe: X天
- Design: X天
- Revision: X天

## 9. Revision Policy
包含X次大改，额外修改按小时收费
```

## Common Challenges

**"Everything above the fold"**: 解释F-pattern阅读习惯，重要信息优先，但不能塞满

**"Make logo bigger"**: Logo已够显眼，更大会破坏比例，建议用品牌色强化存在感

**"Too many colors/fonts"**: 限制2-3色+2字体，展示对比效果说服客户

**"Like [famous brand]"**: 提取他们喜欢的具体元素，而不是照搬（版权+不适合）

## Quality Checklist
- [ ] 配色对比度≥4.5:1
- [ ] 字体层级清晰
- [ ] CTA位置显眼
- [ ] Mobile布局合理
- [ ] 品牌一致性
- [ ] 留白充足
- [ ] 视觉层次分明
