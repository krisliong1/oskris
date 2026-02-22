# Auto Conversation Logger - 自动对话记录器

## 触发条件
**自动触发** - 每次对话结束时自动运行

## 功能
自动记录所有对话内容到结构化文件，方便回顾和搜索。

## 记录内容
1. **完整对话** - 用户问题 + AI回复
2. **时间戳** - 精确到分钟
3. **关键决策** - 重要决定和行动
4. **待办事项** - 提取的任务
5. **学到的教训** - 经验总结

## 存储位置
```
~/.openclaw/workspace/memory/
├── YYYY-MM-DD.md (每日日志)
├── conversations/ (完整对话)
│   └── YYYY-MM-DD-HH-MM.md
└── indexed/ (按主题索引)
    ├── tasks.md
    ├── decisions.md
    └── lessons.md
```

## 自动处理流程

### 1. 每次对话后
```bash
# 记录完整对话
TIMESTAMP=$(date +%Y-%m-%d-%H-%M)
CONV_FILE=~/.openclaw/workspace/memory/conversations/${TIMESTAMP}.md

# 保存对话内容
echo "# 对话 - $TIMESTAMP" > "$CONV_FILE"
echo "" >> "$CONV_FILE"
echo "## 用户" >> "$CONV_FILE"
echo "$USER_MESSAGE" >> "$CONV_FILE"
echo "" >> "$CONV_FILE"
echo "## AI回复" >> "$CONV_FILE"
echo "$AI_RESPONSE" >> "$CONV_FILE"
```

### 2. 提取关键信息
- 扫描对话中的任务关键词（"帮我"、"创建"、"修复"等）
- 识别决策关键词（"决定"、"选择"、"采用"等）
- 识别教训关键词（"问题"、"错误"、"下次"等）

### 3. 更新索引
自动添加到对应的索引文件

## 实现方式

### 方案1: HEARTBEAT集成（推荐）
在HEARTBEAT.md中每30分钟：
1. 检查最近的对话
2. 提取未记录的内容
3. 自动分类存档

### 方案2: 专属Agent
创建一个后台Agent专门负责：
- 监听对话流
- 实时记录
- 智能分类
- 定期整理

### 方案3: Git Hook
利用git自动同步时：
- 扫描新内容
- 自动分类
- 推送到GitHub

## 使用示例

**自动记录模式**（无需手动触发）：
- 所有对话自动保存
- 每日自动汇总
- 每周自动索引

**手动查询**：
```bash
# 查找某日对话
ls ~/.openclaw/workspace/memory/conversations/2026-02-22*.md

# 搜索关键词
grep -r "修复" ~/.openclaw/workspace/memory/conversations/

# 查看所有待办
cat ~/.openclaw/workspace/memory/indexed/tasks.md
```

## 配置

### 记录级别
- **完整模式**: 记录所有对话（默认）
- **摘要模式**: 只记录关键对话
- **选择性**: 只记录标记的对话

### 隐私保护
- API密钥自动过滤
- 密码自动替换为 `***`
- 敏感信息不记录

## 维护

### 自动清理
- 30天后的对话归档压缩
- 90天后的对话可选删除
- 重要对话永久保留

### 索引更新
- 每日自动重建索引
- 每周生成摘要报告
- 每月生成统计分析

## 集成到主系统

在AGENTS.md中添加：
```markdown
## 每次对话后

自动触发Auto Conversation Logger记录：
1. 完整对话内容
2. 提取的任务
3. 重要决策
4. 学到的教训
```

## 立即启用

```bash
# 创建目录结构
mkdir -p ~/.openclaw/workspace/memory/{conversations,indexed}

# 创建索引文件
touch ~/.openclaw/workspace/memory/indexed/{tasks,decisions,lessons}.md

# 添加到HEARTBEAT
echo "检查并记录未保存的对话" >> ~/.openclaw/workspace/HEARTBEAT.md
```
