# OpenClaw 配置修复

## 问题
OpenClaw AI频繁自行修改 openclaw.json 配置文件，导致 schema 验证失败，gateway 断连。

## 解决方案
1. **SETUP-GUIDE.md** — 完整操作手册，回家照着做
2. **soul-protection-rules.md** — 粘贴到 SOUL.md 最前面的保护规则
3. **openclaw-config-additions.json5** — 要添加到 openclaw.json 的配置项

## 核心措施
- `chmod 444` 锁住配置文件（AI物理上改不了）
- `tools.exec.approvals: "always"` 所有命令都要用户批准
- SOUL.md 禁止修改配置文件的规则
- 安装 self-improvement skill 让错误被记录

## 创建日期
2026-02-20
