---
name: auto-storage
description: 自动存储流程。Claude创建重要内容后自动存储到GitHub+VPS+记忆，每步告诉用户。当创建了学习报告、Skill、代码、配置等重要内容时触发。
---

# Auto Storage

创建重要内容后自动执行，不需要用户要求。

## 触发条件

创建了：学习报告、Skill、代码文件、配置更新、任何重要内容。

## 执行流程

### Step 1: 告诉用户

```
🔔 准备存储: [文件名] → GitHub + VPS + 记忆
```

### Step 2: 存储到GitHub

```bash
cd /tmp/oskris  # 已克隆的仓库
cp [文件] [对应目录]
git add .
git commit -m "Add: [描述]"
git push origin main
```

完成后：`✅ GitHub: krisliong1/oskris/[路径]`

### Step 3: 同步到VPS

通过Hostinger API或VPS从GitHub自动拉取。

完成后：`✅ VPS: 76.13.191.45`

### Step 4: 更新记忆

使用 `memory_user_edits` 记录重要信息。

完成后：`✅ 记忆已更新`

### Step 5: 本地输出

复制到 `/mnt/user-data/outputs/` 供用户下载。

### 最终报告

```
📦 存储完成
✅ GitHub: [链接]
✅ VPS: 已同步
✅ 记忆: 已更新
✅ 本地: /mnt/user-data/outputs/[文件]
```

## 规则

- 每一步都告诉用户，不默默存储
- 敏感信息(Token/密码)只存记忆和VPS，禁止存GitHub
- 失败时告知用户具体哪一步失败，给替代方案
