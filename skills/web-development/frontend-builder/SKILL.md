---
name: frontend-builder
description: Professional frontend development implementation following design specifications. Use when building websites, implementing designs, converting mockups to code, creating responsive layouts, or developing interactive features. Prioritizes clean code, performance, and maintainability.
---

# Frontend Builder Skill

实现网站设计为生产就绪代码。强调最佳实践、性能和代码质量。

## When to Use
- 实现已批准的设计稿
- 构建网站布局
- 创建响应式组件
- 开发交互功能
- 代码审查和优化

## Input Requirements
- Design mockups/wireframes (from design-consultant)
- Technical requirements (from requirements-analyst)
- Content and assets ready
- Hosting environment prepared

## Technology Stack

### Simple Sites (5-10 pages)
**Static HTML + CSS + JS** — 快速、轻量、低成本
```
├── index.html
├── css/style.css
├── js/script.js
└── images/
```

### WordPress Sites (SME标配)
**WordPress + Custom Theme** — 客户友好CMS
Essential Plugins: WooCommerce, FPX/Stripe, Yoast/RankMath, WP Rocket

### E-commerce
**WordPress + WooCommerce** — 成熟生态
Payment: FPX, Boost, TNG, GrabPay | Shipping: Ninja Van, J&T

### Custom Web Apps
**Next.js / React + Tailwind CSS** — 现代、SEO友好、可扩展

## Development Best Practices

### 1. Code Organization
HTML: Semantic structure with proper meta tags, OG tags, structured data (JSON-LD)
CSS: Variables for colors/fonts/spacing, mobile-first media queries, BEM naming
JS: Defer non-critical scripts, use modules, minimal dependencies

### 2. Responsive (Mobile-First)
```css
/* Base: mobile */
.grid { display: grid; grid-template-columns: 1fr; gap: 1rem; }
/* Tablet 768px */
@media (min-width: 768px) { .grid { grid-template-columns: repeat(2, 1fr); } }
/* Desktop 1024px */
@media (min-width: 1024px) { .grid { grid-template-columns: repeat(3, 1fr); gap: 2rem; } }
```
Test: 375px (iPhone SE) → 768px (iPad) → 1280px (Laptop) → 1920px (Desktop)

### 3. Performance
Images: WebP + fallback, srcset for responsive, loading="lazy"
CSS: Minify, remove unused, inline critical CSS
JS: defer/async, code splitting, tree shaking
Target: LCP <2.5s, FID <100ms, CLS <0.1

### 4. Accessibility (WCAG 2.2 AA)
- Semantic HTML: header, nav, main, article, footer (不用div套div)
- ARIA labels for buttons/nav/inputs
- Keyboard navigation with visible focus states
- Color contrast ≥4.5:1
- Skip-to-content link

### 5. Forms
- Label + input配对, required + aria-required
- Client-side validation + server-side validation
- AJAX submit with loading state and error handling
- Phone pattern: `[0-9]{10,11}` (Malaysian format)

### 6. SEO Implementation
```html
<title>50-60 chars | Brand</title>
<meta name="description" content="150-160 chars">
<meta property="og:title/description/image/url">
<link rel="canonical" href="...">
<script type="application/ld+json">{ "@context": "https://schema.org", ... }</script>
```
Structured Data types: LocalBusiness, Product, Service, FAQ, BreadcrumbList

### 7. Malaysian Integrations

**WhatsApp CTA** (fixed bottom-right):
```html
<a href="https://wa.me/60XXXXXXXXX?text=Hi" class="whatsapp-btn">Chat on WhatsApp</a>
```

**Payment**: Billplz API (FPX), Stripe (cards), Boost/TNG (e-wallets)
**Maps**: Google Maps embed with business marker
**Multi-language**: EN/BM/CN switcher

## Component Patterns

### Navigation Bar
- Logo left + menu center/right + CTA button
- Mobile: hamburger menu with slide-in drawer
- Sticky on scroll with backdrop blur
- Active page indicator

### Hero Section
- Full-width background (image/gradient/video)
- H1 headline + subtitle + primary CTA
- Trust indicators below CTA
- Responsive: stack vertically on mobile

### Service Cards
- Icon/image + title + short description + link
- Grid: 3-col desktop, 2-col tablet, 1-col mobile
- Hover effect: subtle shadow/scale
- Consistent card height

### Testimonials
- Avatar + name + role + quote
- Carousel or grid layout
- Star rating if applicable

### Contact Section
- Split layout: form left + info right
- WhatsApp + phone + email + address
- Google Maps embed
- Business hours

### Footer
- Multi-column: company, services, contact, social
- Copyright + privacy + terms links
- WhatsApp floating button

## WordPress Checklist
- [ ] Child theme created (not editing parent)
- [ ] Custom post types registered
- [ ] ACF fields configured
- [ ] SEO plugin configured
- [ ] Caching enabled (WP Rocket/LiteSpeed)
- [ ] Security plugin installed (Wordfence)
- [ ] Auto-updates configured
- [ ] Backup solution (UpdraftPlus)
- [ ] SSL certificate active

## Testing Checklist
- [ ] All links working (no 404s)
- [ ] Forms submit correctly
- [ ] Images load and have alt text
- [ ] Mobile responsive (3 breakpoints)
- [ ] Cross-browser (Chrome, Safari, Firefox)
- [ ] Page speed <3s (GTmetrix/PageSpeed Insights)
- [ ] Accessibility scan passed (axe DevTools)
- [ ] SEO audit passed (Lighthouse)
- [ ] SSL/HTTPS working
- [ ] Analytics installed (Google Analytics 4)
- [ ] Favicon and OG images set
- [ ] 404 page customized

## Handover Documentation
每个项目交付时提供:
1. **Technical spec** — 技术架构、文件结构、依赖列表
2. **Content guide** — 如何更新内容、图片尺寸规范
3. **Login credentials** — WordPress admin, hosting, domain
4. **Maintenance guide** — 更新插件、备份流程
5. **Training video** — 基本操作录屏(可选)

## Quality Standards
- Core Web Vitals全绿
- Lighthouse Score: Performance ≥90, Accessibility ≥90, SEO ≥90
- W3C Validator零error
- 无console errors
- 所有功能在slow 3G下可用
