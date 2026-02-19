---
name: brand-guidelines
description: Oskris网站设计公司品牌视觉规范。为客户交付物、营销素材、提案文档、网站设计应用统一品牌风格。当创建任何带Oskris品牌风格的内容时使用。
---

# Oskris Brand Guidelines

面向马来西亚、新加坡和中国市场的专业网站设计公司。品牌定位：专业、现代、值得信赖。

## 色彩体系

### 主色

| 名称 | 色值 | 用途 |
|------|------|------|
| 深夜黑 | `#191919` | 主文字、深色背景、Header |
| 品牌蓝 | `#2563EB` | CTA按钮、链接、重点强调 |
| 纯净白 | `#FFFFFF` | 主背景、卡片背景 |

### 辅助色

| 名称 | 色值 | 用途 |
|------|------|------|
| 暖灰 | `#6B7280` | 次要文字 |
| 浅灰底 | `#F3F4F6` | 区块背景 |
| 边框灰 | `#E5E7EB` | 边框、分隔线 |

### 功能色

成功 `#10B981` / 警告 `#F59E0B` / 错误 `#EF4444`

### 代码引用

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

```python
OSKRIS_COLORS = {
    'dark': (25, 25, 25), 'brand_blue': (37, 99, 235), 'white': (255, 255, 255),
    'gray': (107, 114, 128), 'light_bg': (243, 244, 246), 'border': (229, 231, 235),
    'success': (16, 185, 129), 'warning': (245, 158, 11), 'error': (239, 68, 68),
}
```

## 排版

| 用途 | 字体 | 备选 |
|------|------|------|
| 英文 | Inter | Arial, Helvetica |
| 中文 | Noto Sans SC | PingFang SC, Microsoft YaHei |
| 代码 | JetBrains Mono | Consolas, monospace |

字号：h1 2.5rem/700 → h2 2rem/600 → h3 1.5rem/600 → h4 1.25rem/500 → body 1rem/400 → small 0.875rem

## 设计原则

- **克制**：最少色彩完成设计，避免渐变/重阴影/花哨装饰，留白是设计的一部分
- **一致**：间距用8px网格(8,16,24,32,48,64,96)，圆角统一(小4px/卡片8px/容器12px)
- **可读**：正文行高1.6，段落间距≥16px，中文最小14px，色彩对比≥4.5:1(WCAG AA)
- **多语言**：中英马三语适配，中文段落避免两端对齐

## 应用场景

**客户提案**：封面深色背景+白色Logo+品牌蓝装饰线，内页白底+深色标题，定价页品牌蓝高亮推荐方案

**网站交付**：CTA按钮品牌蓝填充+白色文字+8px圆角，次要按钮白色+品牌蓝边框，Footer深色背景

**文件命名**：`oskris-[类型]-[描述]-[版本].[扩展名]`，如 `oskris-proposal-clientname-v1.pptx`

## Logo规范

最小尺寸：网页≥120px宽，打印≥25mm宽，图标≥32x32px。安全区域：Logo高度50%。禁止拉伸、改色、杂乱背景、旋转。

> 版本 v1.0 — 品牌色和字体为初版建议，确定最终设计后更新。
