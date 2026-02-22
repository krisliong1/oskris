# iOS Shortcuts CLI 基础

**难度**: ⭐  
**优先级**: P0（入门必备）  
**学习时长**: 15分钟

---

## 简介

macOS内置了`shortcuts`命令行工具，让你能在终端中运行、管理和查看iOS Shortcuts，无需打开图形界面。这是自动化和脚本化shortcuts的基础。

**为什么需要它？**
- 🚀 在shell脚本中调用shortcuts
- 🔄 批量运行shortcuts
- 🤖 结合其他命令行工具
- ⚡ 快速测试和调试

---

## 核心概念

### 什么是shortcuts CLI？

`shortcuts`是Apple提供的命令行工具，位于`/usr/bin/shortcuts`。它能：
- 列出所有已安装的shortcuts
- 运行指定的shortcut
- 在Shortcuts app中打开查看
- 签名shortcut文件（高级功能）

### 与Shortcuts App的关系

CLI访问的是**同一个shortcuts库**。你在App中创建的shortcuts，CLI都能看到和运行。

---

## 基础用法

### 1. 列出所有Shortcuts

```bash
shortcuts list
```

**输出示例**:
```
My Morning Routine
Quick Note
Convert Text to Speech
Weather Report
```

**用途**: 查看有哪些shortcuts可用

---

### 2. 运行Shortcut

```bash
shortcuts run "Shortcut Name"
```

**实际示例**:
```bash
# 运行名为"Weather Report"的shortcut
shortcuts run "Weather Report"
```

**注意**: 
- 名称必须完全匹配（大小写敏感）
- 包含空格的名称需要用引号

---

### 3. 传递输入

```bash
echo "Hello World" | shortcuts run "Process Text"
```

**工作原理**: 
- stdin的内容作为shortcut的input
- shortcut可以通过"Get Shortcut Input"获取

**示例**:
```bash
# 传递文件内容
cat file.txt | shortcuts run "Text Analyzer"

# 传递命令输出
date | shortcuts run "Format Date"
```

---

### 4. 接收输出

```bash
shortcuts run "Generate JSON" > output.json
```

**工作原理**:
- shortcut的"Stop and Output"输出到stdout
- 可以重定向到文件或管道到其他命令

**示例**:
```bash
# 保存输出
shortcuts run "Daily Report" > report.txt

# 管道到其他命令
shortcuts run "Get URLs" | grep "https"
```

---

### 5. 在App中查看

```bash
shortcuts view "Shortcut Name"
```

**效果**: 在Shortcuts app中打开该shortcut，可以编辑查看

---

## 实际示例

### 示例1: Shell脚本自动化

```bash
#!/bin/bash
# 每日自动化脚本

echo "Running morning routine..."
shortcuts run "Morning Routine"

echo "Generating daily report..."
shortcuts run "Daily Report" > ~/Reports/$(date +%Y-%m-%d).txt

echo "Done!"
```

**应用场景**: 通过cron定时运行

---

### 示例2: 批量处理文件

```bash
# 遍历所有txt文件，用shortcut处理
for file in *.txt; do
    echo "Processing $file..."
    cat "$file" | shortcuts run "Text Processor" > "processed_$file"
done
```

**应用场景**: 批量文本转换、格式化

---

### 示例3: 结合其他命令

```bash
# 获取系统信息，发送到shortcut生成报告
{
    echo "=== System Info ==="
    uname -a
    echo "=== Disk Usage ==="
    df -h
    echo "=== Memory ==="
    top -l 1 | head -n 10
} | shortcuts run "System Report Generator"
```

**应用场景**: 系统监控自动化

---

### 示例4: 错误处理

```bash
if shortcuts run "Backup Data" 2>&1; then
    echo "Backup successful"
else
    echo "Backup failed!" >&2
    exit 1
fi
```

**应用场景**: 可靠的自动化脚本

---

## 常见陷阱

### ❌ 陷阱1: 名称不匹配

```bash
# 错误
shortcuts run "weather report"  # 小写

# 正确
shortcuts run "Weather Report"  # 完全匹配
```

**解决**: 先用`shortcuts list`确认准确名称

---

### ❌ 陷阱2: 忘记引号

```bash
# 错误
shortcuts run My Morning Routine  # 只运行了"My"

# 正确
shortcuts run "My Morning Routine"
```

---

### ❌ 陷阱3: 未处理输入/输出

```bash
# 可能无输出
shortcuts run "Some Shortcut"

# 确保shortcut有输出
shortcuts run "Some Shortcut" || echo "No output"
```

**提示**: 在shortcut中确保使用"Stop and Output"

---

### ❌ 陷阱4: 权限问题

某些shortcuts需要用户交互或权限，CLI运行可能失败。

**解决**: 
- 确保shortcut不依赖UI交互
- 或者在有UI环境下运行

---

## 高级技巧

### 技巧1: 检查shortcut是否存在

```bash
if shortcuts list | grep -q "^My Shortcut$"; then
    shortcuts run "My Shortcut"
else
    echo "Shortcut not found"
fi
```

---

### 技巧2: 超时控制

```bash
# 5秒超时
timeout 5 shortcuts run "Long Running Task"
```

---

### 技巧3: 后台运行

```bash
# 后台运行，不阻塞
shortcuts run "Background Task" &
```

---

### 技巧4: 结合jq处理JSON输出

```bash
shortcuts run "Get API Data" | jq '.items[] | .name'
```

---

## 完整示例：自动化Workflow

```bash
#!/bin/bash
# daily_automation.sh - 每日自动化脚本

set -e  # 遇到错误立即退出

# 1. 检查shortcuts可用性
if ! command -v shortcuts &> /dev/null; then
    echo "❌ shortcuts command not found"
    exit 1
fi

# 2. 检查必需的shortcuts是否存在
required_shortcuts=(
    "Morning Routine"
    "Email Digest"
    "Daily Report"
)

for sc in "${required_shortcuts[@]}"; do
    if ! shortcuts list | grep -q "^${sc}$"; then
        echo "❌ Shortcut '$sc' not found"
        exit 1
    fi
done

# 3. 运行morning routine
echo "🌅 Running morning routine..."
shortcuts run "Morning Routine"

# 4. 生成邮件摘要
echo "📧 Generating email digest..."
shortcuts run "Email Digest" > /tmp/email_digest.txt
cat /tmp/email_digest.txt

# 5. 生成并保存日报
echo "📊 Generating daily report..."
REPORT_DIR="$HOME/Documents/Reports"
mkdir -p "$REPORT_DIR"
shortcuts run "Daily Report" > "$REPORT_DIR/$(date +%Y-%m-%d).md"

echo "✅ Daily automation complete!"
```

**运行方式**:
```bash
chmod +x daily_automation.sh
./daily_automation.sh

# 或添加到crontab
# 每天早上8点运行
# 0 8 * * * /path/to/daily_automation.sh
```

---

## 相关Skills

### 必须先学
- `ios-shortcuts-terminology` - 理解基本概念

### 组合使用
- `ios-shortcuts-input-output-flow` - 处理输入输出
- `ios-shortcuts-debugging` - 调试CLI运行问题
- `ios-shortcuts-run-shortcut` - Shortcuts互调（在shortcut内）

### 进阶方向
- `ios-shortcuts-file-format` - 理解.shortcut文件
- `ios-shortcuts-best-practices` - 生产级CLI集成

---

## 进阶资源

### 官方文档
```bash
shortcuts --help
man shortcuts  # 可能不存在，但值得尝试
```

### 常用参数速查

| 命令 | 用途 | 示例 |
|-----|------|------|
| `shortcuts list` | 列出shortcuts | - |
| `shortcuts run "Name"` | 运行shortcut | `shortcuts run "Test"` |
| `shortcuts view "Name"` | 在App中查看 | `shortcuts view "Test"` |
| `shortcuts sign file` | 签名文件 | `shortcuts sign test.shortcut` |

### 组合模式

**模式1: 管道链**
```bash
command1 | shortcuts run "Process" | command2
```

**模式2: 条件执行**
```bash
shortcuts run "Check" && shortcuts run "Action"
```

**模式3: 循环批处理**
```bash
for item in list; do shortcuts run "Process" <<< "$item"; done
```

---

## 实战练习

### 练习1: Hello World
创建一个shortcut返回"Hello World"，然后用CLI运行：
```bash
shortcuts run "Hello World"
```

### 练习2: 输入处理
创建一个接收文本输入的shortcut，用CLI传递数据：
```bash
echo "Test Input" | shortcuts run "Echo Test"
```

### 练习3: 输出重定向
创建一个生成JSON的shortcut，保存输出：
```bash
shortcuts run "Generate JSON" > output.json
cat output.json
```

---

**下一步**: 学习 `ios-shortcuts-variables-set-get` 掌握变量操作

**最后更新**: 2026-02-22
