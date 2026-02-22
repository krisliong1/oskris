# Smart AI Dispatcher - 智能AI调度系统

## 理念
**三个方案合并成一个自动调度系统**

## 三层架构

```
用户任务
    ↓
智能调度AI（判断复杂度）
    ↓
├─ 简单任务 → Ollama本地 (免费、快速、离线)
├─ 中等任务 → 豆包 (免费、全能、需网络)
└─ 复杂任务 → Claude (付费、最强)
```

## 调度规则

### Level 1: Ollama本地 (优先)
**适用任务**：
- 文件分类/重命名
- 简单代码生成
- 基础知识问答
- 文本格式转换
- 日志分析

**优势**：
- 免费
- 快速（本地推理）
- 离线可用
- 隐私保护

**限制**：
- 复杂推理能力弱
- 知识截止日期
- 专业深度有限

### Level 2: 豆包 (辅助)
**适用任务**：
- Ollama处理不了的
- 需要较新知识的
- 中文理解要求高的
- 多步骤任务规划

**优势**：
- 免费
- 全能（高级技工水平）
- 中文友好
- 知识较新

**限制**：
- 需要网络
- 依赖第三方服务
- 响应可能较慢

### Level 3: Claude (兜底)
**适用任务**：
- 前两者都失败的
- 复杂多步推理
- 专业深度知识
- 关键决策

**优势**：
- 最强能力
- 专业深度
- 可靠性高

**限制**：
- 昂贵（$17.69已花费）
- 应该少用

## 智能调度AI

### 职责
1. **接收用户任务**
2. **分析任务复杂度**
3. **选择最优AI**
4. **执行并验证**
5. **失败自动降级/升级**

### 判断逻辑

```python
def dispatch_task(task):
    complexity = analyze_complexity(task)
    
    # 尝试Ollama（免费优先）
    if complexity <= 3:
        result = try_ollama(task)
        if result.success:
            return result
    
    # 降级到豆包（免费辅助）
    if complexity <= 7:
        result = try_doubao(task)
        if result.success:
            return result
    
    # 最后用Claude（付费兜底）
    result = use_claude(task)
    return result
```

### 复杂度评分 (1-10)

#### 1-3分：Ollama
- 文件操作
- 简单分类
- 格式转换
- 基础问答

#### 4-7分：豆包
- 代码生成（中等）
- 任务规划
- 知识查询
- 文档总结

#### 8-10分：Claude
- 复杂推理
- 架构设计
- 关键决策
- 专业深度问题

## 实现方案

### Dispatcher AI工作流

```
1. 接收任务
    ↓
2. 分析任务类型和复杂度
    ↓
3. 选择AI：
    - 文件整理 → Ollama
    - 代码生成 → 尝试Ollama → 失败用豆包
    - 架构设计 → 直接Claude
    ↓
4. 执行并记录：
    - 成功率
    - 响应时间
    - 成本
    ↓
5. 优化调度策略（学习）
```

### 接口统一

```javascript
// 统一调用接口
async function askAI(question, options = {}) {
  const task = {
    question,
    complexity: options.complexity || 'auto',
    forceAI: options.force // 'ollama', 'doubao', 'claude'
  };
  
  return await dispatcher.route(task);
}

// 例子
await askAI("整理Downloads文件夹"); 
// → 自动路由到Ollama

await askAI("设计一个分布式备份系统");
// → 自动路由到Claude
```

## 豆包集成方式

### 方式1: iOS快捷指令桥接
```
OpenClaw → HTTP请求 → iPhone快捷指令 → 豆包App → 返回结果
```

**实现**：
1. 创建快捷指令："豆包问答桥"
2. 监听HTTP请求（个人自动化服务器）
3. 调用豆包App
4. 返回JSON结果

### 方式2: 网页版自动化
```
OpenClaw → Browser工具 → 豆包网页版 → 抓取答案
```

**实现**：
1. `browser.open("豆包网页版")`
2. `browser.type(问题)`
3. `browser.wait(回答)`
4. `browser.extract(文本)`

### 方式3: 直接API（如果有）
```
OpenClaw → HTTP请求 → 豆包API → 返回结果
```

## Ollama配置

### 推荐模型

#### Qwen 2.5 (中文优化)
```bash
ollama pull qwen2.5:14b
# 14B参数，中文友好，M4可以跑
```

#### Llama 3.3 (通用)
```bash
ollama pull llama3.3:70b
# 70B参数，能力强，但可能慢
```

#### DeepSeek Coder (代码专用)
```bash
ollama pull deepseek-coder:6.7b
# 代码生成专用，轻量快速
```

### 启动服务
```bash
# 后台运行Ollama服务
ollama serve &

# 测试
ollama run qwen2.5:14b "你好，请介绍一下自己"
```

## 调度AI的MEMORY结构

```markdown
# Smart Dispatcher 记忆文件

## 任务路由统计

### Ollama (本地)
- 总任务数: 245
- 成功率: 87%
- 平均响应时间: 2.3s
- 成本: $0

**擅长**：
- 文件分类 (98%成功率)
- 简单代码 (85%成功率)
- 格式转换 (95%成功率)

**不擅长**：
- 复杂推理 (34%成功率)
- 专业知识 (56%成功率)

### 豆包 (免费在线)
- 总任务数: 123
- 成功率: 92%
- 平均响应时间: 5.1s
- 成本: $0

**擅长**：
- 中文理解 (97%成功率)
- 任务规划 (89%成功率)
- 知识查询 (93%成功率)

**不擅长**：
- 深度推理 (67%成功率)

### Claude (付费兜底)
- 总任务数: 45
- 成功率: 98%
- 平均响应时间: 3.8s
- 成本: $23.45

**擅长**：
- 所有任务 (98%+成功率)

## 优化策略

### 学到的规则
1. 文件整理优先Ollama（98%成功，0成本）
2. 中文任务优先豆包（中文理解强）
3. 代码生成先Ollama尝试，失败降级豆包
4. 复杂推理直接Claude（避免浪费时间）

### 成本优化
- 总任务: 413
- Ollama处理: 245 (59%)
- 豆包处理: 123 (30%)
- Claude处理: 45 (11%)
- **总成本节省**: 约$150+ (如果全用Claude)
```

## Dispatcher AI Workspace

```
~/.openclaw/ai-team/smart-dispatcher/
├── MEMORY.md              # 调度统计和学习
├── routing-rules.json     # 路由规则
├── task-history/          # 任务历史
├── performance-log.json   # 性能记录
└── cost-tracking.json     # 成本追踪
```

## 创建Dispatcher AI

```bash
# Spawn常驻Dispatcher
sessions_spawn \
  --label smart-dispatcher \
  --task "你是智能AI调度员，负责分析任务复杂度并路由到最优AI（Ollama/豆包/Claude）。读取~/.openclaw/ai-team/smart-dispatcher/MEMORY.md学习调度策略。" \
  --cleanup keep
```

## 使用示例

### 用户视角（透明）
```
用户: "帮我整理Downloads文件夹"
    ↓
Dispatcher分析: 简单任务，复杂度2
    ↓
路由到: Ollama本地
    ↓
Ollama执行: 成功
    ↓
用户: 收到结果（不知道是哪个AI处理的）
```

### 失败自动降级
```
用户: "设计一个智能备份系统架构"
    ↓
Dispatcher: 复杂度6，尝试豆包
    ↓
豆包: 回答不够深入（质量评分5/10）
    ↓
Dispatcher: 自动升级到Claude
    ↓
Claude: 提供专业方案（质量9/10）
    ↓
用户: 收到高质量答案
```

## 成本预测

### 当前（全Claude）
- 每月任务: ~400
- 成本: ~$70/月

### 优化后（智能调度）
```
Ollama处理: 240任务 (60%) → $0
豆包处理: 120任务 (30%) → $0
Claude处理: 40任务 (10%) → $7

总成本: $7/月
节省: $63/月 (90%)
```

## 质量保证

### 验证机制
```
1. Ollama处理后验证结果质量
2. 质量<7分 → 自动用豆包重做
3. 豆包质量<7分 → 升级Claude
4. 记录每次选择的准确性
5. 持续优化调度规则
```

### 学习反馈
```
用户满意 → 强化该路由规则
用户不满意 → 调整复杂度评分
```

## 下一步实现

### 阶段1: 基础设施（本周）
- [ ] Ollama安装和配置
- [ ] 测试Ollama基础能力
- [ ] 豆包集成方案确定
- [ ] 创建Dispatcher AI

### 阶段2: 智能路由（2周内）
- [ ] 实现复杂度分析
- [ ] 实现三层路由
- [ ] 添加失败降级/升级
- [ ] 性能和成本追踪

### 阶段3: 优化学习（1月内）
- [ ] 收集100+任务数据
- [ ] 优化路由规则
- [ ] 提升Ollama成功率到90%+
- [ ] 实现自动学习优化

## 成功指标

### 短期（1周）
- Ollama可用并处理简单任务
- 豆包集成至少一种方式可用
- Dispatcher AI创建并运行

### 中期（1月）
- 60%任务由Ollama处理
- 30%任务由豆包处理
- Token成本降低80%+

### 长期（3月）
- 90%任务免费处理
- 响应速度提升50%+
- 用户满意度>90%
