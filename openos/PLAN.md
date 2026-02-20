# OpenOS — 架构规划文档

> 项目代号: OpenOS
> 前身: OskrisAgent + OpenClaw
> 状态: 规划阶段
> 日期: 2026-02-20

---

## 一、项目定位

**OpenOS = 你的私人AI操作系统**

把OpenClaw（本地AI助手）作为核心大脑，把OskrisAgent的VPS远程能力作为扩展模块，统一成一个项目。

**一句话总结**: 本地跑全功能AI助手，VPS跑轻量远程节点，两边数据同步，随时随地可用。

---

## 二、当前状态盘点

### OpenClaw（在Mac Mini上运行中）
- ✅ 多平台聊天: WhatsApp, Telegram, Discord, iMessage
- ✅ 浏览器控制
- ✅ 本地文件系统完整访问
- ✅ Shell命令执行
- ✅ Skills生态系统（自动创建新skill）
- ✅ 持久记忆（Markdown本地存储）
- ✅ Claude Max订阅（OAuth认证）
- ✅ Gateway架构（ws://127.0.0.1:18789）
- ✅ Web聊天界面 + Dashboard
- ⚠️ 已知问题: AI自改配置导致gateway断连（已有保护方案）
- ⚠️ Token需要定期刷新

### OskrisAgent（VPS上，未正常运行）
- ✅ 代码完成: bot.py, agent.py, tools.py, memory.py, config.py
- ✅ Telegram Bot集成
- ✅ Claude API调用 + tool_use循环
- ✅ bash执行、文件读写、GitHub同步
- ✅ systemd自启动服务
- ❌ 实际未正常运行（"待修复，目前无回复"）
- ❌ 功能与OpenClaw重叠
- ❌ 用API按量付费（不如Max订阅）

---

## 三、OpenOS架构

```
┌─────────────────────────────────────────────────────┐
│                    OpenOS                            │
│                                                     │
│  ┌─────────────────────────────────┐                │
│  │   Mac Mini (主脑 - 100%)        │                │
│  │                                 │                │
│  │  OpenClaw Gateway               │                │
│  │  ├── WhatsApp                   │                │
│  │  ├── Telegram                   │                │
│  │  ├── Discord                    │  ◄── 同步 ──►  │
│  │  ├── iMessage                   │                │
│  │  ├── WebChat                    │                │
│  │  ├── 浏览器控制                  │                │
│  │  ├── 本地文件系统                │                │
│  │  ├── Skills引擎                 │                │
│  │  └── 持久记忆                   │                │
│  │                                 │                │
│  │  Claude Max (OAuth)             │                │
│  └─────────────────────────────────┘                │
│                                                     │
│  ┌─────────────────────────────────┐                │
│  │   VPS 远程节点 (20%)            │                │
│  │   76.13.191.45                  │                │
│  │                                 │                │
│  │  ├── Telegram Bot (备用入口)    │                │
│  │  ├── bash远程执行               │                │
│  │  ├── 网站托管 (nginx)           │                │
│  │  ├── 健康监控 + 告警            │                │
│  │  ├── GitHub同步中转             │                │
│  │  └── Mac Mini离线时的fallback   │                │
│  │                                 │                │
│  │  Claude API (轻量调用)          │                │
│  └─────────────────────────────────┘                │
│                                                     │
│  ┌─────────────────────────────────┐                │
│  │   Claude.ai / Claude Code       │                │
│  │   (开发+管理界面)               │                │
│  │                                 │                │
│  │  ├── 项目开发                   │                │
│  │  ├── Skill创建                  │                │
│  │  ├── 文件管理                   │                │
│  │  └── 规划和决策                 │                │
│  └─────────────────────────────────┘                │
└─────────────────────────────────────────────────────┘
```

---

## 四、Mac Mini 主脑（100%能力）

### 保留OpenClaw全部能力
不改OpenClaw的核心，而是在它之上加一层"OpenOS"的配置和skills。

| 能力 | 来源 | 说明 |
|------|------|------|
| 多平台聊天 | OpenClaw原生 | WhatsApp/Telegram/Discord/iMessage |
| 浏览器控制 | OpenClaw原生 | 网页操作、数据抓取 |
| 文件系统 | OpenClaw原生 | 读写Mac本地所有文件 |
| Shell执行 | OpenClaw原生 | 本地命令 |
| Skills系统 | OpenClaw原生 | 自动创建+安装skill |
| 持久记忆 | OpenClaw原生 | Markdown本地存储 |
| 语音交互 | OpenClaw原生 | macOS/iOS语音 |
| **VPS远程控制** | **新增** | SSH到VPS执行命令 |
| **网站部署** | **新增** | 从Mac推代码到VPS |
| **跨节点同步** | **新增** | Mac ↔ VPS ↔ GitHub三方同步 |

### 新增的OpenOS Skills（给OpenClaw用）
```
openos-skills/
├── vps-remote/          # SSH远程执行VPS命令
├── site-deploy/         # 网站部署到VPS
├── cross-sync/          # Mac ↔ VPS ↔ GitHub同步
├── health-monitor/      # VPS健康监控 + 告警
├── backup-manager/      # 自动备份到VPS/GitHub
└── fallback-config/     # Mac离线时VPS接管配置
```

---

## 五、VPS远程节点（20%能力）

### 从OskrisAgent改造
保留OskrisAgent的核心代码，但重新定位为"OpenOS VPS节点"。

| 保留 | 改造 | 删除 |
|------|------|------|
| bot.py (Telegram入口) | 角色从"主AI"改为"远程节点" | 独立的system_prompt |
| tools.py (bash/文件/GitHub) | 加入Mac Mini心跳检测 | 独立的Skills系统 |
| memory.py (对话记忆) | 记忆与Mac Mini同步 | 独立的web_search |
| config.py (配置管理) | 加VPS节点专属配置 | — |
| install.sh (部署脚本) | 改名为openos-vps-install.sh | — |

### VPS节点的职责
1. **Telegram备用入口** — Mac Mini在线时转发到OpenClaw，离线时自己用Claude API回复（降级模式）
2. **网站托管** — nginx运行oskris.com、kkh.oskris.com等
3. **远程bash执行** — OpenClaw通过SSH调用VPS命令
4. **健康监控** — 定时检查服务状态，异常时通过Telegram告警
5. **GitHub中转** — webhook接收推送通知

### VPS节点工作模式
```
正常模式（Mac Mini在线）:
  用户 → Telegram → VPS Bot → 转发到Mac Mini OpenClaw → 回复

降级模式（Mac Mini离线）:
  用户 → Telegram → VPS Bot → 本地Claude API → 基本回复
  （只能执行VPS上的bash、文件操作，不能访问Mac本地文件）
```

---

## 六、数据同步架构

```
Mac Mini ──── GitHub ──── VPS
   │      (krisliong1/     │
   │       oskris)         │
   │                       │
   ├── Skills ◄────────► Skills(轻量版)
   ├── 记忆  ◄────────► 记忆(缓存)
   ├── 配置  ◄────────► 配置(节点版)
   └── 项目  ◄────────► 网站文件
```

**同步规则**:
- Mac Mini是真相来源（source of truth）
- VPS保存缓存副本，Mac Mini更新时自动同步
- GitHub作为中间传输层 + 版本管理
- 敏感信息只存Mac Mini本地 + private-config仓库

---

## 七、项目仓库重组

### 当前仓库
```
krisliong1/oskris        → 活跃代码
krisliong1/backup        → 备份
krisliong1/private-config → 敏感信息
krisliong1/openclaw      → 空仓库
```

### OpenOS后的仓库
```
krisliong1/oskris        → OpenOS主仓库（改名内容，仓库名保留）
  ├── openos/
  │   ├── vps-node/      # VPS节点代码（原OskrisAgent改造）
  │   ├── skills/        # OpenOS专属skills
  │   ├── config/        # 配置模板
  │   └── docs/          # 文档
  ├── skills/            # 所有skills（保留现有结构）
  ├── projects/          # 网站项目
  └── ...

krisliong1/openclaw      → OpenClaw的自定义配置+skills
  ├── soul/              # SOUL.md和保护规则
  ├── skills/            # 给OpenClaw安装的skill
  └── config/            # openclaw.json配置参考

krisliong1/backup        → 不变
krisliong1/private-config → 不变
```

---

## 八、实施路线图

### Phase 1: 基础整合（1-2天）
- [ ] 修复VPS上的OskrisAgent，让它能正常运行
- [ ] 在OskrisAgent里加Mac Mini心跳检测
- [ ] 创建OpenOS目录结构到GitHub
- [ ] 写第一个OpenClaw skill: `vps-remote`（SSH执行VPS命令）

### Phase 2: 双节点联动（2-3天）
- [ ] VPS Bot实现"转发到OpenClaw"逻辑
- [ ] OpenClaw通过SSH控制VPS
- [ ] 基本的记忆同步（Mac → GitHub → VPS）
- [ ] 健康监控 + Telegram告警

### Phase 3: 降级模式（1-2天）
- [ ] Mac Mini离线检测
- [ ] VPS自动切换到本地Claude API
- [ ] 降级模式下的基本对话能力
- [ ] Mac Mini上线后自动恢复+同步

### Phase 4: 完善（持续）
- [ ] 更多OpenOS skills
- [ ] 网站一键部署流程
- [ ] 跨节点备份策略
- [ ] 性能优化

---

## 九、关键决策点（需要你确认）

1. **项目名**: "OpenOS"确定吗？还是其他名字？
2. **GitHub仓库**: 在现有oskris仓库里加openos目录，还是新建仓库？
3. **VPS上的Telegram Bot**: 继续用 @oskristelegramagentbot 还是换新bot？
4. **OpenClaw的SOUL.md**: 需要加OpenOS相关的指令吗？
5. **Claude API费用**: VPS降级模式用Claude API，继续用Pro还是换更便宜的方案？

---

*这是初始规划，随项目推进会持续更新。*
