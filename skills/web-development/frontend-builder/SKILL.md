---
name: frontend-builder
description: Professional frontend development implementation following design specifications. Use when building websites, implementing designs, converting mockups to code, creating responsive layouts, or developing interactive features. Prioritizes clean code, performance, and maintainability.
---

# Frontend Builder Skill

将设计方案转化为可运行的专业级代码。

## 使用时机

- 实现设计稿为代码
- 构建响应式网站
- 开发交互功能
- 代码审查和优化

## 技术选型指南

| 场景 | 推荐技术 | 原因 |
|------|---------|------|
| 简单展示站(5-10页) | 纯HTML + Tailwind CSS + Vanilla JS | 快、轻、便宜 |
| 需要CMS | WordPress + 自定义主题 | 客户友好 |
| 电商 | WordPress + WooCommerce | 成熟生态 |
| 自定义WebApp | Next.js + React + Tailwind | 现代、可扩展 |
| 快速原型/Landing Page | Claude直接生成HTML | 最快速度 |

## 静态网站结构

```
├── index.html
├── about.html
├── services.html
├── contact.html
├── css/style.css
├── js/script.js
└── images/
```

## WordPress主题结构

```
├── style.css (主题信息)
├── functions.php
├── index.php / header.php / footer.php / page.php / single.php
├── template-parts/
├── assets/css/ + js/ + images/
└── inc/custom-functions.php
```

**必备插件**: WooCommerce(电商), FPX/Stripe(支付), Ninja Van/J&T(物流), Yoast/RankMath(SEO), WP Rocket+Imagify(性能)

## 开发规范

### HTML
- 语义化标签: header, nav, main, section, article, footer
- SEO必备: meta description, og tags, structured data
- 无障碍: alt属性, aria标签, 键盘导航
- charset UTF-8, viewport meta

### CSS (优先Tailwind)
- CSS变量管理颜色、字体、间距
- Mobile-first响应式: 640px / 1024px / 1280px
- 避免 !important
- BEM命名(如不用Tailwind)

### CSS变量模板
```css
:root {
  --primary: #0A192F;
  --secondary: #00D1FF;
  --accent: #F97316;
  --text-dark: #111827;
  --text-light: #6B7280;
  --bg-light: #F9FAFB;
  --font-heading: 'Montserrat', sans-serif;
  --font-body: 'Inter', sans-serif;
}
```

### JavaScript
- Vanilla JS优先，按需引入库
- 事件委托减少监听器
- 图片懒加载: loading="lazy"
- 关键CSS内联，JS异步加载

## 核心组件清单

每个网站必须实现:

### 1. 导航栏
- 固定顶部，滚动时半透明背景
- 移动端汉堡菜单
- 当前页面高亮
- CTA按钮在导航栏中

### 2. Hero Section
- 全屏或大尺寸背景
- 标题(h1) + 副标题 + CTA按钮
- 移动端文字居中，桌面端可左对齐

### 3. 服务/功能展示
- 卡片网格布局(移动1列，桌面3列)
- 图标 + 标题 + 描述
- Hover效果

### 4. 社会证明
- 客户评价轮播
- 合作品牌Logo条
- 数据统计(计数器动画)

### 5. 联系表单
- 姓名、邮箱/电话、消息
- 前端验证 + 后端处理
- WhatsApp快捷按钮(马来西亚必备)

### 6. Footer
- 联系信息 + 快速链接 + 社交媒体
- 版权信息
- 隐私政策链接

## 性能优化

### 图片
- WebP格式优先
- srcset响应式图片
- 压缩: 质量80%
- 懒加载: loading="lazy"
- 尺寸: Hero ≤200KB, 缩略图 ≤50KB

### 加载速度
- 关键CSS内联到head
- JS放body底部或async/defer
- 字体: font-display: swap + preload
- 目标: LCP <2.5s, FID <100ms, CLS <0.1

### SEO基础
```html
<title>页面标题 | 站点名</title>
<meta name="description" content="描述">
<link rel="canonical" href="URL">
<script type="application/ld+json">结构化数据</script>
```

## 动画规范

- 过渡: 0.3s ease
- 入场动画: CSS @keyframes, IntersectionObserver触发
- Hover: transform scale(1.02), box-shadow增强
- 避免: layout触发动画(用transform/opacity)
- prefers-reduced-motion媒体查询

## 马来西亚特殊要求

- WhatsApp浮动按钮(固定右下角)
- 多语言: EN/BM/CN (hreflang标签)
- 支付集成: FPX、Boost、TNG、GrabPay
- 谷歌地图嵌入(本地商家)
- 马来西亚节日配色主题

## 交付清单

- [ ] 所有页面完成且响应式
- [ ] 无console错误
- [ ] PageSpeed ≥80
- [ ] SEO meta完整
- [ ] 表单可提交
- [ ] WhatsApp集成
- [ ] 跨浏览器测试(Chrome/Safari/Firefox)
- [ ] 图片已压缩+懒加载
- [ ] 无障碍基础通过

## 整合其他Skills

```
design-consultant → 输出设计规格
  ↓
frontend-builder (本skill) → 输出可运行网站
  ↓
reviewer → 质量检查
  ↓
launcher → 部署上线
```
