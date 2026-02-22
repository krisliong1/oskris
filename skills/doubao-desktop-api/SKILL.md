# Doubao 桌面版 API 集成

> **重要发现**: `localhost:49853` 不是 HTTP REST API，是 WebSocket 服务器！

**版本**: Doubao 桌面版 2.0.31 (Arm64)  
**研究时间**: 2026-02-22  
**状态**: ⚠️ 本地 WebSocket 需要逆向，推荐使用替代方案

---

## 📋 执行摘要

### 核心发现

1. **本地端口 49853 = WebSocket 服务器** (不是 HTTP API)
   - 用途: App Share（应用共享功能）
   - 协议: `pbbp2` (Protobuf Binary Protocol v2)
   - 认证: 需要用户登录

2. **实际的 AI 服务**
   - 远程 WebSocket: `wss://wss100-normal.doubao.com/ws/v2`
   - 协议: 同样是 `pbbp2`
   - 用于: 对话、图片生成、思考等

3. **浏览器扩展**
   - DoubaoExtension 使用 `nativeMessaging` 与桌面应用通信
   - 可以注入网页并调用快捷指令

### 集成方案

| 方案 | 难度 | 可行性 | 推荐度 |
|------|------|--------|--------|
| 浏览器自动化 (Playwright) | 低 | ✅ 高 | ⭐⭐⭐⭐⭐ |
| 逆向 WebSocket 协议 | 高 | ⚠️ 中 | ⭐⭐ |
| Chrome Extension 劫持 | 中 | ✅ 中 | ⭐⭐⭐ |
| 网页版 API | 低 | ✅ 高 | ⭐⭐⭐⭐ |

---

## 🚀 快速开始

### 方案 1: 浏览器自动化 (推荐)

使用 Playwright 自动化 Doubao 网页版：

```javascript
const { chromium } = require('playwright');

async function askDoubao(question) {
  const browser = await chromium.launchPersistentContext(
    '/Users/openclaw/Library/Application Support/openclaw/browser/Default',
    {
      headless: false,
      channel: 'chrome'
    }
  );
  
  const page = await browser.newPage();
  await page.goto('https://www.doubao.com/chat/');
  
  // 等待登录和页面加载
  await page.waitForSelector('[data-testid="chat-input"]', { timeout: 30000 });
  
  // 输入问题
  await page.fill('[data-testid="chat-input"]', question);
  await page.press('[data-testid="chat-input"]', 'Enter');
  
  // 等待回复
  await page.waitForSelector('[data-testid="chat-message"]', { timeout: 60000 });
  
  // 提取回复
  const response = await page.locator('[data-testid="chat-message"]').last().textContent();
  
  await browser.close();
  return response;
}

// 使用
askDoubao("什么是AI?").then(console.log);
```

**优势**:
- ✅ 简单，不需要逆向协议
- ✅ 保持登录状态
- ✅ 支持所有功能（对话、图片、思考）

**劣势**:
- ❌ 需要浏览器界面（或 headless）
- ❌ 速度较慢

---

## 🔬 技术详情

### 本地 WebSocket 服务器 (localhost:49853)

```yaml
地址: ws://127.0.0.1:49853
协议: pbbp2 (Protobuf Binary Protocol v2)
用途: App Share（应用共享）
认证: 需要用户登录状态
```

**启动日志**:
```
[app_proxy] OnAvailablePort use port 49853 to start websocket server
[app_proxy] StartServerOnHandlerThread app share server websocket handler ip address: 127.0.0.1:49853
[app_proxy] OnServerStarted websocket server started
```

**未登录错误**:
```
[app_proxy] ProcessMessageOnWaitHello user not login, not support app share
[app_proxy] ReceiveMessage invalid message, close connect
```

### 远程 AI WebSocket

```yaml
地址: wss://wss100-normal.doubao.com/ws/v2
协议: pbbp2
握手协议: Sec-Websocket-Protocol: pbbp2
Ping间隔: 30秒
```

**握手响应**:
```json
{
  "Connection": "Upgrade",
  "Handshake-Msg": "OK",
  "Handshake-Options": "ping-interval=30;",
  "Handshake-Status": "0",
  "Sec-WebSocket-Accept": "...",
  "Sec-Websocket-Protocol": "pbbp2",
  "Upgrade": "websocket"
}
```

---

## 💡 高级方案

### 方案 2: 逆向 WebSocket 协议

**步骤**:

1. **抓包捕获 WebSocket 消息**
   ```bash
   # 使用 Wireshark 或 Charles Proxy
   # 过滤器: tcp.port == 49853 || tcp.port == 443
   ```

2. **分析 pbbp2 协议**
   - Protobuf 二进制格式
   - 需要找到 .proto 定义文件
   - 或者逆向解码

3. **实现客户端**
   ```python
   import websocket
   import struct
   
   def connect_to_doubao():
       ws = websocket.create_connection("ws://127.0.0.1:49853")
       # 发送登录消息（需要逆向格式）
       # ws.send(login_message)
       # ...
   ```

**挑战**:
- pbbp2 是私有协议，没有公开文档
- 需要分析二进制消息格式
- 需要处理认证

### 方案 3: Chrome Extension 劫持

**思路**: 注入脚本拦截 Doubao Extension 的消息

```javascript
// content.js
window.addEventListener('message', (event) => {
  if (event.source === window && event.data.type === 'DOUBAO_REQUEST') {
    // 劫持 Doubao 的请求
    console.log('Doubao request:', event.data);
    
    // 转发到我们的服务器
    fetch('http://localhost:3000/doubao-proxy', {
      method: 'POST',
      body: JSON.stringify(event.data)
    });
  }
});
```

**扩展配置**:
```json
{
  "manifest_version": 3,
  "name": "Doubao API Interceptor",
  "permissions": ["storage", "webRequest"],
  "content_scripts": [{
    "matches": ["https://www.doubao.com/*"],
    "js": ["content.js"]
  }]
}
```

---

## 📂 架构图

```
┌─────────────────────────────────────────────────┐
│         Doubao 桌面应用 (2.0.31)                 │
│         基于 Chromium 135.0.7049.72             │
└─────────────┬───────────────────────────────────┘
              │
              ├─► 本地 WebSocket 服务器
              │   ws://127.0.0.1:49853
              │   ├─ 用途: App Share
              │   ├─ 协议: pbbp2
              │   └─ 认证: ✅ 需要登录
              │
              ├─► 远程 AI WebSocket
              │   wss://wss100-normal.doubao.com/ws/v2
              │   ├─ 用途: AI 对话/图片生成
              │   ├─ 协议: pbbp2
              │   └─ 认证: ✅ 需要 Cookie/Token
              │
              └─► DoubaoExtension (浏览器扩展)
                  ├─ nativeMessaging 与桌面应用通信
                  ├─ 注入网页内容
                  └─ 快捷指令触发
```

---

## 🧪 测试脚本

### 测试 1: 验证端口可用性

```bash
#!/bin/bash
# test-doubao-port.sh

echo "Testing Doubao local port..."
nc -z 127.0.0.1 49853

if [ $? -eq 0 ]; then
    echo "✅ Port 49853 is open"
else
    echo "❌ Port 49853 is not available"
    echo "Please ensure Doubao desktop app is running"
    exit 1
fi

echo ""
echo "Testing WebSocket connection..."
# 需要安装: npm install -g wscat
wscat -c ws://127.0.0.1:49853 2>&1 | head -5
```

### 测试 2: Playwright 自动化示例

```javascript
// test-doubao-automation.js
const { chromium } = require('playwright');

async function testDoubao() {
  console.log('🚀 Starting Doubao automation test...');
  
  const userDataDir = '/Users/openclaw/Library/Application Support/openclaw/browser/Default';
  const browser = await chromium.launchPersistentContext(userDataDir, {
    headless: false,
    channel: 'chrome'
  });
  
  try {
    const page = await browser.newPage();
    
    console.log('📖 Navigating to Doubao...');
    await page.goto('https://www.doubao.com/chat/');
    
    console.log('⏳ Waiting for chat interface...');
    await page.waitForSelector('textarea', { timeout: 30000 });
    
    console.log('✍️ Typing question...');
    const question = '用一句话解释AI是什么';
    await page.fill('textarea', question);
    await page.press('textarea', 'Enter');
    
    console.log('⏳ Waiting for response...');
    await page.waitForTimeout(5000);
    
    console.log('✅ Test completed!');
    
    // 截图
    await page.screenshot({ path: 'doubao-test.png' });
    console.log('📸 Screenshot saved: doubao-test.png');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    await browser.close();
  }
}

testDoubao();
```

**运行**:
```bash
npm install playwright
node test-doubao-automation.js
```

---

## 🗂️ 关键文件位置

### 日志文件
```
~/Library/Application Support/Doubao/sdk_storage/log/
├── saman_*.log           # 主日志（包含 WebSocket 信息）
├── saman_netlog_*.log    # 网络日志
└── netmain-*.alaudalog   # 网络详细日志
```

### 配置文件
```
~/Library/Application Support/Doubao/Default/
├── Preferences           # 用户偏好设置
├── Cookies              # Cookie 数据库
└── Local Extension Settings/  # 扩展配置
```

### 扩展文件
```
/Applications/DoubaoExtension.app/Contents/PlugIns/
└── DoubaoExtension Extension.appex/Contents/Resources/
    ├── manifest.json              # 扩展配置
    ├── static/js/content.js       # 内容脚本
    ├── static/js/background.js    # 后台脚本
    └── configs/                   # 配置文件
```

### 应用文件
```
/Applications/Doubao 2.app/
├── Contents/Resources/manifest.json  # 应用配置
└── Contents/Helpers/Doubao Browser.app/  # Chromium 浏览器
```

---

## ⚠️ 已知限制

### 本地 WebSocket (49853)

1. **不是公开 API**
   - 私有协议，无官方文档
   - 主要用于内部应用间通信

2. **需要登录**
   - 未登录会被拒绝连接
   - 需要有效的用户 session

3. **协议复杂**
   - pbbp2 是二进制 Protobuf 协议
   - 消息格式未公开
   - 需要大量逆向工作

### 远程 WebSocket

1. **需要认证 Token**
   - Cookie 中的 session token
   - 可能有过期时间

2. **协议同样复杂**
   - 同样使用 pbbp2
   - 需要构造正确的 Protobuf 消息

3. **可能有速率限制**
   - 防滥用机制
   - IP 或账号级别限制

---

## 🎯 推荐实践

### ✅ 推荐做法

1. **使用浏览器自动化 (Playwright/Puppeteer)**
   - 简单、稳定、功能完整
   - 保持登录状态
   - 支持所有功能

2. **使用 Doubao 网页版 API**
   - 如果存在公开 API endpoint
   - 使用开发者工具分析网页请求
   - 模拟 HTTP 请求

3. **使用官方 API（如果有）**
   - 联系 Doubao 官方咨询 API
   - 申请开发者账号
   - 使用官方 SDK

### ❌ 不推荐做法

1. **硬破解本地 WebSocket**
   - 耗时长，维护成本高
   - 每次更新可能失效
   - 可能违反服务条款

2. **注入恶意代码**
   - 安全风险
   - 违反使用协议
   - 可能被封号

---

## 🔮 未来方向

### 短期

1. **完善浏览器自动化脚本**
   - 支持更多功能（图片生成、文件上传）
   - 错误处理和重试机制
   - 并发请求支持

2. **监控 Doubao 更新**
   - 是否会推出官方 API
   - 协议是否有变化

### 中期

1. **尝试逆向 pbbp2 协议**
   - 如果有需求和时间
   - 建立协议文档
   - 开发 Python/Node.js 客户端

2. **研究其他 AI 平台 API**
   - Kimi、ChatGPT、Claude 等
   - 对比集成难度
   - 建立统一接口

### 长期

1. **开发统一 AI Gateway**
   - 支持多个 AI 平台
   - 统一的 REST API
   - 负载均衡和故障转移

---

## 📚 参考资料

### 相关技术

- [WebSocket Protocol (RFC 6455)](https://datatracker.ietf.org/doc/html/rfc6455)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)
- [Playwright Documentation](https://playwright.dev/)
- [Chrome Extension Manifest V3](https://developer.chrome.com/docs/extensions/mv3/)

### Doubao 资源

- 官网: https://www.doubao.com/
- 网页版: https://www.doubao.com/chat/
- 浏览器扩展: DoubaoExtension.app

### 相关 Skills

- `doubao-chrome-extension` - 豆包 Chrome 扩展深度研究
- `browser-automation` - 浏览器自动化最佳实践
- `websocket-reverse-engineering` - WebSocket 协议逆向

---

## 🤝 贡献

**研究员**: Research AI (第7层)  
**日期**: 2026-02-22  
**版本**: 1.0.0  

**鸣谢**:
- macOS Automation Specialist - 发现了 49853 端口
- 主 Agent - 提出研究需求

---

## 📝 更新日志

### v1.0.0 (2026-02-22)

- ✅ 识别本地端口为 WebSocket 服务器
- ✅ 分析日志文件获取协议信息
- ✅ 提供浏览器自动化方案
- ✅ 创建测试脚本
- ✅ 记录完整的技术架构

---

**结论**: Doubao 桌面版 localhost:49853 **不适合直接作为 AI API 使用**。推荐使用 **浏览器自动化** 或等待官方 API。

如需帮助，请查看测试脚本或联系 Research AI。🤖
