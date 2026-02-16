---
name: memory-updater
description: 自动更新Claude记忆。检测到用户提供新信息时自动保存到记忆系统，确保重要信息不丢失。记忆更新后同步推送到GitHub备份。
---

# Memory Updater

检测到重要信息时自动更新记忆，不需要用户要求。

## 触发条件

用户消息包含以下类型信息时自动触发：

- **凭证类**：GitHub token、API key、密码、SSH密钥
- **配置类**：服务器IP、域名、邮箱、仓库地址
- **偏好类**：「记住我喜欢...」「以后都...」「永远不要...」
- **身份类**：工作变动、联系方式更新、新项目启动
- **指令类**：「别忘了」「记住」「以后」「永远」

## 执行流程

1. **检查现有记忆** → `memory_user_edits view`
2. **判断是否重复** → 已存在则跳过或更新
3. **保存** → `memory_user_edits add "[简洁描述]"`
4. **静默完成** → 不主动告诉用户「已保存」，除非用户要求确认

## 记忆格式

简洁，易查找：

```
✅ 好: "GitHub token: ghp_xxx for krisliong1/oskris"
✅ 好: "用户偏好TypeScript"
❌ 坏: "用户在2026年2月16日告诉我他的GitHub token是..."
```

## 记忆同步到GitHub

每次更新记忆后，推送到 `notes/memory/claude-memory.md`：

```bash
cd /tmp/oskris
# 更新记忆备份文件
git add notes/memory/
git commit -m "update: Sync memory backup"
git push origin main
```

## 不保存的内容

- 临时性信息（今天吃什么）
- 一次性任务细节
- 闲聊内容
- 已存在的重复信息

## 敏感信息规则

- Token/密码/API key：存记忆 + VPS，禁止存GitHub代码
- 个人敏感信息（身份证、银行账号）：仅存记忆，不存任何文件
