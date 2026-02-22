# Progress Tracker AI - 进度追踪者

**自动追踪所有AI团队任务、智能分类状态、生成每日进度报告**

## 技能概述

Progress Tracker AI 是一个自动化任务管理系统，能够：
- 扫描所有subagent会话
- 智能识别任务状态
- 追踪任务进度
- 生成每日统计报告
- 通过Discord通知重要完成事件

## 核心功能

### 1. 自动扫描机制

**数据源**：OpenClaw Sessions API
```bash
openclaw sessions --json
```

**扫描范围**：
- 所有 `agent:main:subagent:*` 会话
- 读取会话元数据（标签、时间戳、token使用）
- 解析会话内容（任务描述、输出结果）

**扫描频率建议**：
- 每30分钟自动扫描一次（via heartbeat或cron）
- 手动触发：`check-status.sh`

### 2. 智能状态分类

#### 状态识别规则

| 状态 | 识别条件 | 标记 |
|------|---------|------|
| **已完成** | - 最后一条消息是assistant<br>- 包含"完成"、"交付"、"Done"等关键词<br>- 超过10分钟无更新 | ✅ |
| **进行中** | - 最近5分钟内有活动<br>- 正在执行工具调用 | ⏳ |
| **等待中** | - 最后一条消息是assistant<br>- 包含问题、请求确认<br>- 5-30分钟无更新 | ⏸️ |
| **失败/阻塞** | - 包含错误信息<br>- abortedLastRun=true | ❌ |
| **等待审核** | - 创建了文件但未确认<br>- 包含"请检查"、"Please review" | 📝 |

#### 实现示例

```javascript
function classifyStatus(session, messages) {
  const lastMsg = messages[messages.length - 1];
  const ageMinutes = session.ageMs / 60000;
  
  // 检查是否失败
  if (session.abortedLastRun) return 'failed';
  
  // 检查是否进行中
  if (ageMinutes < 5) return 'in_progress';
  
  // 检查是否已完成
  if (lastMsg.role === 'assistant' && ageMinutes > 10) {
    const text = extractText(lastMsg);
    if (/完成|交付|Done|Completed|delivered/i.test(text)) {
      return 'completed';
    }
  }
  
  // 检查是否等待
  if (ageMinutes > 5 && ageMinutes < 30) {
    const text = extractText(lastMsg);
    if (/\?|请|确认|review|check/i.test(text)) {
      return 'waiting';
    }
  }
  
  return 'completed'; // 默认：超过30分钟 = 已完成
}
```

### 3. 进度追踪存储

**存储位置**：`~/.openclaw/ai-team/progress-tracker/tasks.json`

**数据结构**：
```json
{
  "version": "1.0",
  "lastScan": "2026-02-22T00:48:00.000Z",
  "sessions": [
    {
      "sessionKey": "agent:main:subagent:a120a2c4-eced-47cd-9758-286a8e57eed2",
      "sessionId": "7c14a74a-5a66-4711-a6d4-d4ab4bf80f95",
      "label": "discord-webhook-setup",
      "status": "completed",
      "summary": "Discord Event Webhook研究完成",
      "output": {
        "files": 10,
        "totalSize": "65KB",
        "skills": ["discord-event-webhooks"]
      },
      "startedAt": "2026-02-22T00:15:00.000Z",
      "completedAt": "2026-02-22T00:48:00.000Z",
      "duration": "33分钟",
      "tokenUsage": {
        "input": 200,
        "output": 31323,
        "total": 50269
      }
    }
  ],
  "dailyStats": {
    "2026-02-22": {
      "completed": 4,
      "inProgress": 1,
      "failed": 0,
      "totalFiles": 42,
      "totalTokens": 185000
    }
  }
}
```

**历史归档**：
- 每日归档到：`~/.openclaw/ai-team/progress-tracker/archives/2026-02-22.json`
- 保留最近30天数据

### 4. 每日统计报告

**生成时机**：
- 每日23:59自动生成
- 手动触发：`generate-daily-report.sh`

**报告内容**：

```markdown
# 📊 AI Team Progress Report - 2026-02-22

## 今日概览
- ✅ 完成任务：**4个**
- ⏳ 进行中：1个
- ❌ 失败：0个
- 📝 等待审核：0个

## 交付成果
- 📄 文档：42个文件
- 💾 代码：3个仓库
- 🔧 Skills：5个新技能
- 📊 数据大小：182 KB

## 完成任务详情

### 1. Discord Event Webhooks Research ✅
- **时长**：33分钟
- **交付**：10个文档，研究报告完整
- **Skill**：discord-event-webhooks
- **状态**：已归档

### 2. GitHub Issues Automation ✅
- **时长**：28分钟
- **交付**：自动化脚本 + 文档
- **Skill**：github-automation
- **状态**：已部署

## 需要关注
- ⏸️ **OAuth Security Review** - 等待用户确认（已等待2小时）

## 建议操作
- [x] 关闭已完成的4个sessions
- [ ] 跟进OAuth Security Review
- [ ] 归档今日报告

## Token使用
- 总消耗：185,234 tokens
- 平均每任务：46,308 tokens
```

### 5. Discord通知集成

**通知触发条件**：
- 任务完成（超过20分钟的任务）
- 任务失败
- 任务等待超过2小时

**通知消息格式**：

```javascript
// Discord Webhook示例
{
  "content": "📢 **任务完成通知**",
  "embeds": [{
    "title": "✅ Discord Event Webhooks Research",
    "description": "研究完成，已交付10个文档",
    "color": 5763719,
    "fields": [
      {"name": "时长", "value": "33分钟", "inline": true},
      {"name": "Token", "value": "50,269", "inline": true},
      {"name": "交付", "value": "10 files, 65KB", "inline": false}
    ],
    "timestamp": "2026-02-22T00:48:00.000Z"
  }]
}
```

**Discord配置**：
```bash
# 设置webhook URL
export PROGRESS_TRACKER_WEBHOOK="https://discord.com/api/webhooks/..."
```

## 使用方式

### 手动扫描
```bash
~/.openclaw/ai-team/progress-tracker/scan-sessions.sh
```

### 查看当前状态
```bash
~/.openclaw/ai-team/progress-tracker/check-status.sh
```

### 生成报告
```bash
~/.openclaw/ai-team/progress-tracker/generate-daily-report.sh
```

### 自动化运行（Heartbeat）

在 `HEARTBEAT.md` 中添加：
```markdown
## Progress Tracking
- [ ] 每30分钟扫描一次sessions（检查 heartbeat-state.json）
- [ ] 发现新完成任务时发送Discord通知
- [ ] 每日23:59生成报告
```

## 数据分析能力

### 趋势分析
- 每日完成任务数变化
- 平均任务完成时长
- Token使用效率
- 高产时段识别

### 团队效率指标
```json
{
  "weeklyMetrics": {
    "avgCompletionTime": "25分钟",
    "successRate": "95%",
    "avgTokenPerTask": 45000,
    "peakHours": ["10:00-12:00", "14:00-16:00"]
  }
}
```

## 集成方案

### 与现有Skills集成
- 读取 `skills/*/SKILL.md` 验证交付物
- 识别skill创建/更新事件
- 统计skill使用频率

### 与Memory系统集成
- 自动更新 `MEMORY.md` 的项目进度部分
- 记录重要里程碑
- 提取经验教训

## 扩展功能

### 未来增强
1. **AI助手评分** - 根据完成质量、效率评分
2. **任务优先级预测** - ML预测哪些任务需要优先处理
3. **资源瓶颈识别** - 发现重复失败的任务类型
4. **自动清理** - 归档超过30天的旧sessions
5. **Web Dashboard** - 可视化进度看板

## 安全与隐私

- ✅ 本地存储，不上传敏感数据
- ✅ Discord通知只发送摘要，不包含详细内容
- ✅ 支持黑名单（某些session不追踪）

## 维护指南

### 定期维护
- 每周检查存储大小
- 每月归档旧数据
- 定期更新状态识别规则

### 故障排查
```bash
# 检查扫描日志
tail -f ~/.openclaw/ai-team/progress-tracker/logs/scan.log

# 验证数据完整性
cat ~/.openclaw/ai-team/progress-tracker/tasks.json | jq .

# 重建索引
rm tasks.json && ./scan-sessions.sh
```

## 依赖要求

- OpenClaw >= 2026.2.15
- jq (JSON处理)
- curl (Discord通知)
- bash >= 4.0

## 相关文档

- [OpenClaw Sessions API](https://docs.openclaw.ai/cli/sessions)
- [Discord Webhooks](https://discord.com/developers/docs/resources/webhook)
- [Subagent Management](/tools/subagents)

---

**创建者**：Progress Tracker Specialist  
**创建日期**：2026-02-22  
**版本**：1.0  
**状态**：Active
