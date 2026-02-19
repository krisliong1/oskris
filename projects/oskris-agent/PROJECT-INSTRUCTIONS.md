# OskrisAgent - Project Instructions

## 项目概述

OskrisAgent 是一个通过 Telegram 控制的个人 AI 代理，结合 Claude 的智能与系统级工具执行能力。用户可以从手机随时随地远程操控 VPS、写代码、管理文件、搜索信息、同步 GitHub。

## 技术架构

```
Telegram (手机/桌面) → Telegram Bot API → Node: bot.py
                                            ↓
                                    Claude API (tool_use)
                                            ↓
                                    7个工具: bash / read_file / write_file /
                                    list_directory / web_search / github_push / github_read
                                            ↓
                                    Memory 持久化 (JSON)
```

## 基础设施

- VPS: 76.13.191.45 (Ubuntu 25.10, 2核8GB, Malaysia, Hostinger)
- GitHub: krisliong1/oskris, token: 存于.env
- 代码位置: GitHub `projects/oskris-agent/`
- VPS部署路径: `/opt/oskris-agent/`
- 域名: oskris.com (到期2027)

## 文件结构与职责

```
oskris-agent/
├── bot.py              # Telegram主程序：消息路由、命令处理、文件上传、权限控制
├── system_prompt.md    # Agent的AI人设（可自定义，热加载）
├── install.sh          # VPS一键部署脚本（apt + venv + systemd）
├── requirements.txt    # Python依赖
├── .env.example        # 环境变量模板
├── .env                # 实际配置（不上传GitHub）
├── core/
│   ├── config.py       # 配置管理：从.env读取，路径定义，安全限制
│   ├── agent.py        # Claude API调度器：tool_use循环（最多10轮），消息构建
│   ├── memory.py       # 对话记忆：JSON持久化，自动trim，统计
│   └── tools.py        # 7个工具的定义(schema) + 执行器(executor)
└── data/
    ├── memory/         # 对话历史JSON文件
    └── logs/           # 运行日志
```

## 核心模块说明

### bot.py - Telegram入口
- `@owner_only` 装饰器确保只有主人能用
- 命令: /start, /status, /clear, /exec
- 文本消息 → 转发给Claude Agent处理
- 文件上传 → 保存到/tmp/uploads/ → 告知Claude
- 长消息自动分割（Telegram限制4096字符）
- 工具执行时显示实时状态消息

### core/agent.py - Claude大脑
- 使用 Anthropic Python SDK
- tool_use 循环：Claude请求工具 → 执行 → 返回结果 → Claude继续
- 最多10轮工具调用
- 自动管理对话历史（发给API）
- on_status 回调：工具执行时通知用户

### core/tools.py - 工具系统
当前7个工具：
1. `bash` - 执行系统命令（有安全黑名单，120秒超时）
2. `read_file` - 读取文件（50KB限制）
3. `write_file` - 写入文件（自动创建目录）
4. `list_directory` - 列目录
5. `web_search` - DuckDuckGo搜索（无需API key）
6. `github_push` - 通过GitHub API推送文件
7. `github_read` - 从GitHub读取文件

### core/memory.py - 记忆系统
- 每个chat_id独立的JSON文件
- 保留最近30条消息
- 自动trim防止无限增长
- 支持统计查询

## 开发规则

### 语言
- 华文(中文)回复用户
- 代码、命令、变量名、技术术语保持英文
- 注释用英文

### 代码规范
- Python 3.10+ 语法
- 异步优先（async/await）
- 所有工具执行必须有错误处理
- 工具结果限制在15000字符内
- 敏感信息只存.env，不进代码或GitHub

### 修改代码后的流程
1. 修改/创建文件
2. 确认改动正确
3. 上传到 GitHub: `projects/oskris-agent/` 路径下
4. 如果是运行中的服务，提醒用户SSH到VPS执行 `git pull` + `systemctl restart oskris-agent`

### 质量标准
所有输出必须达到专业级(Level 4)：
- Level 1 初级：能跑 ❌
- Level 2 中级：规范 ❌
- Level 3 高级：优化 ❌
- Level 4 专业级：行业标准 ✅ ← 目标

## 常用操作命令

```bash
# SSH到VPS
ssh root@76.13.191.45

# 服务管理
systemctl start oskris-agent
systemctl stop oskris-agent
systemctl restart oskris-agent
systemctl status oskris-agent

# 查看日志
journalctl -u oskris-agent -f

# 更新代码
cd /opt/oskris-agent
git pull origin main
systemctl restart oskris-agent

# 编辑配置
nano /opt/oskris-agent/.env
```

## 扩展计划（待开发功能）

### 优先级高
- [ ] 语音消息支持（接收语音→转文字→处理）
- [ ] 图片识别（接收图片→Claude Vision分析）
- [ ] 定时任务（Cron-like：定时检查、报告、备份）
- [ ] Markdown渲染优化（Telegram MarkdownV2格式适配）

### 优先级中
- [ ] 多用户支持（白名单机制）
- [ ] 插件/Skill系统（动态加载新工具）
- [ ] 网页抓取工具（aiohttp fetch + BeautifulSoup解析）
- [ ] 数据库支持（SQLite替代JSON存储）

### 优先级低
- [ ] Web Dashboard（查看对话历史、管理配置）
- [ ] WhatsApp/Discord多渠道支持
- [ ] 主动通知（监控VPS状态，异常时推送）
- [ ] 文件传输（Agent生成文件→发送给用户）

## 注意事项

1. `.env` 文件包含敏感信息，绝对不上传GitHub
2. `OWNER_TELEGRAM_ID` 是唯一安全防线，必须正确设置
3. bash工具有安全黑名单但不是万能的，Agent可能执行危险命令
4. DuckDuckGo搜索可能被限流，未来考虑换Brave Search API
5. GitHub token有有效期，过期需更新
6. Claude API按用量计费，注意token消耗（MAX_TOKENS=8192）
7. 对话历史存在VPS磁盘，不会自动备份
