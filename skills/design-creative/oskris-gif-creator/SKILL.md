---
name: oskris-gif-creator
description: 为 Oskris 网站设计业务创建专业动画 GIF。用于网站 hero 动画、加载动画、产品展示动效、社交媒体素材、客户演示 GIF 等。当用户需要为网站或营销素材创建 GIF 动画时使用此 Skill。
---

# Oskris GIF Creator

为 Oskris 网站设计业务创建专业级动画 GIF 的工具包。涵盖网站动画素材、客户演示动效、社交媒体营销素材等场景。

## 适用场景

### 网站设计相关
- **Hero 区域动画**: 网站首屏的动态视觉效果
- **加载动画 (Loading)**: 品牌化的页面加载指示器
- **微交互预览**: 按钮悬停、表单反馈等交互动效展示
- **滚动动画预览**: 展示网站滚动时的动画效果
- **Before/After 对比**: 设计改版前后对比动画

### 客户沟通相关
- **方案演示 GIF**: 向客户展示设计方案的动态效果
- **进度展示**: 项目不同阶段的视觉对比
- **功能演示**: 网站功能的快速动画展示

### 营销素材相关
- **社交媒体广告**: WhatsApp/Instagram/小红书 的动态素材
- **报价单装饰**: 为提案文档添加动态元素
- **作品集展示**: Portfolio 中的项目动画展示

## 尺寸规范

### 网站用途
- Hero 动画: 1200x600 或 1920x800（注意文件大小）
- 加载动画: 200x200（需极度优化）
- 图标动画: 64x64 或 128x128
- 功能展示: 800x600

### 社交媒体用途
- WhatsApp 状态: 640x640
- Instagram 帖子: 1080x1080
- 小红书: 1080x1440
- 微信朋友圈: 750x750

### 客户演示用途
- 演示文稿内嵌: 480x360
- 邮件内嵌: 600x400（需 < 1MB）
- 微信发送: 240x240（需 < 500KB）

**通用参数:**
- FPS: 10-30（越低文件越小）
- 颜色数: 48-128（越少文件越小）
- 时长: 网站加载动画 < 2秒，展示动画 < 5秒

## 核心工作流

```python
from PIL import Image, ImageDraw, ImageFont
import math

# 1. 创建 GIF 构建器
width, height = 480, 360
fps = 15
num_frames = 30
frames = []

# 2. 生成帧
for i in range(num_frames):
    frame = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(frame)
    
    t = i / (num_frames - 1)  # 进度 0.0 → 1.0
    
    # 绘制动画内容（使用 PIL 基础图形）
    # draw.ellipse(), draw.rectangle(), draw.polygon(), draw.line()
    
    frames.append(frame)

# 3. 保存为 GIF
frames[0].save(
    'output.gif',
    save_all=True,
    append_images=frames[1:],
    duration=int(1000 / fps),
    loop=0,
    optimize=True
)
```

## Oskris 品牌色彩（创建动画时优先使用）

```python
OSKRIS_COLORS = {
    'primary': (25, 25, 25),        # 深灰/黑 - 主色
    'accent': (217, 119, 87),       # 橙色 - 强调色（可根据实际品牌调整）
    'secondary': (106, 155, 204),   # 蓝色 - 辅助色
    'background': (250, 249, 245),  # 米白 - 背景
    'text': (20, 20, 19),           # 近黑 - 文字
    'light_gray': (232, 230, 220),  # 浅灰 - 分隔线
}
```

> **注意**: 以上为临时品牌色，当 Oskris 确定最终品牌规范后需更新。

## 绘图技巧

### PIL 基础图形
```python
draw = ImageDraw.Draw(frame)

# 圆形/椭圆
draw.ellipse([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)

# 多边形（星形、三角形等）
points = [(x1, y1), (x2, y2), (x3, y3)]
draw.polygon(points, fill=(r, g, b), outline=(r, g, b), width=3)

# 线条
draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=5)

# 矩形（含圆角矩形）
draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=(r, g, b))
```

### 专业感要点
- 线条宽度 ≥ 2px，1px 看起来廉价
- 使用渐变背景增加层次感
- 多层叠加形状增加丰富度
- 颜色对比要强烈（深色描边 + 浅色填充）
- 动画要流畅，使用缓动函数而非线性运动

### 用户上传图片处理
```python
from PIL import Image

uploaded = Image.open('/mnt/user-data/uploads/file.png')
# 直接使用：裁剪、缩放、添加动画效果
# 作为参考：提取配色、风格灵感
```

## 缓动函数（让动画更自然）

```python
import math

def ease_out(t):
    """减速缓出 - 最常用"""
    return 1 - (1 - t) ** 3

def ease_in(t):
    """加速缓入"""
    return t ** 3

def ease_in_out(t):
    """先加速后减速"""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2

def bounce_out(t):
    """弹跳效果"""
    if t < 1/2.75:
        return 7.5625 * t * t
    elif t < 2/2.75:
        t -= 1.5/2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5/2.75:
        t -= 2.25/2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625/2.75
        return 7.5625 * t * t + 0.984375

def elastic_out(t):
    """弹性效果"""
    if t == 0 or t == 1:
        return t
    return 2 ** (-10 * t) * math.sin((t - 0.075) * (2 * math.pi) / 0.3) + 1

def interpolate(start, end, t, easing='ease_out'):
    """在两个值之间插值"""
    easings = {
        'linear': lambda t: t,
        'ease_in': ease_in,
        'ease_out': ease_out,
        'ease_in_out': ease_in_out,
        'bounce_out': bounce_out,
        'elastic_out': elastic_out,
    }
    eased_t = easings.get(easing, ease_out)(t)
    return start + (end - start) * eased_t
```

## 网站设计常用动画模板

### 1. 加载动画（Loading Spinner）
```python
# 旋转圆弧 - 适用于网站加载页面
for i in range(num_frames):
    angle = (i / num_frames) * 360
    draw.arc([cx-r, cy-r, cx+r, cy+r], 
             start=angle, end=angle+270, 
             fill=OSKRIS_COLORS['accent'], width=4)
```

### 2. 淡入展示（Fade In）
```python
# 元素从透明到可见 - 适用于滚动触发动画预览
for i in range(num_frames):
    alpha = int(255 * ease_out(i / (num_frames - 1)))
    overlay = Image.new('RGBA', (w, h), (*OSKRIS_COLORS['primary'], alpha))
    frame = Image.alpha_composite(bg, overlay)
```

### 3. 滑入效果（Slide In）
```python
# 从左/右/下滑入 - 适用于内容区块展示
for i in range(num_frames):
    t = ease_out(i / (num_frames - 1))
    x_offset = int((1 - t) * width)  # 从右侧滑入
    # 在 x_offset 位置绘制内容
```

### 4. 脉冲强调（Pulse）
```python
# 按钮/CTA 的脉冲效果
for i in range(num_frames):
    t = i / (num_frames - 1)
    scale = 1.0 + 0.15 * math.sin(t * 2 * math.pi)
    r = int(base_radius * scale)
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=OSKRIS_COLORS['accent'])
```

### 5. 打字机效果（Typewriter）
```python
# 文字逐字出现 - 适用于 Hero 标语
text = "专业网站设计"
for i in range(num_frames):
    chars_to_show = int(len(text) * (i / (num_frames - 1)))
    draw.text((x, y), text[:chars_to_show], fill=OSKRIS_COLORS['text'], font=font)
```

### 6. Before/After 滑块
```python
# 设计前后对比 - 适用于作品集展示
for i in range(num_frames):
    t = ease_in_out(i / (num_frames - 1))
    divider_x = int(width * t)
    frame.paste(before_img.crop((0, 0, divider_x, height)), (0, 0))
    frame.paste(after_img.crop((divider_x, 0, width, height)), (divider_x, 0))
```

## 文件大小优化

### 按用途优化
```python
# 网站加载动画（需极小）
frames[0].save('loading.gif', save_all=True, append_images=frames[1:],
    duration=66, loop=0, optimize=True)
# 目标: < 50KB

# 客户演示（质量优先）
frames[0].save('demo.gif', save_all=True, append_images=frames[1:],
    duration=66, loop=0, optimize=True)
# 目标: < 2MB

# 社交媒体（平衡质量和大小）
frames[0].save('social.gif', save_all=True, append_images=frames[1:],
    duration=100, loop=0, optimize=True)
# 目标: < 5MB
```

### 通用优化策略
1. 减少帧数: FPS 10 而非 20
2. 减少颜色: 48 色而非 256 色
3. 缩小尺寸: 按用途选择最小合适尺寸
4. 缩短时长: 加载动画 < 2秒
5. 去除重复帧: 静止部分合并

## 依赖

```bash
pip install pillow imageio numpy --break-system-packages
```
