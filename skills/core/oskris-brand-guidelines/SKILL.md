---
name: oskris-brand-guidelines
description: Oskris 网站设计公司的品牌视觉规范。为所有客户交付物、营销素材、提案文档、网站设计应用统一的品牌风格。当需要创建带有 Oskris 品牌风格的任何内容时使用此 Skill。
---

# Oskris 品牌视觉规范

## 概述

Oskris 是一家面向马来西亚、新加坡和中国市场的专业网站设计公司。品牌定位为"专业、现代、值得信赖"，视觉风格需要传达技术能力与设计品味的结合。

**关键词**: 品牌色彩、排版、视觉标准、设计规范、Oskris 品牌、提案风格、客户交付物

## 品牌色彩体系

### 主色调 (Primary)

| 名称 | 色值 | RGB | 用途 |
|------|------|-----|------|
| 深夜黑 | `#191919` | (25, 25, 25) | 主文字、深色背景、Header |
| 品牌蓝 | `#2563EB` | (37, 99, 235) | CTA 按钮、链接、重点强调 |
| 纯净白 | `#FFFFFF` | (255, 255, 255) | 主背景、卡片背景 |

### 辅助色 (Secondary)

| 名称 | 色值 | RGB | 用途 |
|------|------|-----|------|
| 暖灰 | `#6B7280` | (107, 114, 128) | 次要文字、说明文字 |
| 浅灰底 | `#F3F4F6` | (243, 244, 246) | 区块背景、分隔区域 |
| 边框灰 | `#E5E7EB` | (229, 231, 235) | 边框、分隔线 |

### 功能色 (Functional)

| 名称 | 色值 | 用途 |
|------|------|------|
| 成功绿 | `#10B981` | 成功状态、完成标记 |
| 警告橙 | `#F59E0B` | 提醒、注意事项 |
| 错误红 | `#EF4444` | 错误提示、删除操作 |

### Python 中使用

```python
OSKRIS_COLORS = {
    # 主色
    'dark': (25, 25, 25),
    'brand_blue': (37, 99, 235),
    'white': (255, 255, 255),
    # 辅助色
    'gray': (107, 114, 128),
    'light_bg': (243, 244, 246),
    'border': (229, 231, 235),
    # 功能色
    'success': (16, 185, 129),
    'warning': (245, 158, 11),
    'error': (239, 68, 68),
}
```

### CSS 变量

```css
:root {
    --oskris-dark: #191919;
    --oskris-blue: #2563EB;
    --oskris-white: #FFFFFF;
    --oskris-gray: #6B7280;
    --oskris-light-bg: #F3F4F6;
    --oskris-border: #E5E7EB;
    --oskris-success: #10B981;
    --oskris-warning: #F59E0B;
    --oskris-error: #EF4444;
}
```

## 排版规范

### 字体选择

| 用途 | 首选字体 | 备选字体 | 说明 |
|------|---------|---------|------|
| 英文标题 | Inter | Arial, Helvetica | 现代感、专业感 |
| 英文正文 | Inter | Arial, Helvetica | 保持一致性 |
| 中文标题 | Noto Sans SC | PingFang SC, Microsoft YaHei | 支持简繁体 |
| 中文正文 | Noto Sans SC | PingFang SC, Microsoft YaHei | 可读性优先 |
| 代码 | JetBrains Mono | Consolas, monospace | 技术内容 |

### 字号层级

```css
/* 网页端 */
h1 { font-size: 2.5rem; font-weight: 700; line-height: 1.2; }     /* 40px - 页面标题 */
h2 { font-size: 2rem; font-weight: 600; line-height: 1.3; }       /* 32px - 区块标题 */
h3 { font-size: 1.5rem; font-weight: 600; line-height: 1.4; }     /* 24px - 子标题 */
h4 { font-size: 1.25rem; font-weight: 500; line-height: 1.4; }    /* 20px - 小标题 */
body { font-size: 1rem; font-weight: 400; line-height: 1.6; }     /* 16px - 正文 */
small { font-size: 0.875rem; font-weight: 400; line-height: 1.5; } /* 14px - 辅助文字 */
```

### Python-pptx 中使用

```python
from pptx.util import Pt
from pptx.dml.color import RGBColor

# 标题样式
title_font_size = Pt(28)
title_color = RGBColor(25, 25, 25)
title_font = 'Inter'

# 正文样式
body_font_size = Pt(14)
body_color = RGBColor(107, 114, 128)
body_font = 'Inter'

# 强调样式
accent_font_size = Pt(16)
accent_color = RGBColor(37, 99, 235)
```

## 设计原则

### 1. 克制与专业
- 使用最少的色彩完成设计（主色 + 1个强调色 + 灰色系）
- 避免渐变色、阴影过重、花哨装饰
- 让留白成为设计的一部分

### 2. 一致性
- 所有交付物使用相同的色彩体系
- 间距使用 8px 基准网格（8, 16, 24, 32, 48, 64, 96）
- 圆角统一：小元素 4px，卡片 8px，大容器 12px

### 3. 可读性优先
- 正文行高 1.6，标题行高 1.2-1.4
- 段落间距 ≥ 16px
- 中文正文最小 14px，英文最小 14px
- 确保色彩对比度符合 WCAG AA 标准（≥ 4.5:1）

### 4. 多语言适配
- 同时考虑中文、英文、马来文的排版需求
- 中文段落避免两端对齐（会产生不均匀间距）
- 英文使用左对齐，数字使用等宽字体

## 应用场景

### 客户提案文档
- 封面: 深色背景 (#191919) + 白色 Logo + 品牌蓝装饰线
- 内页: 白色背景 + 深色标题 + 灰色正文
- 定价页: 品牌蓝高亮当前推荐方案
- 页脚: 浅灰背景 + oskris.com + 联系方式

### 网站设计交付
- Header: 白色或深色背景
- CTA 按钮: 品牌蓝 (#2563EB) 填充 + 白色文字 + 8px 圆角
- 次要按钮: 白色填充 + 品牌蓝边框 + 品牌蓝文字
- Footer: 深色背景 (#191919) + 浅灰文字

### 社交媒体素材
- 背景: 品牌蓝渐变或纯净白
- 文字: 高对比度，确保手机端可读
- Logo: 始终放在固定位置（右下角或左上角）

## Logo 使用规范

### 最小尺寸
- 网页: 宽度 ≥ 120px
- 打印: 宽度 ≥ 25mm
- 图标: 最小 32x32px

### 安全区域
- Logo 四周保留等于 Logo 高度 50% 的空白区域
- 安全区域内不放置其他元素

### 禁止操作
- 不拉伸变形
- 不改变 Logo 颜色（除单色版本）
- 不在杂乱背景上使用
- 不旋转 Logo

## 文件命名规范

所有设计文件遵循统一命名：
```
oskris-[类型]-[描述]-[版本].[扩展名]

示例:
oskris-proposal-client-name-v1.pptx
oskris-website-homepage-v2.html
oskris-social-ig-post-promo.png
oskris-logo-dark-bg.svg
```

---

> **版本**: v1.0（2026-02-16）
> **维护**: 当 Oskris 品牌确定最终设计后更新此规范
> **注意**: 目前品牌色和字体为初版建议，可根据实际品牌设计调整
