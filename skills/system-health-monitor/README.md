# System Health Monitor

一条命令快速了解整个系统状态，避免重复执行多个检查命令。

## 快速开始

```bash
# 完整检查
~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh

# JSON输出
~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh --json

# Silent模式（仅在有问题时输出）
~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh --silent
```

## 使用场景

- ✅ 系统刚重启，快速确认状态
- ✅ 接收新任务前，确保资源充足
- ✅ 备份任务前，检查磁盘空间
- ✅ 调试问题时，收集系统信息
- ✅ Heartbeat检查

## 检查项目

- 系统运行时间和负载
- 磁盘使用（/ 和 /Users）
- 内存使用
- 关键进程（Ollama, rsync, OpenClaw）
- 网络连通性（VPS）
- iPhone连接状态
- 智能建议

## 详细文档

参考 `SKILL.md` 了解完整功能和高级用法。
