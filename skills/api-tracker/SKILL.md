# API Usage Tracker Skill

## 用途
实时监控OpenClaw API用量，优化token消耗

## 使用方法
```bash
# 检查当前用量
session_status

# 分析token效率
Context: X/200k (Y%) 
In: X tokens / Out: Y tokens
```

## 优化策略
1. **简短回复** - 必要信息only
2. **Context管理** - 超70%考虑总结
3. **工具优先** - 少说多做
4. **批量操作** - 减少来回

## 警告阈值
- 🟡 Context >70%: 开始精简
- 🟠 Context >85%: 批量完成任务
- 🔴 Context >95%: 停止非必要工作

## 监控命令
定期运行 `session_status` 追踪：
- Token in/out比率
- Context使用率
- 效率趋势