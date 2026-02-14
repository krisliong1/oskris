# Design Enhancement Skill
## 专业网站设计感提升指南

### 触发条件
当用户需要以下任何内容时使用此skill:
- 为网站添加专业动画效果
- 提升网站整体设计感和视觉质量
- 实现小众但高质量的设计风格
- 添加微交互和流畅过渡效果
- 使用GSAP动画库
- 创建正式且有动画的专业网站

---

## 核心设计原则

### 1. 视觉设计哲学
**克制但精致的美学**
- 配色方案: 2-3种主色调(通常黑白灰 + 1个品牌色)
- 字体选择: 专业无衬线字体(Inter, SF Pro, Helvetica, Roboto)
- 图片尺寸: 适中合理,避免全屏巨图
- 留白运用: 充足但不过分,保持呼吸感
- 模块化布局: 清晰的网格系统,一致的间距

**高级感特征**
- 简洁的布局
- 高质量但克制的视觉元素
- 精致的细节处理
- 专业的色彩搭配
- 优雅的动画过渡

### 2. 动画设计规范

**适度原则**
- 动画是辅助,不是主角
- 每个动画都应有明确的目的
- 避免过度或花哨的效果
- 保持性能和流畅度

**推荐的动画类型**
1. **微交互** - 按钮悬停时的颜色/阴影变化
2. **滚动动画** - 内容随滚动淡入/滑入
3. **图标动效** - 悬停时轻微缩放(1.05-1.1倍)
4. **平滑过渡** - 页面切换时的淡入淡出
5. **数字滚动** - 统计数据的动态计数
6. **视差效果** - 背景与前景不同速度移动
7. **加载动画** - 精致的loading效果

---

## GSAP 动画库使用指南

### 安装方式

**NPM安装** (推荐用于构建工具)
```bash
npm install gsap
```

**CDN引入** (快速原型)
```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
```

**常用插件**
```javascript
// 注册插件
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ScrollSmoother } from "gsap/ScrollSmoother";

gsap.registerPlugin(ScrollTrigger, ScrollSmoother);
```

### 基础动画语法

**1. gsap.to() - 最常用的动画方法**
从当前状态动画到目标状态
```javascript
// 基础示例
gsap.to(".box", {
  x: 200,           // 向右移动200px
  rotation: 360,    // 旋转360度
  duration: 2,      // 持续2秒
  ease: "power2.out" // 缓动函数
});

// 专业网站常用效果
gsap.to(".card", {
  y: -10,           // 悬停上浮
  boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
  duration: 0.3,
  ease: "power1.out"
});
```

**2. gsap.from() - 入场动画**
从指定状态动画到当前状态
```javascript
// 元素淡入
gsap.from(".hero-text", {
  opacity: 0,
  y: 50,
  duration: 1,
  ease: "power2.out"
});
```

**3. gsap.fromTo() - 完全控制**
同时指定起始和结束状态
```javascript
gsap.fromTo(".button", 
  { scale: 1 },           // 起始状态
  { 
    scale: 1.05,          // 结束状态
    duration: 0.2,
    ease: "power1.inOut"
  }
);
```

### 实用动画模式

**1. 滚动触发动画 (ScrollTrigger)**
```javascript
gsap.registerPlugin(ScrollTrigger);

// 元素进入视口时淡入
gsap.from(".feature-card", {
  scrollTrigger: {
    trigger: ".feature-card",
    start: "top 80%",      // 当元素顶部到达视口80%位置时触发
    toggleActions: "play none none reverse"
  },
  opacity: 0,
  y: 30,
  duration: 0.8,
  stagger: 0.2            // 多个元素依次动画,间隔0.2秒
});
```

**2. 悬停动画**
```javascript
// 鼠标悬停效果
document.querySelectorAll('.project-card').forEach(card => {
  card.addEventListener('mouseenter', () => {
    gsap.to(card, {
      y: -8,
      boxShadow: "0 20px 40px rgba(0,0,0,0.15)",
      duration: 0.3,
      ease: "power2.out"
    });
  });
  
  card.addEventListener('mouseleave', () => {
    gsap.to(card, {
      y: 0,
      boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
      duration: 0.3,
      ease: "power2.out"
    });
  });
});
```

**3. 时间轴动画 (Timeline)**
用于组合多个动画
```javascript
const tl = gsap.timeline();

tl.from(".logo", { opacity: 0, y: -20, duration: 0.6 })
  .from(".nav-item", { opacity: 0, y: -10, stagger: 0.1 }, "-=0.3")
  .from(".hero-title", { opacity: 0, y: 30, duration: 0.8 }, "-=0.2");
```

**4. 平滑滚动 (ScrollSmoother)**
```javascript
gsap.registerPlugin(ScrollSmoother);

ScrollSmoother.create({
  smooth: 1.5,              // 平滑度
  effects: true,            // 启用视差效果
  smoothTouch: 0.1          // 移动端平滑度
});
```

### 性能优化建议

**1. 优先使用transform和opacity**
```javascript
// ✅ 推荐 - GPU加速
gsap.to(".element", { x: 100, scale: 1.2, opacity: 0.5 });

// ❌ 避免 - 触发重排
gsap.to(".element", { left: "100px", width: "200px" });
```

**2. 使用will-change提示浏览器**
```css
.animated-element {
  will-change: transform, opacity;
}
```

**3. 控制动画数量**
- 同时运行的复杂动画不超过5个
- 使用懒加载延迟非关键动画
- 在移动设备上减少或禁用某些动画

---

## 专业网站设计模式

### 1. 首页设计结构
```
- Hero区域
  - 简洁的标语 (淡入动画)
  - 一句话介绍 (延迟淡入)
  - CTA按钮 (微妙的脉动或悬停效果)
  
- 精选作品/服务
  - 网格布局 (2-3列)
  - 卡片式设计
  - 悬停效果: 轻微上浮 + 阴影加深
  
- 关于/价值主张
  - 分栏布局
  - 图标 + 简短说明
  - 滚动触发的淡入效果
  
- 联系方式/CTA
  - 简洁表单或联系按钮
  - 清晰的行动号召
```

### 2. 卡片悬停效果示例
```javascript
// HTML
<div class="project-card">
  <img src="project-thumbnail.jpg" alt="项目">
  <h3>项目名称</h3>
  <p>简短描述</p>
</div>

// CSS
.project-card {
  transition: transform 0.3s ease;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

// JavaScript (GSAP)
const cards = gsap.utils.toArray('.project-card');

cards.forEach(card => {
  const image = card.querySelector('img');
  
  card.addEventListener('mouseenter', () => {
    gsap.to(card, { y: -10, duration: 0.3 });
    gsap.to(image, { scale: 1.05, duration: 0.5 });
  });
  
  card.addEventListener('mouseleave', () => {
    gsap.to(card, { y: 0, duration: 0.3 });
    gsap.to(image, { scale: 1, duration: 0.5 });
  });
});
```

### 3. 页面加载动画
```javascript
// 页面加载完成后的入场动画
window.addEventListener('load', () => {
  const tl = gsap.timeline();
  
  tl.from('.logo', { 
    opacity: 0, 
    y: -20, 
    duration: 0.6,
    ease: "power2.out"
  })
  .from('.nav-item', { 
    opacity: 0, 
    y: -10, 
    stagger: 0.1,
    duration: 0.4
  }, "-=0.3")
  .from('.hero-content', { 
    opacity: 0, 
    y: 30, 
    duration: 0.8 
  }, "-=0.2");
});
```

---

## 小众高质量设计参考

### 推荐研究的工作室
1. **Waaark** (waaark.com) - 法国精品工作室,极简但功能性强
2. **Zajno** (zajno.com) - 国际精品设计,流畅GSAP动画
3. **Louis Ansa** - 干净作品展示,优雅slider
4. **Les Animals** - 全屏设计,精致过渡

### 灵感来源平台
- **minimal.gallery** - 极简风格网站收集
- **Godly.website** - 小众设计工作室精选
- **SiteInspire** - 可按风格筛选
- **Awwwards** - 筛选"minimal"或"studio"类别

---

## 技术栈建议

### 快速开发工具
1. **Webflow** - 无代码但能实现高级动画
2. **Framer** - 交互原型直接转网站
3. **Custom Code** - HTML + CSS + GSAP (最灵活)

### 开发流程
1. 在Figma设计原型
2. 确定关键动画点
3. 使用GSAP实现动画
4. 测试性能和兼容性
5. 优化加载速度

---

## 常见动画效果代码片段

### 1. 淡入淡出导航
```javascript
gsap.from(".nav", {
  opacity: 0,
  y: -20,
  duration: 0.6,
  ease: "power2.out",
  delay: 0.2
});
```

### 2. 文字逐字出现
```javascript
gsap.from(".title span", {
  opacity: 0,
  y: 20,
  stagger: 0.05,
  duration: 0.4,
  ease: "back.out"
});
```

### 3. 视差背景
```javascript
gsap.to(".parallax-bg", {
  scrollTrigger: {
    trigger: ".section",
    scrub: true
  },
  y: (i, target) => -ScrollTrigger.maxScroll(window) * target.dataset.speed
});
```

### 4. 数字计数动画
```javascript
gsap.to(".counter", {
  textContent: 1000,
  duration: 2,
  ease: "power1.inOut",
  snap: { textContent: 1 },
  scrollTrigger: {
    trigger: ".counter",
    start: "top 80%"
  }
});
```

---

## 最佳实践清单

### 设计层面
- [ ] 使用2-3种主色调
- [ ] 选择专业字体(最多2种字体家族)
- [ ] 保持一致的间距系统(8px或16px倍数)
- [ ] 图片质量高但尺寸适中
- [ ] 充足的留白和呼吸空间

### 动画层面
- [ ] 每个动画都有明确目的
- [ ] 持续时间0.2-0.8秒(大部分情况)
- [ ] 使用合适的缓动函数(ease)
- [ ] 避免同时运行过多动画
- [ ] 移动端考虑性能,减少复杂动画

### 技术层面
- [ ] 优先使用transform和opacity
- [ ] 注册所有使用的GSAP插件
- [ ] 测试多种设备和浏览器
- [ ] 压缩和优化资源文件
- [ ] 实现渐进增强(无JS时仍可用)

---

## 参考资源

### GSAP官方资源
- 文档: https://gsap.com/docs/v3/
- 安装指南: https://gsap.com/docs/v3/Installation
- 基础教程: https://gsap.com/resources/get-started/
- 示例库: https://gsap.com/showcase/
- CodePen示例: https://codepen.io/GreenSock

### 学习资源
- GSAP YouTube频道: https://www.youtube.com/@GreenSockLearning
- Made With GSAP: https://madewithgsap.com/ (50+效果示例)
- FreeCodeCamp GSAP教程

### 性能优化
- 使用Chrome DevTools Performance面板
- 监控FPS保持在60fps
- 使用Lighthouse检测性能问题

---

## 工作流程建议

### 1. 设计阶段
1. 研究参考网站,截图保存喜欢的细节
2. 在Figma创建设计稿
3. 标注需要动画的元素
4. 制作简单的动画原型

### 2. 开发阶段
1. 搭建HTML结构
2. 编写基础CSS样式
3. 添加GSAP动画
4. 测试和优化
5. 跨浏览器测试

### 3. 优化阶段
1. 压缩图片和资源
2. 最小化CSS/JS文件
3. 实现懒加载
4. 添加loading状态
5. 移动端适配

---

## 关键提醒

⚠️ **永远记住**:
- 设计感来自克制和精致,而非堆砌效果
- 动画应该增强用户体验,而非分散注意力
- 性能永远比炫技重要
- 小众不等于小气,要保持专业水准
- 测试,测试,再测试 - 在真实设备上验证效果

💡 **设计哲学**:
好的设计是看不见的设计,
好的动画是让用户感觉流畅而非察觉到动画本身。

---

当用户需要提升网站设计感时,始终:
1. 先确认他们想要的风格(小众/专业/极简等)
2. 推荐合适的参考案例
3. 提供GSAP实现代码
4. 强调性能和用户体验
5. 给出完整的实现建议
