# Doubao 桌面版 API 集成

**重要发现**: Doubao 桌面版的 `localhost:49853` 是 WebSocket 服务器，不是 HTTP REST API！

---

## 📖 快速开始

### 1. 浏览器自动化（推荐）

```bash
# 安装依赖
npm install playwright

# 运行测试
node test-automation.js

# 提问单个问题
node test-automation.js "什么是AI?"

# 生成图片
node test-automation.js --image "一只可爱的猫咪"
```

### 2. WebSocket 测试

```bash
# 安装依赖
npm install ws

# 测试连接
node test-websocket.js

# 分析消息（Hex格式）
node test-websocket.js --analyze "0801120474657374"
```

---

## 🎯 主要发现

### 端口 49853 = WebSocket 服务器

- **协议**: `pbbp2` (Protobuf Binary Protocol v2)
- **用途**: App Share（应用共享）
- **认证**: 需要用户登录

### 实际的 AI 服务

- **地址**: `wss://wss100-normal.doubao.com/ws/v2`
- **用途**: AI 对话、图片生成等

---

## 📂 文件说明

```
doubao-desktop-api/
├── SKILL.md                 # 完整文档（技术细节、架构图）
├── README.md               # 本文件（快速开始）
├── test-automation.js      # Playwright 自动化脚本
└── test-websocket.js       # WebSocket 测试脚本
```

---

## 🔧 使用示例

### JavaScript API

```javascript
const { askDoubao } = require('./test-automation.js');

// 提问
const answer = await askDoubao("用一句话解释AI");
console.log(answer);

// 批量提问
const { askMultiple } = require('./test-automation.js');
const results = await askMultiple([
  "什么是AI?",
  "写一个Hello World",
  "今天几号?"
]);
```

### 命令行

```bash
# 单个问题
node test-automation.js "用Python写一个斐波那契函数"

# 默认测试（3个问题）
node test-automation.js

# 图片生成
node test-automation.js --image "赛博朋克风格的城市"
```

---

## ⚠️ 重要提示

### ✅ 可以做的

- 使用 Playwright 自动化网页版
- 研究 WebSocket 协议（学习用途）
- 使用官方网页界面

### ❌ 不推荐做的

- 直接用 curl 调用 localhost:49853（会失败）
- 破解 pbbp2 协议用于生产环境
- 违反服务条款的操作

---

## 🚀 下一步

1. **阅读 SKILL.md** - 了解完整技术细节
2. **运行测试脚本** - 验证功能
3. **根据需求选择方案**:
   - 简单使用 → 浏览器自动化
   - 研究协议 → WebSocket 测试
   - 生产环境 → 等待官方 API

---

## 📚 更多资料

- [完整文档](SKILL.md) - 技术架构、协议分析
- [Playwright 官方文档](https://playwright.dev/)
- [WebSocket RFC](https://datatracker.ietf.org/doc/html/rfc6455)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)

---

**作者**: Research AI  
**日期**: 2026-02-22  
**版本**: 1.0.0
