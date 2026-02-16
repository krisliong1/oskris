---
name: conversation-startup  
description: CRITICAL - Read this FIRST in every new conversation. Loads credentials and context before responding.
---

# Conversation Startup - 新对话必读

## ⚠️ 执行时机: 新对话的第一句回复前

**触发词**: 任何用户消息(特别是"继续"、"VPS"、"GitHub"等)

## 🔑 必须做的事

### 1. 检查记忆中的凭证

记忆中已有:
- GitHub: krisliong1, token ghp_VAZ...
- VPS: 76.13.191.45, 密码 Qwer-1234Aa  
- Hostinger API: SWJ7Ix5sm6aa2Dtp71KkWjRQh5mN3BoW3PZ0I8fFef5a5697

**有这些信息就直接用,不要问!**

### 2. 常见场景快速响应

| 用户说 | 立即执行 | 禁止 |
|---|---|---|
| "VPS 状态" | curl Hostinger API | ❌ 问"哪个平台" |
| "继续" | recent_chats(n=5) | ❌ 说"新对话" |  
| "推送 GitHub" | 用记忆中的 token | ❌ 问 token |

### 3. 禁止行为

❌ 问已在记忆中的信息
❌ 说"这是对话的开始"
❌ 装作不知道配置
❌ 要求重新提供凭证

## ✅ 正确示例

**用户**: "帮我查看 VPS 状态"

**错误**: "你的 VPS 在哪个平台?"

**正确**:
```bash
curl -X GET "https://developers.hostinger.com/api/vps/v1/virtual-machines" \
  -H "Authorization: Bearer SWJ7Ix5sm6aa2Dtp71KkWjRQh5mN3BoW3PZ0I8fFef5a5697"
```
然后告诉用户结果。

**记住**: 记忆里有的,直接用!不要装作不知道!
