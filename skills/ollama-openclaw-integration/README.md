# Ollama-OpenClaw Integration

**让OpenClaw的AI团队使用免费本地Ollama模型，大幅降低成本！**

## 快速开始

### 1. 测试调用（等模型下载完成）
```bash
# 简单问答
~/.openclaw/workspace/skills/ollama-openclaw-integration/call.sh qwen2.5:14b "你好"

# 文件分类任务
~/.openclaw/workspace/skills/ollama-openclaw-integration/call.sh qwen2.5:14b "列出Downloads常见的文件类型"

# 代码生成
~/.openclaw/workspace/skills/ollama-openclaw-integration/call.sh qwen2.5:7b "写一个检查磁盘空间的bash脚本"
```

### 2. 在OpenClaw中使用
```javascript
// 主AI调用Ollama处理简单任务
const result = await exec({
  command: "~/.openclaw/workspace/skills/ollama-openclaw-integration/call.sh",
  args: ["qwen2.5:14b", "整理Downloads文件夹的建议"]
});

// 免费！不消耗Claude token
```

## 成本对比

**Before** (全部用Claude):
- 简单任务：90个/天 × 500 tokens = 45,000 tokens/天
- 复杂任务：10个/天 × 5,000 tokens = 50,000 tokens/天
- **总计：95,000 tokens/天 = $2/天 = $60/月**

**After** (混合模式):
- 简单任务：90个/天 × Ollama = **$0**
- 复杂任务：10个/天 × 5,000 tokens = 50,000 tokens/天
- **总计：50,000 tokens/天 = $1/天 = $30/月**

**节省：50% ($30/月)**

## 任务分配

### 用Ollama（免费）
- ✅ 创建新对话
- ✅ 整理文件
- ✅ 检查系统状态
- ✅ 简单分类
- ✅ 记录日志
- ✅ 文本提取
- ✅ 基础代码生成

### 用Claude（付费）
- 🎯 复杂推理
- 🎯 架构设计
- 🎯 创意工作
- 🎯 关键决策
- 🎯 深度分析

## 可用模型

- **qwen2.5:14b** - 中文优化，通用任务（推荐）
- **qwen2.5:7b** - 轻量版，速度更快
- **deepseek-coder:6.7b** - 代码专用
- **llama3.3:8b** - 英文通用

## 详细文档

参考 `SKILL.md` 了解完整设计理念和高级用法。

## 当前状态

⏳ Deploy Manager正在下载模型...
- qwen2.5:14b (约8GB)
- qwen2.5:7b (约4GB)

预计15-20分钟完成。
