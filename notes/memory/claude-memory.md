# Claude 记忆系统

最后更新: 2026-02-19

## 核心配置
1. GitHub: krisliong1/oskris, 只推main分支, /tmp克隆操作
2. VPS: 76.13.191.45, 密码Qwer-1234Aa, Ubuntu 25.10, 2核8GB, Malaysia
3. Hostinger API已配置(token存Claude记忆)
4. 域名: oskris.com(到期2027)
5. 用户邮箱: oskrismy@gmail.com / krisliong11@gmail.com / official@oskris.com

## 工作规则
6. 所有价格用RM(马来西亚令吉)
7. 用户零代码基础, Claude负责学习+执行
8. 质量等级: 初级→中级→高级→专业级, 要求专业级
9. 先验证再执行, 不用占位符
10. 代码/命令保持英文, 其他用华文回复
11. 提供命令不加#注释, 只给纯代码
12. 文件已存在用str_replace, 不要盲目创建

## 自动存储
13. 创建/修改/创建新project/创建任何文件后→1)上传GitHub 2)Desktop模式同时写入Mac本地 3)claude.ai模式提醒去Desktop同步
14. 每步告诉用户同步了哪些文件到哪里(需提醒用户已上传或修改的文件)
15. 敏感信息禁止存GitHub, 只存VPS+记忆
16. 记忆更新后同步此文件: notes/memory/claude-memory.md

## Mac Mini M4 Desktop同步
32. Claude Desktop已配置MCP filesystem, 可读写: /Users/oskris/Desktop, Documents, Downloads
33. 检测到Desktop模式(有filesystem工具)→自动开启数据同步: 文件直接写入Mac+上传GitHub
34. claude.ai模式→上传GitHub, 告知用户去Desktop同步
35. Node.js路径: /Users/oskris/.nvm/versions/node/v20.20.0
36. 已安装MCP: filesystem, github, hostinger-api-mcp

## Context Window 监控(核心!)
17. 研究证实: 20-40%就开始降级, 不是100%
18. 降级是悬崖式非线性的, 不可预测
19. Claude必须每10轮主动报告估计用量%
20. 阈值: 30%警告, 40%强烈建议开新对话, 50%必须停止
21. 来源: Chroma Research(18个LLM测试), Stanford Lost in the Middle

## Skills分类
22. core/ - 核心系统(work-rules, core-work-rules等)
23. web-development/ - 网站开发(project-workflow等)
24. content/ - 翻译(auto-translate, smart-info-manager)
25. product/ - 产品(product-self-knowledge, app-recommendations)

## 当前项目
26. websitedesign.oskris.com - 网站设计服务
27. 定价: 用户不满意旧定价, 待用户自己确定新价格

## Telegram Bot
37. oskristelegramagentbot 是Claude制作的文件里的telegrambot(非主要通讯bot)
38. Bot Token: 存在Claude记忆中

## iOS配置
39. mobileconfig 组织名: oskris.com

## 文件路径
28. /home/claude - 临时工作
29. /mnt/user-data/outputs - 输出给用户
30. /mnt/skills/user/ - 读取Skills
31. /tmp - 临时目录(克隆GitHub用)
