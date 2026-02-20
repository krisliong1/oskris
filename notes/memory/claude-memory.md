# Claude 记忆系统

最后更新: 2026-02-20

## 核心配置
1. GitHub: krisliong1/oskris, 只推main分支, /tmp克隆操作
2. VPS: 76.13.191.45, 见private-config
3. Hostinger API已配置(见private-config)
4. 域名: oskris.com(到期2027)
5. 用户邮箱: oskrismy@gmail.com / krisliong11@gmail.com / official@oskris.com

## GitHub仓库分工
6. krisliong1/oskris (Public) — 活跃代码、skills、项目文件
7. krisliong1/backup (Public) — 存放/备份
8. krisliong1/private-config (Private) — 所有token、密码、API key
9. 敏感信息只推private-config, 绝不推public仓库

## 工作规则
10. 代码/命令英文, 其他华文; 所有价格用RM
11. 质量要求专业级; 先验证再执行
12. 文件已存在用str_replace, 不盲目创建
13. 文件双版本: Claude版含完整信息, GitHub Public版去敏感信息

## OpenClaw (Mac Mini user:openclaw)
14. Gateway端口: 18789
15. Discord已配: honorkingsellbot; 待配: kaijiepeiwanbot
16. Telegram待配置(见private-config)
17. 核心问题: gateway断连因AI自改配置
18. 解决方案: chmod 444+exec approvals+SOUL规则
19. 配置文件: projects/openclaw-setup/ + private-config仓库

## 当前项目
20. websitedesign.oskris.com - 待部署
21. OpenClaw配置修复 - 文件已准备, 等用户回家操作
