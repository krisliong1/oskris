# Auto Storage Skill（完整版）

## 核心原则
**每次创建内容后，自动存储到 GitHub + VPS，并告诉用户每一步**

## 配置来源
**从 Secrets Manager Skill 读取所有配置**
- 位置: `/mnt/skills/user/secrets-manager/SKILL.md`
- 包含: VPS、Hostinger API、GitHub Token

## 触发条件
- 创建了学习报告
- 完成了 Skill
- 生成了代码
- 更新了配置
- **任何重要内容**

## 执行流程

### 🔔 第 1 步：立即告诉用户
```
🔔 准备存储以下内容：
━━━━━━━━━━━━━━━━━━━━━━
📄 文件: XXX.md
📁 类型: 学习报告/Skill/代码
🎯 目标: 
  - GitHub (krisliong1/oskris)
  - VPS (76.13.191.45)
  - 记忆系统

开始执行...
```

### 📦 第 2 步：存储到 GitHub

**告诉用户**:
```
[1/4] 正在存储到 GitHub...
```

**执行**:
```bash
# 1. 读取 Secrets Manager 获取 GitHub Token
# 2. 克隆仓库
# 3. 复制文件到对应目录
# 4. 提交并推送
```

**告诉用户结果**:
```
✅ [1/4] GitHub 存储成功
  - 仓库: krisliong1/oskris
  - 路径: learning-reports/XXX.md
  - 提交: Add: XXX
  - 链接: https://github.com/krisliong1/oskris/blob/main/...
```

### 🖥️ 第 3 步：同步到 VPS

**告诉用户**:
```
[2/4] 正在同步到 VPS...
```

**方法**: VPS 从 GitHub 自动拉取或使用 Hostinger API

**告诉用户结果**:
```
✅ [2/4] VPS 同步成功
  - IP: 76.13.191.45
  - 路径: /root/oskris-data/XXX.md
```

### 🧠 第 4 步：更新记忆

**执行**: `memory_user_edits add "..."`

**告诉用户结果**:
```
✅ [3/4] 记忆已更新
```

### 💾 第 5 步：本地输出

**告诉用户结果**:
```
✅ [4/4] 本地文件已准备
  - /mnt/user-data/outputs/XXX.md
```

### 📊 最终报告

```
━━━━━━━━━━━━━━━━━━━━━━
📦 存储完成！
━━━━━━━━━━━━━━━━━━━━━━

✅ GitHub
  仓库: krisliong1/oskris
  路径: XXX.md
  链接: https://github.com/krisliong1/oskris/...

✅ VPS  
  IP: 76.13.191.45
  状态: 已同步

✅ 记忆
  已更新

✅ 本地
  /mnt/user-data/outputs/XXX.md

🎉 所有存储操作完成！
```

## 重要提醒

### ✅ 必须做
1. **每一步都告诉用户**
2. **显示成功/失败状态**
3. **提供链接和路径**
4. **更新记忆系统**

### ❌ 绝对禁止
1. ❌ 默默存储
2. ❌ 忘记告诉用户
3. ❌ 在此文件包含密钥（从 Secrets Manager 读取）

## 自动化记忆更新

### 每次对话结束时
1. 自动调用 `memory_user_edits`
2. 记录重要内容
3. 确保新对话能读取

### 新对话开始时
1. 自动读取所有 Skills
2. 特别是 `secrets-manager` 和 `auto-storage`
3. 恢复所有配置和状态

## 更新日志
- 2026-02-16: 创建完整自动化存储 Skill（不含密钥）
