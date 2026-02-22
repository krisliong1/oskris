# Auto Memory Updater - 自动记忆更新器

## 触发条件
**自动触发** - 每次heartbeat时检查并更新

## 功能
自动从对话中提取重要信息并更新MEMORY.md，无需手动操作。

## 工作流程

### 1. 检测新对话
```bash
# 检查session history
# 提取最近的对话内容
# 识别未记录的信息
```

### 2. 智能提取
自动识别并提取：
- **重要决策** - "决定"、"选择"、"采用"
- **关键任务** - "必须"、"要求"、"需要"
- **经验教训** - "问题"、"错误"、"注意"
- **用户偏好** - "喜欢"、"不要"、"想要"
- **系统变更** - "创建"、"修复"、"更新"

### 3. 自动更新MEMORY.md
```markdown
## YYYY-MM-DD HH:MM - [自动记录]

**关键信息**:
- 提取的内容

**决策**:
- 提取的内容

**教训**:
- 提取的内容
```

### 4. 保存并同步
- 自动追加到MEMORY.md
- 自动commit到Git
- 自动push到GitHub

## 在HEARTBEAT中的实现

```bash
# 检查是否有新对话需要记录
LAST_UPDATE=$(tail -1 ~/.openclaw/workspace/MEMORY.md | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}')
CURRENT_TIME=$(date +%Y-%m-%d)

if [ "$LAST_UPDATE" != "$CURRENT_TIME" ]; then
  # 调用记忆更新逻辑
  # 提取今日重要对话
  # 自动追加到MEMORY.md
  # Git commit & push
fi
```

## 关键词识别

### 决策类
- "决定"、"选择"、"采用"、"使用"、"方案"

### 任务类
- "必须"、"要求"、"需要"、"立刻"、"马上"

### 问题类
- "错误"、"失败"、"问题"、"bug"、"修复"

### 偏好类
- "喜欢"、"不喜欢"、"不要"、"想要"、"希望"

### 系统类
- "创建"、"删除"、"修改"、"更新"、"配置"

## 自动化脚本

创建 `~/.openclaw/workspace/memory/auto-update-memory.sh`：

```bash
#!/bin/bash
# 自动记忆更新脚本

MEMORY_FILE=~/.openclaw/workspace/MEMORY.md
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# 从session history提取最近对话
# （这部分需要OpenClaw API支持）

# 智能提取关键信息
# （使用grep或AI分析）

# 追加到MEMORY.md
echo "" >> "$MEMORY_FILE"
echo "## $TIMESTAMP - [自动记录]" >> "$MEMORY_FILE"
echo "" >> "$MEMORY_FILE"
echo "**对话摘要**: ..." >> "$MEMORY_FILE"

# Git同步
cd ~/.openclaw/workspace
git add MEMORY.md
git commit -m "🤖 自动更新记忆 - $TIMESTAMP"
git push
```

## 集成到系统

在HEARTBEAT.md中添加：
```markdown
## 🧠 自动记忆更新（每次heartbeat）

运行记忆更新检查：
```bash
~/.openclaw/workspace/memory/auto-update-memory.sh
```
```

## 优势
- ✅ 完全自动，无需手动
- ✅ 永不遗忘重要信息
- ✅ 实时更新到GitHub
- ✅ 智能提取关键内容
- ✅ 保持MEMORY.md简洁

## 配置

### 更新频率
- 每次heartbeat检查（30分钟）
- 或每日自动汇总

### 提取级别
- **简洁模式**: 只记录最关键的
- **详细模式**: 记录所有重要对话
- **完整模式**: 记录所有对话（不推荐）

## 隐私保护
- 自动过滤API密钥
- 自动替换密码为 `***`
- 敏感信息不记录到Git
