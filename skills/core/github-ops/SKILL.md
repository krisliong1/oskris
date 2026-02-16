---
name: github-ops
description: GitHub仓库操作统一规范。合并原github-auto-auth、github-change-tracker、github-skills-sync、skill-auto-sync四个skill。覆盖认证、推送、同步、变更报告的完整流程。当需要push代码、同步skills、或操作GitHub仓库时使用。
---

# GitHub Ops

krisliong1/oskris 仓库的所有GitHub操作统一流程。

## 认证

Token从Claude记忆获取，永不询问用户。静默配置，直接使用。

```bash
cd /tmp
rm -rf oskris
git clone https://krisliong1:{TOKEN}@github.com/krisliong1/oskris.git
cd oskris
git config user.name "Claude Assistant"
git config user.email "claude@oskris.com"
```

## 推送流程

每次推送遵循：修改 → add → 报告变更 → commit → push → 告知用户。

### 变更报告（推送前必须）

告诉用户改了什么，格式简洁：

```
新建: skills/core/work-rules/SKILL.md
更新: skills/README.md
```

### Commit信息规范

- 新增：`feat: Add {name}`
- 修改：`update: Modify {name}`
- 删除：`remove: Delete {name}`
- 批量：`chore: Sync {count} files`

### 推送后确认

推送完成后告诉用户新建和更新的文件名，格式简洁，一行一个。

## Skills目录结构

```
skills/
├── core/              # 核心规则
├── web-development/   # 网站开发
├── documents/         # 文档处理
├── business/          # 业务流程
└── creative/          # 设计创意
```

新skill：确定分类 → 创建 `skills/{分类}/{skill-name}/SKILL.md` → 推送main。

文件夹名：小写+连字符，禁止下划线或大写。每个skill一个SKILL.md。

## Skills同步（Claude.ai环境）

当 /mnt/skills/user/ 为空或缺少需要的skill时：

```bash
cd /tmp && rm -rf oskris
git clone https://krisliong1:{TOKEN}@github.com/krisliong1/oskris.git
cp -r /tmp/oskris/skills/* /mnt/skills/user/ 2>/dev/null || true
```

不需要每次对话都同步，只在skills缺失时执行。

## 自动推送触发

创建/修改skill后自动推送，不需要用户要求。批量修改时收集所有变更一次性推送。

## 安全检查

推送前检查：禁止提交API keys、密码、Token到代码文件。敏感信息只存Claude记忆和VPS。

## 错误处理

- 推送失败：最多重试2次，失败告知用户检查网络
- Token过期：提醒用户更新
- 冲突：`git pull --rebase` 后重试
