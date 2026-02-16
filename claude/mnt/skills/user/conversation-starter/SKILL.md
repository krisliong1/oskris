# Conversation Starter Skill

## 触发条件
每次新对话开始时自动触发

## 执行流程
1. 读取所有 /mnt/skills/user/ 下的 Skills
2. 从 VPS 读取敏感配置（不存 GitHub）
3. 从 GitHub 读取项目记忆
4. 报告当前状态

## 安全规则
⛔ Token/API Key 绝对不存 GitHub
✅ 只存 VPS: /root/.oskris/config.json
✅ 聊天中不显示完整 Token

## CLAUDE.md 核心原则
- 先 Plan 后 Execute
- 每次读取 CLAUDE.md
- API Key 安全管理
