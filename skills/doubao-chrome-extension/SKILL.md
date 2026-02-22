# Doubao Chrome Extension - 豆包扩展生态系统指南

> **Skill文档** | 创建时间: 2024-02-21 | 研究员: Research AI  
> **用途**: AI agents自动化集成豆包Chrome扩展

---

## 📋 执行摘要

豆包（Doubao）是字节跳动的AI助手平台，拥有丰富的Chrome扩展生态系统。本文档汇总了豆包扩展的功能、自动化方法和AI agents集成方案。

**关键发现**：
- 🔧 豆包有活跃的第三方扩展生态（去水印、公式导出、批量处理等）
- 🤖 扩展主要通过DOM操作、Fetch API劫持与豆包网页交互
- 🎯 AutoDoubao扩展支持批量prompt发送和自动下载
- ⚠️ 官方API尚未确认，自动化主要依赖扩展和脚本

---

## 🎯 功能清单

### 官方豆包功能
- [ ] **对话助手** - 文本对话、代码生成
- [ ] **图片生成** - AI绘图（带水印）
- [ ] **文档处理** - 文本分析、总结
- [ ] **快捷指令浮标** - ❓待验证（宝提到的功能）

### 已验证的第三方扩展

#### 1. 豆包去水印（v1.5.0）
**功能**: 自动捕获图片下载请求，合成去水印图片

**技术原理**:
```javascript
// 劫持fetch API监听图片下载
window.fetch = async function(...args) {
    const url = typeof args[0] === 'string' ? args[0] : (args[0] && args[0].url);
    if (url && url.includes('image_dld_watermark')) {
        // 获取原图上半部分 + 水印图下半部分
        // 合成完整去水印图片
    }
    return originalFetch.apply(this, args);
};
```

**关键文件**:
- Manifest: `/Users/openclaw/.openclaw/browser/openclaw/user-data/Default/Extensions/dnoflfkdnjfpgfbkngdoblpgbcbodnmo/1.5.0_0/manifest.json`
- 注入脚本: `injected.js` - Fetch API劫持
- 通信: Custom Events (`DOUBAO_FETCH_CAPTURED`, `DOUBAO_DOWNLOAD_MERGED`)

#### 2. 豆包数学公式导出Word（v1.2.5）
**功能**: 一键导出数学/物理/化学公式为Word文档

**权限**: `clipboardRead`, `storage`  
**API**: 调用 `api.aiwhaler.com` 进行转换

**集成点**:
```json
{
  "content_scripts": [{
    "js": ["content.js"],
    "matches": ["https://www.doubao.com/*"],
    "run_at": "document_end"
  }]
}
```

#### 3. Kimi/豆包会话助手（v1.0.3）
**功能**: 显示会话中所有问题并支持快速跳转

**多平台**: 同时支持Kimi和豆包  
**无权限**: 纯DOM操作，无特殊权限需求

#### 4. AutoDoubao（Chrome Web Store）
**功能**: 
- ✅ 批量自动发送prompt
- ✅ 自动排队处理
- ✅ 自动下载生成的图片

**状态**: 未安装，需进一步测试

---

## 🔧 AI Agents集成方案

### 方案A: Chrome扩展自动化（推荐）

适用于需要与豆包网页深度交互的场景。

#### 前置条件
1. 安装Chrome/Chromium
2. 安装目标扩展（如AutoDoubao）
3. 使用Puppeteer/Playwright控制浏览器

#### 实现步骤

```javascript
// 使用Playwright控制豆包扩展
const { chromium } = require('playwright');

async function automateDoubao() {
    // 1. 启动浏览器（加载已安装的扩展）
    const userDataDir = '/Users/openclaw/.openclaw/browser/openclaw/user-data';
    const browser = await chromium.launchPersistentContext(userDataDir, {
        headless: false,
        args: [
            '--disable-blink-features=AutomationControlled'
        ]
    });
    
    // 2. 打开豆包网站
    const page = await browser.newPage();
    await page.goto('https://www.doubao.com/chat/');
    
    // 3. 等待页面加载
    await page.waitForSelector('textarea[placeholder*="输入"]', { timeout: 10000 });
    
    // 4. 发送prompt
    await page.fill('textarea', '生成一张日落海滩的图片');
    await page.keyboard.press('Enter');
    
    // 5. 等待图片生成（监听DOM变化）
    await page.waitForSelector('img[src*="doubao"]', { timeout: 60000 });
    
    // 6. 触发下载（如果安装了去水印扩展，会自动处理）
    const downloadButton = await page.locator('button:has-text("下载")');
    await downloadButton.click();
    
    // 7. 等待下载完成
    await page.waitForTimeout(3000);
    
    await browser.close();
}
```

### 方案B: Fetch API拦截（高级）

直接在网页上下文注入脚本，劫持API调用。

```javascript
// 注入到豆包页面的脚本
(function() {
    const originalFetch = window.fetch;
    
    window.fetch = async function(...args) {
        const url = args[0];
        
        // 拦截图片生成请求
        if (url && url.includes('/api/generate_image')) {
            console.log('📸 拦截到图片生成请求');
            const response = await originalFetch.apply(this, args);
            const clone = response.clone();
            const data = await clone.json();
            
            // 通知外部脚本
            window.postMessage({
                type: 'DOUBAO_IMAGE_GENERATED',
                imageUrl: data.image_url
            }, '*');
            
            return response;
        }
        
        return originalFetch.apply(this, args);
    };
})();
```

### 方案C: 命令行接口（如果官方API可用）

```bash
# 假设豆包提供CLI或API
# 需要验证此方法是否可行

# 生成图片
curl -X POST https://api.doubao.com/v1/images/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "prompt": "日落海滩",
    "size": "1024x1024"
  }'

# 或使用官方CLI（如果存在）
doubao generate --prompt "日落海滩" --output ./image.png
```

**状态**: ❓ 待验证 - 豆包官方API文档未找到

---

## 🎨 图片生成自动化完整流程

### 目标
AI agents自动调用豆包生成图片，无需人工干预。

### 步骤

#### 1. 环境准备
```bash
# 安装Node.js依赖
npm install playwright

# 或使用Python
pip install playwright
playwright install chromium
```

#### 2. 创建自动化脚本
```bash
mkdir -p ~/.openclaw/workspace/scripts/doubao-automation
cd ~/.openclaw/workspace/scripts/doubao-automation
```

创建 `generate-image.js`:
```javascript
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function generateImage(prompt, outputPath) {
    const userDataDir = path.join(process.env.HOME, '.openclaw/browser/openclaw/user-data');
    
    const browser = await chromium.launchPersistentContext(userDataDir, {
        headless: false,
        downloadsPath: path.dirname(outputPath)
    });
    
    const page = await browser.newPage();
    
    try {
        // 1. 导航到豆包
        await page.goto('https://www.doubao.com/chat/', { waitUntil: 'networkidle' });
        
        // 2. 找到输入框并发送prompt
        const textarea = await page.waitForSelector('textarea', { timeout: 10000 });
        await textarea.fill(prompt);
        await page.keyboard.press('Enter');
        
        // 3. 等待图片生成
        console.log('⏳ 等待图片生成...');
        await page.waitForSelector('img[src*="image"]', { timeout: 120000 });
        
        // 4. 等待去水印扩展处理（如果已安装）
        await page.waitForTimeout(2000);
        
        // 5. 查找并点击下载按钮
        const downloadBtn = await page.locator('button:has-text("下载"), svg[class*="download"]').first();
        
        // 监听下载事件
        const downloadPromise = page.waitForEvent('download');
        await downloadBtn.click();
        const download = await downloadPromise;
        
        // 6. 保存文件
        await download.saveAs(outputPath);
        console.log(`✅ 图片已保存: ${outputPath}`);
        
        return { success: true, path: outputPath };
        
    } catch (error) {
        console.error('❌ 生成失败:', error);
        return { success: false, error: error.message };
        
    } finally {
        await browser.close();
    }
}

// 命令行接口
if (require.main === module) {
    const prompt = process.argv[2] || '美丽的日落';
    const outputPath = process.argv[3] || './doubao-output.png';
    
    generateImage(prompt, outputPath)
        .then(result => {
            if (result.success) {
                console.log(`\n🎨 图片生成成功！`);
                console.log(`📁 保存位置: ${result.path}`);
                process.exit(0);
            } else {
                console.error(`\n❌ 生成失败: ${result.error}`);
                process.exit(1);
            }
        });
}

module.exports = { generateImage };
```

#### 3. 使用示例
```bash
# 直接调用脚本
node generate-image.js "梦幻森林中的小屋" ./output.png

# 从OpenClaw agents调用
# 在任务中执行：
exec("node ~/.openclaw/workspace/scripts/doubao-automation/generate-image.js '日落海滩' /tmp/beach.png")
```

---

## 📚 扩展开发参考

### Manifest V3结构
所有现代豆包扩展都使用Manifest V3：

```json
{
  "manifest_version": 3,
  "name": "豆包助手扩展",
  "version": "1.0.0",
  "description": "增强豆包功能",
  
  "permissions": [
    "activeTab",
    "storage",
    "downloads"
  ],
  
  "host_permissions": [
    "https://*.doubao.com/*"
  ],
  
  "content_scripts": [{
    "matches": ["https://*.doubao.com/*"],
    "js": ["content.js"],
    "run_at": "document_start"
  }],
  
  "background": {
    "service_worker": "background.js"
  }
}
```

### 注入脚本模式
```javascript
// content.js - 注入主world脚本
const script = document.createElement('script');
script.src = chrome.runtime.getURL('injected.js');
(document.head || document.documentElement).appendChild(script);

// 监听injected.js发出的事件
window.addEventListener('DOUBAO_EVENT', (event) => {
    // 转发到background.js
    chrome.runtime.sendMessage({
        type: 'EVENT',
        data: event.detail
    });
});
```

---

## 🚨 已知限制和注意事项

### 限制
1. **无官方API** - 豆包未提供官方Chrome Extension API或REST API
2. **依赖DOM结构** - 页面改版可能导致脚本失效
3. **需要登录** - 自动化脚本需要保持登录状态
4. **速率限制** - 批量请求可能触发反爬机制
5. **水印问题** - 官方图片带水印，需要第三方扩展处理

### 最佳实践
- ✅ 使用持久化用户数据目录（保持登录状态）
- ✅ 添加合理的等待时间（避免检测）
- ✅ 监听DOM变化而非固定延迟
- ✅ 使用去水印扩展自动处理下载
- ✅ 捕获所有错误并记录日志
- ⚠️ 避免高频请求（遵守使用条款）

---

## 🧪 测试清单（需要人工验证）

### Phase 1: 快捷指令功能验证
- [ ] 打开豆包网站（https://www.doubao.com/chat/）
- [ ] 查找页面上是否有"浮标"或"快捷按钮"
- [ ] 测试浮标能做什么（图片生成？对话？其他？）
- [ ] 确认是否可以通过脚本触发

### Phase 2: 扩展功能测试
- [ ] 安装AutoDoubao扩展
- [ ] 测试批量prompt发送
- [ ] 测试自动队列处理
- [ ] 测试自动下载功能
- [ ] 记录触发方式和API调用

### Phase 3: 自动化集成测试
- [ ] 运行上述Playwright脚本
- [ ] 验证图片是否成功生成
- [ ] 验证去水印是否自动触发
- [ ] 测试不同prompt的成功率

---

## 📖 参考资料

### 已安装扩展路径
```
豆包去水印: 
/Users/openclaw/.openclaw/browser/openclaw/user-data/Default/Extensions/dnoflfkdnjfpgfbkngdoblpgbcbodnmo/1.5.0_0/

豆包数学公式导出:
/Users/openclaw/.openclaw/browser/openclaw/user-data/Default/Extensions/ohalkmdcakplbfpelgmnegcbdkfigolo/1.2.5_0/

Kimi/豆包会话助手:
/Users/openclaw/.openclaw/browser/openclaw/user-data/Default/Extensions/mainaomjpdphhfpgeklfcnnjhmbdaabf/1.0.3_0/
```

### 相关链接
- 豆包官网: https://www.doubao.com
- Chrome Web Store（豆包扩展搜索）: https://chromewebstore.google.com/search/豆包
- ❓ 官方API文档: 未找到
- ❓ 开发者文档: 待确认

### 技术栈
- **Chrome Extension Manifest V3**
- **Playwright / Puppeteer** - 浏览器自动化
- **Fetch API Interception** - 网络请求劫持
- **Custom Events** - 扩展间通信
- **Canvas API** - 图像处理

---

## 🎓 学习要点（供AI agents参考）

1. **扩展生态理解** - 豆包主要通过第三方扩展增强功能
2. **自动化策略** - 使用浏览器自动化工具（Playwright）是最可靠的方法
3. **DOM观察** - 不要依赖固定延迟，监听实际的DOM变化
4. **状态管理** - 使用持久化浏览器上下文保持登录
5. **错误处理** - 豆包页面可能变化，需要robust的错误处理

---

## 📝 更新日志

**2024-02-21** - Research AI
- ✅ 初始文档创建
- ✅ 分析4个已安装扩展
- ✅ 提供Playwright自动化方案
- ✅ 创建完整图片生成流程
- ⏳ 待验证：快捷指令浮标功能
- ⏳ 待验证：官方API可用性
- ⏳ 待测试：AutoDoubao扩展功能

**下次更新重点**：
1. 验证快捷指令浮标是什么
2. 测试AutoDoubao批量功能
3. 补充官方API文档（如果存在）

---

*本文档由Research AI创建，供AI Team使用。如有新发现请及时更新。*
