# Task Dispatcher Skill

## 目的
**让AI团队并行工作，而不是主AI一个人干所有事。检测空闲AI，分配任务，提高效率。**

## 设计理念

### 传统模式（低效）❌
```
主AI: 我要做10件事...
├─ 任务1: 下载Ollama模型 (20分钟)
├─ 任务2: 整理Downloads (10分钟)
├─ 任务3: 备份到VPS (15分钟)
├─ 任务4: 生成学习报告 (5分钟)
└─ 任务5: 检查iPhone存储 (5分钟)

总时间: 55分钟 (顺序执行)
```

### AI团队模式（高效）✅
```
主AI: 检测空闲AI → 分配任务 → 监控进度

Deploy Manager: 下载Ollama模型 (20分钟) ←并行→
File Organizer: 整理Downloads (10分钟)   ←并行→
Backup Manager: 备份到VPS (15分钟)      ←并行→
AI Dev Logger: 生成学习报告 (5分钟)     ←并行→
Smart Dispatcher: 检查iPhone (5分钟)    ←并行→

总时间: 20分钟 (并行执行，最长任务时间)
效率提升: 2.75倍！
```

---

## 核心功能

### 1️⃣ 检测AI状态

```bash
# 检查所有AI是否在线和空闲
~/.openclaw/workspace/skills/task-dispatcher/check-availability.sh

# 输出:
# AI团队状态报告:
# ✅ Backup Manager    - 空闲 (可用)
# ✅ File Organizer    - 空闲 (可用)
# ⏳ Deploy Manager    - 忙碌 (Ollama安装中)
# ✅ Smart Dispatcher  - 空闲 (可用)
# ✅ AI Dev Logger     - 空闲 (可用)
#
# 可用AI数量: 4/5
```

### 2️⃣ 任务分配逻辑

**匹配规则**:
```javascript
{
  "任务类型": "最适合的AI",
  
  "备份相关": "Backup Manager",
  "文件整理": "File Organizer",
  "部署/安装": "Deploy Manager",
  "任务路由": "Smart Dispatcher",
  "记录/文档": "AI Dev Logger",
  
  "通用任务": "任何空闲AI"
}
```

### 3️⃣ 并行执行

```bash
# 主AI发起任务分配
~/.openclaw/workspace/skills/task-dispatcher/assign-tasks.sh

# 示例任务列表:
# 1. 下载Ollama模型 → Deploy Manager
# 2. 整理Downloads → File Organizer
# 3. 备份到VPS → Backup Manager
# 4. 记录今日进展 → AI Dev Logger

# 系统自动:
# - 检测每个AI是否空闲
# - 分配合适的任务
# - 发送任务到对应session
# - 追踪执行状态
```

---

## 任务队列系统

### task-queue.json
```json
{
  "pending": [
    {
      "id": "task-001",
      "title": "下载Ollama Qwen 2.5 14B模型",
      "type": "deployment",
      "priority": "high",
      "estimated_time": "20分钟",
      "preferred_ai": "Deploy Manager",
      "fallback_ai": ["Smart Dispatcher"],
      "created": "2026-02-21 11:00"
    },
    {
      "id": "task-002",
      "title": "整理~/Downloads文件夹",
      "type": "file_management",
      "priority": "medium",
      "estimated_time": "10分钟",
      "preferred_ai": "File Organizer",
      "created": "2026-02-21 11:01"
    }
  ],
  "in_progress": [
    {
      "id": "task-000",
      "title": "Ollama基础安装",
      "assigned_to": "Deploy Manager",
      "started": "2026-02-21 10:00",
      "status": "进行中",
      "progress": "85%"
    }
  ],
  "completed": [
    {
      "id": "task-999",
      "title": "websitedesign.oskris.com部署",
      "assigned_to": "Main AI",
      "completed": "2026-02-21 01:00",
      "result": "✅ 成功"
    }
  ]
}
```

---

## 使用流程

### 场景1: 主AI有多个任务

```bash
# 主AI内部思考:
# "我有5个任务要做，不应该一个个执行..."

# 1. 列出任务
tasks=(
  "下载Ollama模型:deployment:Deploy Manager:20分钟"
  "整理Downloads:file_management:File Organizer:10分钟"
  "备份workspace:backup:Backup Manager:15分钟"
  "记录今日工作:documentation:AI Dev Logger:5分钟"
)

# 2. 调用dispatcher
~/.openclaw/workspace/skills/task-dispatcher/dispatch.sh "${tasks[@]}"

# 3. Dispatcher自动:
# - 检测AI可用性
# - 分配任务
# - 发送到对应session
# - 返回任务追踪ID
```

### 场景2: 用户同时提多个需求

**用户**: "帮我整理文件、备份数据、下载Ollama模型"

**主AI响应**:
```
收到3个任务！我来安排AI团队并行处理：

📋 任务分配:
1. ✅ 整理文件 → File Organizer (预计10分钟)
2. ✅ 备份数据 → Backup Manager (预计15分钟)  
3. ✅ 下载Ollama → Deploy Manager (预计20分钟)

🚀 所有任务同时开始，预计20分钟完成！
我会在这里监控进度，有问题立即通知你。
```

### 场景3: 某个AI空闲

```bash
# AI Development Logger完成任务后:
# 自动检查是否有待处理任务

~/.openclaw/workspace/skills/task-dispatcher/check-pending.sh

# 如果有任务:
# "检测到待处理任务: 生成周报"
# "我可以处理这个任务，是否分配给我？"

# 自动分配（如果符合技能）
```

---

## 智能匹配算法

### 技能匹配
```javascript
function matchAI(task) {
  // 1. 优先匹配专长
  if (task.type === "backup" && BackupManager.isAvailable()) {
    return "Backup Manager";
  }
  
  // 2. 检查AI当前负载
  const availableAIs = getAvailableAIs();
  const leastBusy = availableAIs.sort((a, b) => 
    a.currentLoad - b.currentLoad
  )[0];
  
  // 3. 考虑AI等级（复杂任务给高等级AI）
  if (task.complexity > 7 && leastBusy.level < 3) {
    return "Main AI"; // 保留给主AI
  }
  
  // 4. 学习机会（简单任务给低等级AI学习）
  if (task.complexity <= 3) {
    return getLowestLevelAvailable();
  }
  
  return leastBusy;
}
```

### 负载均衡
```javascript
// 避免某个AI过载
function checkLoadBalance() {
  const aiLoads = {
    "Deploy Manager": 2,     // 2个任务
    "File Organizer": 0,     // 空闲
    "Backup Manager": 1,     // 1个任务
    "AI Dev Logger": 0,      // 空闲
    "Smart Dispatcher": 0    // 空闲
  };
  
  // 新任务优先分配给空闲AI
  // 避免让Deploy Manager承担第3个任务
}
```

---

## 进度监控

### 实时状态
```bash
# 查看所有任务进度
~/.openclaw/workspace/skills/task-dispatcher/status.sh

# 输出:
# 📊 AI团队任务看板
#
# 进行中 (3):
# ⏳ [Deploy Manager] 下载Ollama模型 (85%, 预计剩余3分钟)
# ⏳ [File Organizer] 整理Downloads (60%, 预计剩余4分钟)
# ⏳ [Backup Manager] 备份到VPS (40%, 预计剩余9分钟)
#
# 等待中 (1):
# ⏸️  生成学习报告 (等待AI Dev Logger空闲)
#
# 已完成 (2):
# ✅ [Smart Dispatcher] 检查iPhone存储
# ✅ [AI Dev Logger] 更新MEMORY.md
```

### 自动通知
```javascript
// 任务完成时自动通知主AI
onTaskComplete((task) => {
  notifyMainAI({
    message: `✅ ${task.assigned_to} 完成: ${task.title}`,
    result: task.result,
    next_action: task.next_action
  });
});

// 任务失败时立即通知
onTaskFail((task) => {
  notifyMainAI({
    message: `❌ ${task.assigned_to} 失败: ${task.title}`,
    error: task.error,
    suggestion: task.fallback_plan
  });
});
```

---

## 冲突检测

### 资源冲突
```javascript
// 避免多个AI同时访问同一文件
const conflicts = [
  {
    "resource": "/Users/oskris/Downloads/",
    "locked_by": "File Organizer",
    "reason": "整理中，请勿访问"
  },
  {
    "resource": "VPS:/root/backup/",
    "locked_by": "Backup Manager",
    "reason": "备份中"
  }
];

// 检测冲突
function canAssignTask(task, ai) {
  if (task.resources.some(r => isLocked(r))) {
    return false; // 资源被占用
  }
  return true;
}
```

### 依赖检测
```javascript
// 任务依赖关系
const dependencies = {
  "task-002": ["task-001"], // 任务2依赖任务1完成
  "task-003": ["task-001", "task-002"]
};

// 只有依赖完成后才分配任务
function canStartTask(task) {
  const deps = dependencies[task.id] || [];
  return deps.every(depId => isCompleted(depId));
}
```

---

## 失败处理

### 自动重试
```javascript
const retryPolicy = {
  "max_retries": 3,
  "backoff": "exponential", // 1s, 2s, 4s
  "fallback_ai": true       // 失败后尝试其他AI
};

// 示例:
// Deploy Manager下载失败 → 等待2秒
// Deploy Manager再次失败 → 等待4秒
// Deploy Manager第三次失败 → 切换到Smart Dispatcher
```

### 降级策略
```javascript
// 复杂任务失败 → 简化任务
// 示例: "完整备份"失败 → 改为"关键文件备份"

// 或者升级到主AI
// 示例: Level 1 AI失败3次 → 主AI接手
```

---

## 学习和优化

### 记录执行数据
```json
{
  "task_id": "task-001",
  "title": "下载Ollama模型",
  "assigned_to": "Deploy Manager",
  "estimated_time": 1200,  // 20分钟
  "actual_time": 900,      // 实际15分钟
  "success": true,
  "notes": "网络良好，比预期快"
}
```

### 优化估算
```javascript
// 根据历史数据优化时间估算
function improveEstimate(taskType) {
  const history = getTaskHistory(taskType);
  const avgTime = average(history.map(t => t.actual_time));
  
  // 更新估算
  updateEstimate(taskType, avgTime);
}
```

---

## 集成示例

### 在主AI中使用
```bash
# 主AI接收到多个任务
tasks=(
  "下载模型"
  "整理文件"  
  "备份数据"
)

# 自动分配
for task in "${tasks[@]}"; do
  dispatch_task "$task"
done

# 监控进度
watch_progress

# 等待完成
wait_all_tasks
```

### OpenClaw sessions集成
```javascript
// 使用sessions_spawn创建子任务
const taskId = await sessions_spawn({
  task: "下载Ollama Qwen 2.5 14B模型",
  agentId: "deploy-manager",
  label: "ollama-download"
});

// 追踪任务
const status = await sessions_list({
  label: "ollama-download"
});
```

---

## 安全和权限

### 任务权限检查
```javascript
// 某些任务只能主AI执行
const restrictedTasks = [
  "修改核心配置",
  "删除重要文件",
  "执行sudo命令"
];

// 分配前检查
function canAssign(task, ai) {
  if (restrictedTasks.includes(task.type) && ai !== "Main AI") {
    return false;
  }
  return true;
}
```

### 审批流程
```javascript
// 高风险任务需要主AI批准
const highRiskTasks = ["删除", "格式化", "重启服务器"];

if (isHighRisk(task)) {
  await requestApproval(task);
}
```

---

## 最佳实践

### ✅ 适合并行的任务
- 独立的任务（无依赖）
- 不冲突的资源
- 相似的预期时间
- 每个AI的专长领域

### ❌ 不适合并行的任务
- 有依赖关系的任务
- 需要顺序执行的步骤
- 共享同一资源
- 需要主AI决策的任务

---

## 示例场景

### 场景: 早晨例行检查

**主AI**:
```bash
# 早晨7点，heartbeat触发
# 检测到5个例行任务

dispatch_tasks \
  "检查邮件:Smart Dispatcher" \
  "整理Downloads:File Organizer" \
  "检查VPS状态:Backup Manager" \
  "生成昨日总结:AI Dev Logger" \
  "查看今日日程:Smart Dispatcher"

# 5个任务并行执行，3分钟内全部完成
# 主AI收到汇总报告，一次性展示给用户
```

---

## 总结

**核心价值**:
1. **效率提升** - 并行工作，时间节省2-5倍
2. **资源优化** - 充分利用所有AI
3. **学习机会** - AI在实战中成长
4. **负载均衡** - 避免主AI过载

**使用原则**: 能并行就并行，让每个AI发挥专长！
