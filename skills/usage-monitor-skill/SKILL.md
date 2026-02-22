# Usage Monitor Skill

## 职责
监控OpenClaw和Claude.ai的token/context使用，自动预警

## 监控指标
- Context使用率（%）
- Token消耗速率（token/分钟）
- 预计剩余时间
- 成本追踪

## 预警阈值
- 75%: 注意
- 85%: 警告
- 90%: 危险，建议compact
- 95%: 紧急

## 工作流程
1. 每15分钟运行 session_status
2. 计算速率和预测
3. 记录到logs/usage-log.json
4. 超过阈值立刻警告主AI

## 报告格式
```
Context: X%
Token速率: Y/分钟
预计剩余: Z小时
建议: [compact/继续/警告]
```
