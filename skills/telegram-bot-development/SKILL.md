---
name: telegram-bot-development
description: Oskris Telegram AI Agent开发。Python+Claude API+工具系统完整架构。基于VPS部署的生产环境经验。
---

# Telegram Bot Development Skill

## 架构设计

### 系统组件
```
Telegram Bot API ←→ Python Gateway (VPS) ←→ Claude API
                                              ↓
                                    Skills系统 + 文件操作 + GitHub
```

### 核心文件结构
```
oskris-agent/
├── bot.py          # Telegram Bot主程序
├── agent.py        # Claude API集成+工具调用
├── tools.py        # 工具函数(文件、GitHub、VPS)
├── memory.py       # 对话记忆管理
├── config.py       # 配置管理
└── system_prompt.md # 系统提示词
```

## 技术栈

### 框架选择
- **Python 3.11+** 
- **python-telegram-bot** (异步框架)
- **anthropic SDK** (Claude API)
- **aiofiles** (异步文件操作)

### API集成
- **Telegram Bot API**: 消息收发
- **Claude API**: AI推理+工具调用
- **GitHub API**: 代码同步
- **Hostinger API**: VPS管理

## 工具系统设计

### 工具定义结构
```python
TOOL_DEFINITIONS = [
    {
        "name": "execute_command",
        "description": "Execute shell commands on VPS",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string"},
                "working_dir": {"type": "string"}
            }
        }
    }
]
```

### 工具执行循环
```python
def tool_use_loop(message):
    response = claude_api.call(message, tools=TOOL_DEFINITIONS)
    while response.tool_calls:
        for tool_call in response.tool_calls:
            result = execute_tool(tool_call)
            response = claude_api.continue_conversation(result)
    return response.content
```

## 记忆管理

### 对话记忆
- **短期**: 最近50轮对话
- **长期**: 重要决策和学习成果
- **检索**: 语义搜索相关上下文

### Context Window管理
- **监控**: 实时跟踪token用量
- **警告**: 20-30%开始提醒
- **压缩**: 自动总结旧对话
- **重置**: 40%以上强制新对话

## 部署配置

### VPS环境
```bash
# Ubuntu 25.10
# Python 3.11+
# SSH密钥认证
# systemd服务管理
```

### 环境变量
```python
TELEGRAM_BOT_TOKEN = "bot_token"
ANTHROPIC_API_KEY = "claude_key" 
GITHUB_TOKEN = "github_token"
HOSTINGER_API_KEY = "hostinger_key"
```

### 服务监控
```bash
systemctl status oskris-agent
journalctl -f -u oskris-agent
```

## 实战经验

### 性能优化
- 异步处理提升50%响应速度
- 工具调用缓存减少重复API调用
- Context压缩节省30% token

### 错误处理
- API限流重试机制
- 网络异常自动恢复  
- 工具执行超时保护

### 用户体验
- 华文回复 + 英文代码
- 实时进度反馈
- 错误信息人性化

---
*基于Oskris Agent生产环境运行经验*