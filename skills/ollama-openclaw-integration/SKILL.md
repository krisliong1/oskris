# Ollama-OpenClaw Integration Skill

## 目的
**让OpenClaw的AI团队使用本地Ollama模型处理简单任务，大幅降低成本。**

## 核心理念

### 用户的聪明想法 💡
"为什么系统管理任务要消耗token？让AI帮你创建新对话框、整理文件这些简单任务，用离线免费的Ollama就够了！"

**完全正确** ✅

---

## 成本对比

### 当前模式（全部用Claude）❌
```
创建新对话 → Claude Sonnet ($$$)
整理文件   → Claude Sonnet ($$$)
检查状态   → Claude Sonnet ($$$)
简单分类   → Claude Sonnet ($$$)
记录文档   → Claude Sonnet ($$$)

月成本: ~$70
```

### 混合模式（Ollama + Claude）✅
```
创建新对话 → Ollama Qwen (免费)
整理文件   → Ollama Qwen (免费)
检查状态   → Ollama Qwen (免费)
简单分类   → Ollama Qwen (免费)
记录文档   → Ollama Qwen (免费)
复杂推理   → Claude Sonnet ($$$)
架构设计   → Claude Sonnet ($$$)

月成本: ~$7 (90%节省)
```

---

## OpenClaw Ollama支持现状

### 当前情况
OpenClaw配置支持的providers:
- ✅ anthropic (Claude)
- ✅ openai (GPT)
- ✅ google (Gemini)
- ✅ groq
- ❌ ollama (尚未直接支持)

### 临时解决方案（可用）

#### 方案1: exec直接调用 ⭐推荐
```bash
# 通过exec工具直接调用ollama命令
result=$(exec ollama run qwen2.5:14b "帮我创建一个新对话，标题是Ollama配置")
```

**优点**:
- ✅ 立即可用
- ✅ 不需要修改配置
- ✅ 完全免费

**缺点**:
- ⚠️ 需要手动解析输出
- ⚠️ 没有统一的AI接口

#### 方案2: cliBackends配置
```json
{
  "agents": {
    "defaults": {
      "cliBackends": {
        "ollama-qwen": {
          "command": "/usr/local/bin/ollama",
          "args": ["run", "qwen2.5:14b"],
          "modelArg": "--model"
        }
      }
    }
  }
}
```

**优点**:
- ✅ 统一接口
- ✅ OpenClaw原生支持

**缺点**:
- ⚠️ 需要测试配置格式
- ⚠️ 文档不完整

#### 方案3: 等待官方支持
OpenClaw后续版本可能会直接支持Ollama provider

---

## 实现方案

### 架构设计

**系统管理Agent** (免费):
```json
{
  "id": "system-manager",
  "name": "System Manager",
  "workspace": "~/.openclaw/ai-team/system-manager",
  "backend": "ollama-qwen",  // 使用Ollama
  "tasks": [
    "创建新对话",
    "整理文件",
    "检查系统状态",
    "简单分类",
    "记录日志"
  ]
}
```

**专业Agent** (付费):
```json
{
  "id": "main",
  "name": "Main AI",
  "workspace": "~/.openclaw/workspace",
  "model": "anthropic/claude-sonnet-4-5",  // 继续用Claude
  "tasks": [
    "复杂推理",
    "架构设计",
    "代码生成",
    "创意工作"
  ]
}
```

---

## 使用场景

### 场景1: 创建新对话

**错误做法** ❌:
```
主AI(Claude): 好的，我来创建新对话...
消耗token: ~500 tokens = $0.01
```

**正确做法** ✅:
```
主AI: @system-manager 创建新对话 "Ollama配置"
系统管理AI(Ollama): 好的，创建完成
消耗token: 0 (本地执行)
成本: $0
```

### 场景2: 整理Downloads

**错误做法** ❌:
```
主AI(Claude): 扫描文件...分类...移动...
消耗token: ~2000 tokens = $0.04
```

**正确做法** ✅:
```
主AI: @file-organizer 整理Downloads
File Organizer(Ollama): 完成，移动了50个文件
消耗token: 0
成本: $0
```

### 场景3: 复杂任务（继续用Claude）

```
主AI(Claude): 设计三合一AI架构...
这种复杂任务值得用Claude
消耗token: ~5000 tokens = $0.10
成本合理
```

---

## 实战配置

### 步骤1: 下载Ollama模型
```bash
# 已完成基础安装
ollama --version  # 0.16.3

# 下载模型（需要执行）
ollama pull qwen2.5:14b     # 中文优化，8GB
ollama pull qwen2.5:7b      # 轻量版，4GB
```

### 步骤2: 测试Ollama
```bash
# 测试命令行调用
ollama run qwen2.5:14b "列出~/Downloads里的文件类型"

# 预期输出:
# 我会帮你分析Downloads文件夹...
# PDF: 10个
# 图片: 25个
# 安装包: 3个
```

### 步骤3: 创建调用函数
```bash
# ~/.openclaw/workspace/skills/ollama-openclaw-integration/call-ollama.sh

#!/bin/bash
model="${1:-qwen2.5:14b}"
prompt="$2"

result=$(ollama run "$model" "$prompt" 2>&1)
echo "$result"
```

### 步骤4: 在OpenClaw中使用
```javascript
// 主AI调用Ollama处理简单任务
const simpleTask = "整理Downloads文件夹";

// 使用exec调用
const result = await exec({
  command: "~/.openclaw/workspace/skills/ollama-openclaw-integration/call-ollama.sh",
  args: ["qwen2.5:14b", simpleTask]
});

// Ollama返回结果，免费！
```

---

## 任务路由规则

### 自动分类

**复杂度1-3** → Ollama (免费):
- 文件操作 (ls, cat, mv)
- 简单分类
- 文本提取
- 日志记录

**复杂度4-7** → Ollama (免费):
- 代码片段生成
- 文件整理逻辑
- 简单问答
- 数据转换

**复杂度8-10** → Claude (付费):
- 架构设计
- 复杂推理
- 创意工作
- 关键决策

---

## 实际效果预测

### 每日任务分布
```
总任务: 100个/天

系统管理: 60个 → Ollama (免费)
  - 文件操作: 20个
  - 状态检查: 15个
  - 日志记录: 15个
  - 简单分类: 10个

中等任务: 30个 → Ollama (免费)
  - 代码生成: 15个
  - 文档整理: 10个
  - 数据转换: 5个

复杂任务: 10个 → Claude (付费)
  - 架构设计: 3个
  - 深度分析: 4个
  - 创意工作: 3个
```

### 成本计算
```
Claude任务: 10个 × 5000 tokens × $0.02/1000 = $1/天
Ollama任务: 90个 × 0 = $0/天

日成本: $1
月成本: ~$30 → 实际可能更低（不是每天都100个任务）

对比原来$70/月，节省57%
```

---

## 未来展望

### OpenClaw原生支持（等待）
```json
{
  "agents": {
    "list": [
      {
        "id": "system-manager",
        "model": "ollama/qwen2.5:14b",  // 未来可能支持
        "workspace": "~/.openclaw/ai-team/system-manager"
      },
      {
        "id": "main",
        "model": "anthropic/claude-sonnet-4-5",
        "workspace": "~/.openclaw/workspace"
      }
    ]
  }
}
```

### 智能路由器
```javascript
// Smart Dispatcher自动选择模型
function selectModel(task) {
  const complexity = analyzeComplexity(task);
  
  if (complexity <= 7) {
    return "ollama/qwen2.5:14b";  // 免费
  } else {
    return "anthropic/claude-sonnet-4-5";  // 付费
  }
}
```

---

## 立即可用方案

### 创建系统管理器
```bash
# 1. 下载模型
ollama pull qwen2.5:14b

# 2. 创建调用脚本
mkdir -p ~/.openclaw/workspace/skills/ollama-openclaw-integration
cat > ~/.openclaw/workspace/skills/ollama-openclaw-integration/call.sh << 'EOF'
#!/bin/bash
ollama run qwen2.5:14b "$1"
EOF
chmod +x ~/.openclaw/workspace/skills/ollama-openclaw-integration/call.sh

# 3. 测试
~/.openclaw/workspace/skills/ollama-openclaw-integration/call.sh "你好"
```

### 在主AI中使用
```javascript
// 简单任务 → Ollama
if (taskComplexity <= 7) {
  const result = await exec({
    command: "~/.openclaw/workspace/skills/ollama-openclaw-integration/call.sh",
    args: [taskDescription]
  });
  return result;
}

// 复杂任务 → 继续用Claude
else {
  // 正常处理
}
```

---

## 总结

**核心价值**:
1. **成本大幅降低** - 90%任务用免费Ollama
2. **立即可用** - 通过exec调用，不等官方支持
3. **智能分配** - 简单任务Ollama，复杂任务Claude
4. **完全离线** - Ollama本地运行，不需网络

**使用原则**: 
- 系统管理 → Ollama
- 专业工作 → Claude
- 自动路由 → Smart Dispatcher

**下一步**: 下载Ollama模型，测试调用，然后逐步迁移简单任务到Ollama！
