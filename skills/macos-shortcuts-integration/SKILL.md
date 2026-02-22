---
name: macos-shortcuts-integration
description: OpenClaw与macOS Shortcuts/Automator/AppleScript集成。本地自动化、文件处理、系统操作的技术指南。
tags: [macos, automation, shortcuts, applescript, system-integration]
---

# macOS Shortcuts Integration Skill

OpenClaw调用macOS原生自动化工具的技术实现指南。

---

## 快速开始

### 最简单的调用

```bash
# 运行一个Shortcut
shortcuts run "快捷指令名称"

# 带输入文件
shortcuts run "图片压缩" --input-path ~/image.jpg --output-path ~/compressed.jpg
```

### 在OpenClaw中使用

```javascript
// exec工具调用
const result = await exec({
  command: 'shortcuts run "批量处理" --input-path ~/Downloads/*.jpg'
});
```

---

## 方法对比表

| 方法 | 难度 | 速度 | 返回值 | 批处理 | 推荐度 |
|------|------|------|--------|--------|--------|
| shortcuts CLI | ⭐ 简单 | 🚀 快 | ✅ 支持 | ✅ 优秀 | ⭐⭐⭐⭐⭐ |
| URL Scheme | ⭐ 简单 | ⚡ 很快 | ❌ 困难 | ❌ 不适合 | ⭐⭐⭐ |
| AppleScript | ⭐⭐⭐ 复杂 | 🐢 中等 | ✅ 支持 | ⚠️ 一般 | ⭐⭐⭐⭐ |
| Automator | ⭐⭐ 中等 | 🐢 慢 | ❌ 困难 | ✅ 优秀 | ⭐⭐ |

**推荐**：90%的场景用 `shortcuts CLI`

---

## 方法1：shortcuts CLI（主力方法）

### 基本命令

```bash
# 列出所有Shortcuts
shortcuts list

# 查看Shortcut详情
shortcuts view "快捷指令名称"

# 运行Shortcut
shortcuts run "快捷指令名称"

# 带输入
shortcuts run "处理文本" --input-path input.txt

# 带输出
shortcuts run "图片处理" \
  --input-path image.jpg \
  --output-path result.png \
  --output-type public.png
```

### 输出类型（UTI）

常用的`--output-type`值：

```
public.plain-text       # 纯文本
public.json             # JSON数据
public.png              # PNG图片
public.jpeg             # JPEG图片
public.html             # HTML文档
public.xml              # XML文档
com.adobe.pdf           # PDF文件
```

查找更多UTI：https://developer.apple.com/documentation/uniformtypeidentifiers

### OpenClaw集成模板

```javascript
/**
 * 通用Shortcut调用函数
 */
async function runShortcut(name, options = {}) {
  const { inputPath, outputPath, outputType } = options;
  
  let command = `shortcuts run "${name}"`;
  
  if (inputPath) {
    command += ` --input-path "${inputPath}"`;
  }
  
  if (outputPath) {
    command += ` --output-path "${outputPath}"`;
  }
  
  if (outputType) {
    command += ` --output-type ${outputType}`;
  }
  
  const result = await exec({ command });
  return result;
}

// 使用示例
await runShortcut("批量压缩图片", {
  inputPath: "~/Downloads/*.jpg",
  outputPath: "~/compressed/",
  outputType: "public.jpeg"
});
```

### 错误处理

```bash
# 检查Shortcut是否存在
if shortcuts list | grep -q "图片处理"; then
  shortcuts run "图片处理" --input-path image.jpg
else
  echo "错误：Shortcut不存在"
  exit 1
fi
```

---

## 方法2：URL Scheme（快速触发）

### 基本语法

```bash
# 简单运行
open "shortcuts://run-shortcut?name=快捷指令名称"

# 带文本输入
open "shortcuts://run-shortcut?name=发送通知&input=text&text=Hello"

# URL编码中文
name=$(python3 -c "import urllib.parse; print(urllib.parse.quote('生成图片'))")
open "shortcuts://run-shortcut?name=$name"
```

### x-callback-url（带回调）

```bash
# 成功后回调
open "shortcuts://x-callback-url/run-shortcut?name=任务&x-success=myapp://done"

# 失败时回调
open "shortcuts://x-callback-url/run-shortcut?name=任务&x-error=myapp://error"
```

### 适用场景

✅ **适合**：
- 快速通知
- 简单任务触发
- 用户交互场景

❌ **不适合**：
- 批量处理（会打开GUI）
- 需要返回值
- 后台静默运行

---

## 方法3：AppleScript（高级控制）

### 基本调用

```applescript
tell application "Shortcuts Events"
    run shortcut "快捷指令名称"
end tell
```

### 带输入和输出

```applescript
tell application "Shortcuts Events"
    set result to run shortcut "计算器" with input "42"
    return result
end tell
```

### 命令行执行

```bash
# 单行执行
osascript -e 'tell application "Shortcuts Events" to run shortcut "任务"'

# 多行脚本
osascript <<EOF
tell application "Shortcuts Events"
    set result to run shortcut "处理文本" with input "测试"
    return result
end tell
EOF
```

### 复杂示例：控制多个应用

```applescript
-- 1. 运行Shortcut生成图片
tell application "Shortcuts Events"
    set imagePath to run shortcut "AI生成图片" with input "一只猫"
end tell

-- 2. 在Finder中打开
tell application "Finder"
    reveal POSIX file imagePath
    activate
end tell

-- 3. 发送通知
display notification "图片已生成" with title "任务完成"
```

### OpenClaw集成

```javascript
// 封装AppleScript调用
async function runShortcutWithResult(name, input = null) {
  let script = `tell application "Shortcuts Events"\n`;
  
  if (input) {
    script += `  set result to run shortcut "${name}" with input "${input}"\n`;
  } else {
    script += `  set result to run shortcut "${name}"\n`;
  }
  
  script += `  return result\nend tell`;
  
  const result = await exec({
    command: `osascript -e '${script}'`
  });
  
  return result.stdout.trim();
}

// 使用
const output = await runShortcutWithResult("翻译文本", "Hello World");
console.log(output); // "你好世界"
```

---

## 方法4：Automator（后台服务）

### 创建Automator服务

1. 打开Automator.app
2. 选择"快速操作"（Quick Action）
3. 设置接收类型（文件、文本等）
4. 添加动作
5. 保存到 `~/Library/Services/`

### 命令行调用

```bash
# 方法1：通过automator命令
automator -i input.txt ~/Library/Services/批量处理.workflow

# 方法2：通过AppleScript
osascript -e 'tell application "System Events" to do shell script "automator ~/Library/Services/批量处理.workflow"'
```

### 文件夹监控

```applescript
-- 在Automator中设置"文件夹操作"
-- 当文件添加到~/Downloads时自动触发

on adding folder items to this_folder after receiving added_items
    repeat with item in added_items
        -- 调用Shortcut处理文件
        do shell script "shortcuts run '文件处理' --input-path " & quoted form of POSIX path of item
    end repeat
end adding folder items
```

---

## 实用场景示例

### 场景1：批量图片处理

**需求**：压缩、调整大小、添加水印

**Shortcut设计**（在iOS/macOS Shortcuts.app中创建）：
1. 接收图片
2. 调整大小到1920x1080
3. 压缩质量到80%
4. 添加文字水印（右下角日期）
5. 保存到指定文件夹

**OpenClaw调用**：
```bash
# 处理单张
shortcuts run "批量图片处理" \
  --input-path ~/Downloads/photo.jpg \
  --output-path ~/processed/photo.jpg

# 批量处理
for img in ~/Downloads/*.jpg; do
  shortcuts run "批量图片处理" \
    --input-path "$img" \
    --output-path ~/processed/$(basename "$img")
done
```

---

### 场景2：智能文件整理

**需求**：自动分类文件到不同文件夹

**Shortcut设计**：
1. 接收文件
2. 获取文件类型
3. 如果是图片 → OCR提取文本 → 根据内容分类
4. 如果是文档 → 读取元数据 → 按日期分类
5. 移动到对应文件夹
6. 重命名为统一格式

**OpenClaw集成**：
```javascript
async function organizeFiles(folderPath) {
  // 获取文件列表
  const files = await exec({
    command: `find "${folderPath}" -type f`
  });
  
  // 逐个处理
  for (const file of files.stdout.split('\n')) {
    if (!file) continue;
    
    await exec({
      command: `shortcuts run "智能文件整理" --input-path "${file}"`
    });
  }
  
  return "整理完成";
}

// 使用
await organizeFiles("~/Downloads");
```

---

### 场景3：定时任务与通知

**需求**：每天早上检查日历，发送今日提醒

**Shortcut设计**：
1. 获取今日日历事件
2. 筛选重要事件
3. 生成总结文本
4. 发送macOS通知
5. 可选：发送到Discord/Telegram

**OpenClaw Heartbeat集成**：
```javascript
// 在HEARTBEAT.md中添加
async function morningRoutine() {
  const now = new Date();
  
  // 仅在早上8点执行
  if (now.getHours() === 8 && now.getMinutes() < 30) {
    const result = await exec({
      command: 'shortcuts run "今日提醒"'
    });
    
    // 将结果发送到Discord
    if (result.stdout) {
      await message({
        action: 'send',
        target: 'your-channel',
        message: `📅 今日日程：\n${result.stdout}`
      });
    }
  }
}
```

---

### 场景4：AI图片后处理

**需求**：豆包生成图片 → 自动压缩、添加水印、上传

**完整工作流**：
```javascript
async function generateAndProcess(prompt) {
  // 1. 调用豆包生成图片（假设豆包有API）
  const imagePath = await callDoubao(prompt);
  
  // 2. Shortcut后处理
  const processedPath = `/tmp/processed_${Date.now()}.jpg`;
  await exec({
    command: `shortcuts run "图片后处理" --input-path "${imagePath}" --output-path "${processedPath}"`
  });
  
  // 3. 上传到服务器
  await exec({
    command: `scp "${processedPath}" user@server:/var/www/images/`
  });
  
  return `https://example.com/images/${path.basename(processedPath)}`;
}

// 使用
const url = await generateAndProcess("一只可爱的猫咪");
console.log("图片地址:", url);
```

---

## VPS集成方案

### 方案A：SSH远程调用

**架构**：VPS通过SSH调用Mac mini的Shortcuts

```bash
# VPS端脚本
ssh mac-mini "shortcuts run '图片处理' --input-path ~/queue/image.jpg --output-path ~/processed/image.jpg"

# 下载处理后的文件
scp mac-mini:~/processed/image.jpg ./
```

**优点**：
- ✅ 充分利用macOS功能
- ✅ VPS和Mac各司其职

**缺点**：
- ❌ 需要Mac保持开机
- ❌ 网络延迟

---

### 方案B：HTTP API包装

**Mac端**：创建简单的HTTP服务器

```javascript
// server.js (在Mac上运行)
const express = require('express');
const { exec } = require('child_process');

const app = express();

app.post('/run-shortcut', (req, res) => {
  const { name, input } = req.body;
  
  exec(`shortcuts run "${name}" --input-path "${input}"`, (err, stdout) => {
    if (err) {
      res.status(500).json({ error: err.message });
    } else {
      res.json({ result: stdout });
    }
  });
});

app.listen(3000);
```

**VPS端**：
```bash
curl -X POST http://mac-mini:3000/run-shortcut \
  -H "Content-Type: application/json" \
  -d '{"name":"图片处理","input":"~/image.jpg"}'
```

---

### 方案C：Linux原生替代

**不需要Mac的替代方案**：

```bash
# Shortcuts图片处理 → ImageMagick
convert input.jpg -resize 800x600 -quality 80 output.jpg

# Shortcuts文件整理 → bash脚本
for file in ~/Downloads/*; do
  case "${file##*.}" in
    jpg|png) mv "$file" ~/Pictures/ ;;
    pdf) mv "$file" ~/Documents/ ;;
    *) mv "$file" ~/Other/ ;;
  esac
done

# Shortcuts OCR → Tesseract
tesseract image.jpg output.txt
```

**何时使用**：
- Mac无法保持开机
- VPS性能更强
- 不需要macOS专属功能

---

## 常用macOS工具速查

### 图片处理

```bash
# sips - 系统自带图片工具
sips -z 800 600 image.jpg                    # 调整大小
sips -s format png image.jpg --out image.png # 转换格式
sips -r 90 image.jpg                         # 旋转

# ImageMagick（需安装：brew install imagemagick）
convert input.jpg -resize 50% output.jpg
convert *.jpg output.pdf                     # 合并为PDF
```

### 文本处理

```bash
# textutil - 文档转换
textutil -convert html document.doc          # Word转HTML
textutil -convert txt document.pdf           # PDF转纯文本

# say - 文本转语音
say "Hello World"
say -o output.aiff "保存为音频文件"
```

### 文件操作

```bash
# open - 打开文件/应用/URL
open file.pdf                                # 用默认应用打开
open -a Safari https://example.com           # 指定应用
open .                                       # 在Finder中打开当前目录
```

---

## 调试技巧

### 查看Shortcut执行日志

```bash
# macOS系统日志
log stream --predicate 'subsystem == "com.apple.shortcuts"' --level debug
```

### 测试Shortcut

```bash
# 先测试能否列出
shortcuts list | grep "你的快捷指令"

# 测试运行（带详细输出）
shortcuts run "测试" --input-path test.txt 2>&1
```

### AppleScript调试

```applescript
-- 添加日志
log "开始执行"
tell application "Shortcuts Events"
    set result to run shortcut "测试"
    log "结果: " & result
end tell
```

---

## 最佳实践

### 1. 命名规范

**Shortcuts命名**：
- ✅ 用途清晰：`OpenClaw-批量压缩图片`
- ✅ 前缀区分：`OpenClaw-` 开头表示专为AI设计
- ❌ 避免中文复杂字符（URL编码麻烦）

### 2. 错误处理

**在Shortcut中**：
- 添加"如果"条件检查输入
- 使用"通知"反馈结果
- 记录日志到文件

**在OpenClaw中**：
```javascript
try {
  const result = await exec({
    command: 'shortcuts run "任务" --input-path file.jpg'
  });
  
  if (result.exitCode !== 0) {
    throw new Error(`Shortcut失败: ${result.stderr}`);
  }
  
  return result.stdout;
} catch (error) {
  console.error("执行失败:", error);
  // 降级方案
  return await fallbackMethod();
}
```

### 3. 性能优化

```bash
# 批量处理时，并行执行
for img in *.jpg; do
  shortcuts run "处理" --input-path "$img" &
done
wait  # 等待所有后台任务完成
```

### 4. 安全性

```bash
# 避免路径注入
safe_path=$(printf '%q' "$user_input")
shortcuts run "处理" --input-path "$safe_path"
```

---

## 常见问题

### Q1: Shortcut权限问题

**症状**：首次运行AppleScript调用时卡住

**解决**：
1. 打开"系统设置" → "隐私与安全性"
2. 找到"自动化"
3. 允许Terminal/OpenClaw控制Shortcuts

### Q2: 找不到Shortcut

**症状**：`shortcuts list`没有显示

**解决**：
1. 确保在Shortcuts.app中创建了快捷指令
2. 确保快捷指令已同步（iCloud）
3. 尝试重启Shortcuts.app

### Q3: 输出类型不匹配

**症状**：`--output-type`报错

**解决**：
- 使用正确的UTI格式
- 查看Apple文档确认支持的类型
- 尝试不指定output-type（自动检测）

---

## 下一步学习

1. **创建第一个Shortcut**：简单的文本处理或通知
2. **在OpenClaw中调用**：用`shortcuts run`测试
3. **探索复杂场景**：多步骤工作流、API集成
4. **研究豆包API**：尝试本地调用
5. **优化性能**：批处理、并行执行

---

## 参考资源

- [Apple Shortcuts用户指南](https://support.apple.com/guide/shortcuts/welcome/)
- [shortcuts CLI文档](https://support.apple.com/guide/shortcuts-mac/intro-to-shortcuts-apdf22b0444c/)
- [AppleScript语言指南](https://developer.apple.com/library/archive/documentation/AppleScript/)
- [UTI类型参考](https://developer.apple.com/documentation/uniformtypeidentifiers)

---

**维护者**: macOS Automation Specialist  
**最后更新**: 2026-02-22  
**版本**: 1.0
