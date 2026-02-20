# Claude 记忆系统（三环境通用）

最后更新: 2026-02-20

## 三个环境

| 环境 | 使用者 | 路径 |
|------|--------|------|
| Claude.ai | Claude (web/iOS) | /mnt/user-data/outputs, /tmp |
| Claude Desktop/Code | Claude (Mac MCP) | /Users/oskris/ |
| OpenClaw | OpenClaw AI (Mac) | /Users/openclaw/.openclaw/workspace/ |

## 通用规则
- 修改现有文件前必须告诉用户并等确认
- 敏感信息只存 private-config（Private仓库）
- 质量专业级，先验证再执行
- 工具失败最多重试2次

## GitHub仓库分工
- krisliong1/oskris (Public) — 代码、skills、项目
- krisliong1/backup (Public) — 备份快照
- krisliong1/private-config (Private) — 所有凭据

## OpenClaw规则
- 绝不修改 ~/.openclaw/openclaw.json
- 绝不执行 openclaw config set
- 绝不自己重启 gateway
- 只在 workspace/ 目录内操作
- 犯错记录到 .learnings/ERRORS.md

## 当前待办
- OpenClaw: 加Telegram + 锁配置（文件在 openclaw/）
- websitedesign.oskris.com: 待部署

完整版见 Claude Project Knowledge
