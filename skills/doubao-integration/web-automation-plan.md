# 豆包Web自动化测试计划

## 目标
先用免费的Web版测试豆包，收集数据后再决定是否需要付费API。

## 豆包网址
- 主站: https://www.doubao.com
- 聊天: https://www.doubao.com/chat/

## Phase 1: 手动测试（优先）

### 你可以帮我做的：
1. 用浏览器访问 https://www.doubao.com/chat/
2. 测试几个问题：
   - "你好，请介绍一下你自己"
   - "写一个Python脚本检查文件夹大小"
   - "帮我整理这些文件：report.pdf, photo.jpg, code.js"
   - "用中文解释什么是API"

3. 收集数据：
   - ⏱️ 响应速度（秒）
   - 📝 回答质量（1-10分）
   - 💬 对话是否流畅
   - ⚠️ 有没有限制（次数/长度）
   - 🔐 是否需要登录

## Phase 2: 自动化方案（如果值得）

### 方案A: Playwright/Puppeteer
```javascript
// 伪代码
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('https://www.doubao.com/chat/');

// 找到输入框
const input = await page.locator('textarea');
await input.fill('你好');

// 点击发送
const send = await page.locator('button:has-text("发送")');
await send.click();

// 等待回复
const response = await page.locator('.message-bot').last();
```

### 方案B: OpenClaw Browser工具
```bash
# 需要Chrome扩展连接
browser open https://www.doubao.com/chat/
browser snapshot  # 查看页面结构
browser act type "你好" into input
browser act click "发送"
browser snapshot  # 获取回复
```

### 方案C: 简单的HTTP请求抓包
1. 打开浏览器开发者工具
2. 发送一条消息
3. 查看Network请求
4. 找到API endpoint
5. 直接用curl模拟（可能更简单）

## Phase 3: 决策标准

### 继续用Web版的条件：
- ✅ 免费无限制
- ✅ 响应速度 < 5秒
- ✅ 质量满足需求
- ✅ 自动化可靠

### 切换到API的条件：
- ❌ Web版有频率限制
- ❌ 响应速度慢（>10秒）
- ❌ 需要验证码
- ❌ 自动化不稳定

## 数据收集表格

| 测试项目 | 结果 | 备注 |
|---------|------|------|
| 访问速度 | | 首页加载时间 |
| 是否需要登录 | | |
| 中文问答质量 | /10 | |
| 代码生成质量 | /10 | |
| 响应速度 | 秒 | 平均每条 |
| 单日限制 | | 次数/字数 |
| 自动化难度 | 低/中/高 | |

## 下一步

**立即行动**:
1. 你手动测试豆包网页版
2. 填写上面的表格
3. 截图发给我

**我来做**:
1. 分析你的测试结果
2. 设计自动化方案
3. 评估是否值得用API

---

## 预期结果

**最理想**: Web版免费好用 → 不花钱，省¥30/月
**可接受**: Web版一般 → API方案 ¥30/月，还是比Claude便宜
**最差**: 都不好用 → 继续只用Ollama+Claude

无论如何，**先测试，后决定** ✅
