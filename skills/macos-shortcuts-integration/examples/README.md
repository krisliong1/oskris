# macOS Shortcuts集成示例代码

实用的示例脚本，可直接运行或作为模板使用。

---

## 文件说明

### 1. `trigger-shortcut.sh` - Shell脚本调用

**功能**：简单的Shell脚本包装，带错误检查和彩色输出

**用法**：
```bash
# 基本运行
./trigger-shortcut.sh "快捷指令名称"

# 带输入文件
./trigger-shortcut.sh "图片处理" ~/image.jpg

# 带输入和输出
./trigger-shortcut.sh "图片压缩" ~/input.jpg ~/output.jpg
```

**特性**：
- ✅ 自动检查Shortcut是否存在
- ✅ 验证输入文件
- ✅ 自动创建输出目录
- ✅ 彩色输出（成功/失败提示）
- ✅ 详细的错误信息

---

### 2. `batch-process.applescript` - 批量处理

**功能**：批量处理文件夹中的所有文件

**用法**：
```bash
# 处理文件夹中的所有文件
osascript batch-process.applescript "/path/to/folder" "快捷指令名称"

# 示例：批量压缩图片
osascript batch-process.applescript ~/Downloads "批量图片压缩"
```

**特性**：
- ✅ 自动遍历文件夹
- ✅ 进度通知
- ✅ 成功/失败计数
- ✅ 完成后显示统计
- ✅ 错误日志记录

**适用场景**：
- 批量图片处理
- 批量文件转换
- 批量数据处理

---

### 3. `ai-to-shortcut.js` - Node.js桥接库

**功能**：完整的JavaScript库，用于OpenClaw集成

**安装**：
```bash
# 无需额外依赖，使用Node.js内置模块
node ai-to-shortcut.js list  # 测试是否工作
```

**API**：

#### `runShortcut(name, options)`
运行单个Shortcut

```javascript
const { runShortcut } = require('./ai-to-shortcut.js');

// 基本用法
const result = await runShortcut('图片处理');

// 带参数
const result = await runShortcut('图片压缩', {
  inputPath: '~/image.jpg',
  outputPath: '~/compressed.jpg',
  outputType: 'public.jpeg',
  timeout: 60000  // 60秒超时
});

if (result.success) {
  console.log('输出:', result.stdout);
} else {
  console.error('错误:', result.stderr);
}
```

#### `runShortcutBatch(name, files, concurrency)`
批量并行处理

```javascript
const { runShortcutBatch } = require('./ai-to-shortcut.js');

const files = [
  { inputPath: 'image1.jpg', outputPath: 'out1.jpg' },
  { inputPath: 'image2.jpg', outputPath: 'out2.jpg' },
  { inputPath: 'image3.jpg', outputPath: 'out3.jpg' }
];

const results = await runShortcutBatch('图片处理', files, 3);

// 结果数组
results.forEach(r => {
  console.log(`${r.file}: ${r.success ? '✅' : '❌'}`);
  if (!r.success) {
    console.log(`  错误: ${r.error}`);
  }
});
```

#### `listShortcuts()`
列出所有Shortcuts

```javascript
const { listShortcuts } = require('./ai-to-shortcut.js');

const shortcuts = await listShortcuts();
console.log('可用的Shortcuts:', shortcuts);
```

#### `shortcutExists(name)`
检查Shortcut是否存在

```javascript
const { shortcutExists } = require('./ai-to-shortcut.js');

if (await shortcutExists('图片处理')) {
  console.log('Shortcut存在');
} else {
  console.log('Shortcut不存在');
}
```

**CLI模式**：
```bash
# 列出所有Shortcuts
node ai-to-shortcut.js list

# 运行Shortcut
node ai-to-shortcut.js run "快捷指令名称"

# 带输入运行
node ai-to-shortcut.js run "图片处理" ~/image.jpg

# 批量处理文件夹
node ai-to-shortcut.js batch "图片处理" ~/Downloads
```

**特性**：
- ✅ Promise-based API
- ✅ 错误处理和重试
- ✅ 并发控制（防止系统过载）
- ✅ 输入文件验证
- ✅ 自动创建输出目录
- ✅ 详细日志
- ✅ 超时控制
- ✅ 可作为库或CLI使用

---

## 使用场景示例

### 场景1：OpenClaw调用图片处理

```javascript
// 在OpenClaw中集成
const { runShortcut } = require('./examples/ai-to-shortcut.js');

async function processImage(imagePath) {
  // 1. 压缩图片
  const compressed = await runShortcut('压缩图片', {
    inputPath: imagePath,
    outputPath: '/tmp/compressed.jpg'
  });
  
  if (!compressed.success) {
    throw new Error('压缩失败');
  }
  
  // 2. 添加水印
  const watermarked = await runShortcut('添加水印', {
    inputPath: '/tmp/compressed.jpg',
    outputPath: '/tmp/final.jpg'
  });
  
  return '/tmp/final.jpg';
}
```

### 场景2：批量整理下载文件

```bash
#!/bin/bash
# 使用trigger-shortcut.sh批量整理

for file in ~/Downloads/*; do
  ./trigger-shortcut.sh "智能文件整理" "$file"
done
```

### 场景3：定时任务

```bash
# 添加到crontab
# 每天早上8点执行
0 8 * * * /path/to/trigger-shortcut.sh "每日提醒"

# 每小时整理下载文件夹
0 * * * * osascript /path/to/batch-process.applescript ~/Downloads "文件整理"
```

### 场景4：与OpenClaw Heartbeat集成

```javascript
// 在HEARTBEAT.md或heartbeat脚本中
const { runShortcut, shortcutExists } = require('./skills/macos-shortcuts-integration/examples/ai-to-shortcut.js');

async function heartbeat() {
  // 检查是否有"每日检查"Shortcut
  if (await shortcutExists('每日检查')) {
    const result = await runShortcut('每日检查');
    
    if (result.success && result.stdout) {
      // 将结果发送到Discord
      await message({
        action: 'send',
        target: 'your-channel',
        message: `📋 每日检查结果:\n${result.stdout}`
      });
    }
  }
}
```

---

## 调试技巧

### 测试Shortcut是否可用

```bash
# 方法1：直接运行
shortcuts run "你的快捷指令"

# 方法2：用trigger-shortcut.sh（更详细的输出）
./trigger-shortcut.sh "你的快捷指令"

# 方法3：用JavaScript库
node ai-to-shortcut.js run "你的快捷指令"
```

### 查看执行日志

```bash
# macOS系统日志
log stream --predicate 'subsystem == "com.apple.shortcuts"' --level debug
```

### 错误处理

如果遇到问题：
1. 检查Shortcut名称是否正确（区分大小写）
2. 确保Shortcut在Shortcuts.app中可以手动运行
3. 检查文件路径是否正确
4. 查看系统日志

---

## 性能优化

### 并发处理

```javascript
// 推荐：控制并发数（3-5个）
await runShortcutBatch('处理', files, 3);

// 不推荐：无限制并发（可能卡死）
await Promise.all(files.map(f => runShortcut('处理', f)));
```

### 批量处理策略

```bash
# Shell脚本：后台并行 + wait
for file in *.jpg; do
  shortcuts run "处理" --input-path "$file" &
done
wait  # 等待所有完成
```

---

## 下一步

1. **创建你的第一个Shortcut**  
   打开Shortcuts.app，创建一个简单的处理流程

2. **测试示例脚本**  
   运行这些示例，确保工作正常

3. **集成到OpenClaw**  
   将`ai-to-shortcut.js`集成到你的工作流

4. **探索高级场景**  
   多步骤工作流、API集成、AI驱动的自动化

---

## 贡献

欢迎改进这些示例！添加新的场景或优化现有代码。

**维护者**: macOS Automation Specialist  
**最后更新**: 2026-02-22
