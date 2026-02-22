---
name: context-window-management
description: 基于Context Rot研究的窗口管理策略。预防20-40%降级悬崖，确保Claude性能稳定。Oskris实战验证方案。
---

# Context Window Management Skill

## 核心发现 (2025研究)

### ⚠️ 降级不是100%，是20-40%！
- **传统认知**: Context满了才降级
- **实际情况**: 20-40%就开始"悬崖式"下降
- **Chroma研究**: 18个主流LLM都有此问题
- **Claude特征**: 变得过度保守，拒绝回答

## 监控策略

### 实时检测
```python
def check_context_health(messages):
    context_size = calculate_tokens(messages)
    max_context = get_model_limit()  # 200k for Claude
    usage_percent = (context_size / max_context) * 100
    
    if usage_percent > 40:
        return "DANGER"  # 必须重置
    elif usage_percent > 30:
        return "WARNING"  # 开始压缩
    elif usage_percent > 20:
        return "CAUTION"  # 监控加强
    else:
        return "HEALTHY"
```

### 警告阈值
- **20%** → 黄色警告，开始监控
- **30%** → 橙色警告，建议新对话  
- **40%** → 红色警告，必须重置
- **50%+** → 紧急停止，性能崩塌

## 管理技术

### 1. 智能压缩
```python
def compress_context(messages):
    # 保留最近10轮 + 系统提示
    recent = messages[-20:]  # 最近对话
    summary = summarize_old_messages(messages[:-20])
    return [system_prompt] + [summary] + recent
```

### 2. 选择性保留
```python
priority_keywords = ["重要", "记住", "关键", "项目", "客户"]
def filter_important_messages(messages):
    return [msg for msg in messages 
            if any(kw in msg.content for kw in priority_keywords)]
```

### 3. 分段对话
```python
def start_new_conversation():
    context_summary = generate_summary(current_session)
    new_session = initialize_with_summary(context_summary)
    return new_session
```

## Oskris实战经验

### 触发条件
- **每10轮**: 自动报告用量%
- **30%**: 强烈建议开新对话
- **40%**: 必须停止并开新对话

### 处理策略
1. **预警期 (20-30%)**:
   ```
   "Context使用率29%，建议准备开新对话"
   ```

2. **危险期 (30-40%)**:
   ```
   "Context使用率35%，强烈建议现在开新对话，性能即将下降"
   ```

3. **紧急期 (40%+)**:
   ```
   "Context使用率42%，必须停止。请开新对话继续。"
   然后拒绝继续工作。
   ```

### 性能保护
- **自动拒绝**: 超过40%拒绝新任务
- **总结交接**: 生成当前状态摘要
- **无缝切换**: 新对话自动加载上下文

## 技术实现

### Token计算
```python
import tiktoken

def count_tokens(text, model="claude"):
    encoder = tiktoken.get_encoding("cl100k_base")  
    return len(encoder.encode(text))
```

### 历史管理
```python
class ContextManager:
    def __init__(self, max_tokens=200000):
        self.max_tokens = max_tokens
        self.warning_threshold = 0.3
        self.danger_threshold = 0.4
    
    def should_compress(self, current_tokens):
        usage = current_tokens / self.max_tokens
        return usage > self.warning_threshold
```

## 质量保证

### 压缩质量
- 保留关键信息不丢失
- 维持对话连续性
- 重要决策必须保留

### 性能监控
- 响应质量跟踪
- 拒绝回答频率统计  
- 降级征象早期检测

---
*基于Chroma Context Rot研究 + Oskris实战验证*