# Conversation Manager Skill

## 目的
**主动管理对话分类，避免一个对话涵盖太多主题，让每个对话都有清晰的主题和目标。**

## 设计理念

### 问题
- ❌ 一个对话混杂多个主题（网站部署 + 备份 + AI团队 + Ollama...）
- ❌ 想回到某个话题，要翻很久的历史记录
- ❌ 对话标题不清晰，难以快速找到
- ❌ Token消耗快，context window压力大

### 解决方案
- ✅ 按主题开启新对话
- ✅ 每个对话有清晰的标题和目标
- ✅ 追踪对话状态（进行中/已完成/待续）
- ✅ 轻松切换回特定话题

---

## 对话分类原则

### 何时开启新对话

#### 1️⃣ 新项目开始
```
❌ 错误: 在"系统维护"对话中讨论新网站设计
✅ 正确: 开启新对话 "ABC公司网站设计"
```

#### 2️⃣ 新技术学习
```
❌ 错误: 在"日常任务"对话中学习Docker
✅ 正确: 开启新对话 "学习Docker容器化"
```

#### 3️⃣ 问题调试
```
❌ 错误: 在"Ollama配置"对话中调试Nginx
✅ 正确: 开启新对话 "Nginx配置问题排查"
```

#### 4️⃣ 不同阶段
```
❌ 错误: 设计、开发、部署、维护都在一个对话
✅ 正确: 
  - "网站设计阶段"
  - "网站开发"
  - "网站部署上线"
  - "网站维护优化"
```

#### 5️⃣ Token压力
```
⚠️ 当前对话已达到 40K+ tokens
✅ 建议分割成多个主题对话
```

---

## 对话命名规范

### 好的标题格式

**项目类**:
- ✅ "websitedesign.oskris.com 部署"
- ✅ "OskrisAgent Telegram机器人开发"
- ✅ "Kong Kiong Hardware 网站优化"

**学习类**:
- ✅ "学习Ollama本地AI部署"
- ✅ "研究iOS快捷指令自动化"
- ✅ "掌握Docker容器化"

**问题类**:
- ✅ "解决Claude备份卡顿问题"
- ✅ "排查Nginx SSL证书错误"
- ✅ "修复iPhone存储不足"

**系统类**:
- ✅ "AI团队创建和配置"
- ✅ "系统安全加固"
- ✅ "备份策略优化"

**日常类**:
- ✅ "每日例行检查 2026-02-21"
- ✅ "快速问答"

### 不好的标题
- ❌ "Chat 1" / "新对话" (没有信息)
- ❌ "各种事情" (太模糊)
- ❌ "帮我做..." (太宽泛)

---

## 对话追踪系统

### conversations.json
```json
{
  "active": [
    {
      "id": "conv-001",
      "title": "AI团队创建和权限系统",
      "started": "2026-02-21 00:00",
      "status": "进行中",
      "topics": ["AI团队", "权限分级", "审批流程"],
      "next_action": "完成Ollama配置",
      "token_usage": 40000
    },
    {
      "id": "conv-002",
      "title": "Ollama本地AI完整配置",
      "started": "2026-02-21 11:00",
      "status": "新开启",
      "topics": ["Ollama安装", "模型下载", "OpenClaw集成"],
      "next_action": "下载Qwen和DeepSeek模型",
      "token_usage": 500
    }
  ],
  "completed": [
    {
      "id": "conv-000",
      "title": "websitedesign.oskris.com 部署",
      "started": "2026-02-20 23:00",
      "completed": "2026-02-21 01:00",
      "status": "已完成",
      "result": "✅ 网站成功上线 https://websitedesign.oskris.com"
    }
  ],
  "paused": []
}
```

### 状态定义
- **新开启** - 刚创建，还没深入
- **进行中** - 正在活跃讨论
- **待续** - 暂停，等待某些条件
- **已完成** - 目标达成
- **已归档** - 不再需要

---

## 使用流程

### 1️⃣ 主AI检查当前对话
```bash
# 快速检查当前对话状态
~/.openclaw/workspace/skills/conversation-manager/check.sh

# 输出:
# 当前对话: "AI团队创建和权限系统"
# Token使用: 40K / 200K (20%)
# 主题数: 5个 (AI团队, 权限, Ollama, 备份, 系统监控)
# ⚠️ 建议: 主题过多，建议分割
```

### 2️⃣ 建议开启新对话
当主AI检测到以下情况，建议用户开启新对话：
- 新主题与当前对话主题不相关
- 当前对话已涵盖3+个主题
- Token使用超过30%
- 用户说"现在我们来..."（新事情）

**建议话术**:
```
💡 建议: 

现在我们要开始配置Ollama，这是一个完整的新主题。
建议开启新对话 "Ollama本地AI完整配置"，这样：

✅ 对话聚焦，易于回顾
✅ 节省当前对话的token
✅ 将来查找更容易

要不要我们开始新对话？
```

### 3️⃣ 创建新对话记录
```bash
# 记录新对话
~/.openclaw/workspace/skills/conversation-manager/new.sh \
  --title "Ollama本地AI完整配置" \
  --topics "Ollama安装,模型下载,集成" \
  --goal "完成三合一AI架构的Ollama部分"
```

### 4️⃣ 切换回旧对话
```bash
# 列出所有对话
~/.openclaw/workspace/skills/conversation-manager/list.sh

# 输出:
# 进行中的对话:
# 1. [conv-001] AI团队创建和权限系统 (40K tokens)
# 2. [conv-002] Ollama本地AI完整配置 (500 tokens)
#
# 已完成:
# 3. [conv-000] websitedesign.oskris.com 部署 ✅

# 用户可以选择切换回哪个对话
```

### 5️⃣ 更新对话状态
```bash
# 标记对话为已完成
~/.openclaw/workspace/skills/conversation-manager/complete.sh conv-002

# 暂停对话（等待某些条件）
~/.openclaw/workspace/skills/conversation-manager/pause.sh conv-001 \
  --reason "等待Ollama配置完成"
```

---

## 对话切换提示

### 提醒用户
当用户在对话A中提到对话B的主题：

```
💡 注意:

这个问题属于 "Ollama本地AI配置" 对话的内容。

建议:
1. 切换到那个对话继续讨论
2. 或者在这里快速回答，然后在那边记录

你想怎么做？
```

### 自动同步
当在对话A中解决了对话B的问题，自动更新对话B的状态：

```bash
# 在conversations.json中更新
{
  "id": "conv-002",
  "status": "已完成",
  "completed_in": "conv-001",
  "result": "✅ Ollama模型下载完成"
}
```

---

## 对话归档策略

### 何时归档
- ✅ 已完成超过7天
- ✅ 结果已记录到MEMORY.md
- ✅ 所有文件已整理到项目文件夹

### 归档流程
1. 提取关键决策和经验
2. 更新MEMORY.md
3. 整理相关文件
4. 标记对话为"已归档"
5. 可选：删除对话（如果所有内容已保存）

---

## 最佳实践

### ✅ 好习惯
1. **一事一议** - 每个对话专注一个主题
2. **清晰命名** - 看标题就知道内容
3. **及时分割** - 不等到混乱才分
4. **定期归档** - 完成的对话及时归档
5. **交叉引用** - 相关对话互相引用

### ❌ 坏习惯
1. 一个对话讨论所有事情
2. 标题随便起，"新对话"、"Chat 1"
3. 对话越来越长，从不分割
4. 完成的对话不归档，堆积如山
5. 同一个问题在多个对话重复讨论

---

## 集成到主AI工作流

### Heartbeat检查
```markdown
# HEARTBEAT.md
每次heartbeat检查：
1. 当前对话是否偏题
2. Token使用是否超过30%
3. 是否应该建议新对话
```

### 新消息处理
```javascript
// 伪代码
if (message.topic != current_conversation.topics) {
  suggest_new_conversation(message.topic);
}
```

### 定期整理
```bash
# 每周日晚上
# 检查所有对话状态
# 归档已完成的
# 提醒待续的
```

---

## 示例场景

### 场景1: 用户突然提新需求
**当前对话**: "AI团队创建"  
**用户**: "对了，我想做个iPhone快捷指令..."

**主AI回应**:
```
这是一个很好的想法！

不过这是一个新项目，建议我们开启新对话：
"iPhone快捷指令开发 - [项目名]"

这样我们可以：
✅ 专注讨论快捷指令
✅ 保持"AI团队创建"对话的清晰
✅ 将来查找更容易

要不要现在开始新对话？
```

### 场景2: 对话主题漂移
**对话标题**: "Ollama配置"  
**讨论内容**: Ollama → Nginx → SSL → DNS → ...

**主AI自检**:
```
⚠️ 检测到主题漂移

原始主题: Ollama配置
当前讨论: DNS记录管理

建议:
1. 完成Ollama配置后关闭此对话
2. DNS问题开新对话 "域名DNS管理"
```

### 场景3: 回到旧话题
**用户**: "之前那个websitedesign的SSL证书问题解决了吗？"

**主AI查找**:
```
找到相关对话: "websitedesign.oskris.com 部署"

状态: ✅ 已完成
结果: SSL证书已安装，有效期到2026-05-21

要不要切换到那个对话查看详情？
还是我在这里简单说明？
```

---

## 工具脚本

### check.sh
检查当前对话状态和建议

### new.sh
创建新对话记录

### list.sh
列出所有对话

### complete.sh
标记对话完成

### pause.sh
暂停对话

### archive.sh
归档旧对话

### sync.sh
同步对话状态到conversations.json

---

## 总结

这个skill的核心价值：
1. **组织有序** - 每个对话清晰聚焦
2. **易于查找** - 看标题就知道内容
3. **节省Token** - 避免一个对话变得太长
4. **提升效率** - 减少翻历史记录的时间

**使用原则**: 一事一议，及时分割，清晰命名！
