# Persistent AI Team - 常驻AI团队系统

## 理念
**一次性AI = 健忘症患者**  
**常驻AI = 经验丰富的专家**

## AI团队成员

### 1. Backup Manager (备份管理员)
**职责**：所有备份任务
**Workspace**: `~/.openclaw/ai-team/backup-manager/`
**记忆**：
- 备份历史记录
- 优化的rsync参数
- 失败案例和解决方案
**技能提升**：
- 学习最优压缩率
- 自动排除无用文件
- 智能增量备份

### 2. File Organizer (文件管理员)
**职责**：整理、分类、清理文件
**Workspace**: `~/.openclaw/ai-team/file-organizer/`
**记忆**：
- 用户文件习惯
- 分类规则优化
- 垃圾文件模式识别
**技能提升**：
- 学习用户偏好
- 智能命名建议
- 自动去重

### 3. Deploy Manager (部署管理员)
**职责**：网站部署、VPS管理、DNS配置
**Workspace**: `~/.openclaw/ai-team/deploy-manager/`
**记忆**：
- 部署成功案例
- Nginx配置模板
- 域名管理记录
**技能提升**：
- 优化部署流程
- 自动化配置
- 性能调优经验

### 4. Research Assistant (研究助手)
**职责**：web搜索、学习新技术、文档总结
**Workspace**: `~/.openclaw/ai-team/research-assistant/`
**记忆**：
- 学习笔记
- 可信来源列表
- 技术知识库
**技能提升**：
- 提高搜索精准度
- 快速提取关键信息
- 建立知识图谱

### 5. iOS Automation (iOS自动化专家)
**职责**：快捷指令、iPhone管理、豆包集成
**Workspace**: `~/.openclaw/ai-team/ios-automation/`
**记忆**：
- 快捷指令库
- 自动化脚本
- 设备配置
**技能提升**：
- 学习新快捷指令技巧
- 优化自动化流程
- 多设备协作

## Workspace结构

```
~/.openclaw/ai-team/
├── backup-manager/
│   ├── MEMORY.md           # 记忆文件
│   ├── learning-log.md     # 学习日志
│   ├── best-practices.md   # 最佳实践
│   ├── history/            # 操作历史
│   └── scripts/            # 优化脚本
│
├── file-organizer/
│   ├── MEMORY.md
│   ├── rules.json          # 分类规则
│   ├── user-preferences.md # 用户偏好
│   └── patterns/           # 识别模式
│
├── deploy-manager/
│   ├── MEMORY.md
│   ├── templates/          # 配置模板
│   ├── deployments.log     # 部署记录
│   └── optimization.md     # 优化心得
│
├── research-assistant/
│   ├── MEMORY.md
│   ├── knowledge-base/     # 知识库
│   ├── sources.json        # 可信来源
│   └── notes/              # 学习笔记
│
└── ios-automation/
    ├── MEMORY.md
    ├── shortcuts/          # 快捷指令库
    ├── automation-rules.md # 自动化规则
    └── device-configs/     # 设备配置
```

## 调用机制

### 方法1: 直接调用 (sessions_send)
```bash
# 调用备份管理员
sessions_send --label backup-manager \
  --message "备份Claude Desktop到VPS"
```

### 方法2: 智能路由
```bash
# 主AI自动判断派给哪个AI
"帮我备份XXX" → 自动路由到 Backup Manager
"整理Downloads" → 自动路由到 File Organizer
"部署网站" → 自动路由到 Deploy Manager
```

### 方法3: Cron定时任务
```bash
# 每天凌晨3点备份
cron add --schedule "0 3 * * *" \
  --session backup-manager \
  --task "执行每日备份"
```

## 学习机制

### 每次任务后
1. **记录操作**到history/
2. **更新MEMORY.md**（成功/失败经验）
3. **优化流程**（下次更快）
4. **提取模式**（形成最佳实践）

### 定期review
- 每周review学习日志
- 提炼best practices
- 更新技能树
- 淘汰过时方法

## 技能成长路径

### Level 1: 新手 (0-100次任务)
- 跟随指令
- 记录操作
- 识别基础错误
- 建立肌肉记忆

### Level 2: 熟练工 (100-1000次)
- 优化流程
- 减少重复错误
- 形成工作习惯
- 提出改进建议

### Level 3: 高级技工 (1000-5000次)
- 自主决策常规任务
- 预判常见问题
- 创新局部方案
- 可以指导新手AI

### Level 4: 准专业 (5000-10000次)
- 深度理解技术原理
- 处理复杂边界情况
- 跨领域应用知识
- 形成系统性方法论

### Level 5: 专业级 (10000+次)
- 接近人类10年经验
- 能处理未知情况
- 创造新方法和理论
- 但仍需持续学习

**注意**: 即使Level 5，AI也只是"熟练执行者"，不等同于人类20年经验的智慧和判断力。真正的专业需要理解"为什么"，而不只是"怎么做"。

## 记忆格式 (MEMORY.md)

```markdown
# [AI名称] 记忆文件

## 基本信息
- 创建时间: 2026-02-21
- 任务完成数: 15
- 当前等级: Level 2 (熟练)
- 专长: VPS备份、增量同步

## 关键经验

### 成功案例
1. **Claude Desktop 10GB备份** (2026-02-21)
   - 使用rsync -avz
   - 传输速度6MB/s
   - 耗时20分钟
   - 教训: --exclude node_modules节省30%时间

2. **OpenClaw workspace备份** (2026-02-21)
   - tar.gz压缩
   - 排除.git减少50%体积
   - 成功率100%

### 失败案例
1. **GitHub推送失败** (2026-02-21)
   - 原因: SSH认证未配置
   - 解决: 使用Personal Access Token
   - 记住: 先检查认证再推送

## 优化记录
- rsync参数优化: -avz → -avz --compress-level=6 (更快)
- 备份前检查磁盘空间 (避免失败)
- 使用md5sum验证完整性

## 用户偏好
- 喜欢简洁报告，不要冗长日志
- 优先VPS备份，GitHub次要
- 敏感数据只VPS不GitHub

## 待学习
- [ ] 学习rclone (云端备份)
- [ ] 研究deduplication (去重)
- [ ] 掌握ZFS快照

## 技能树
✅ rsync基础
✅ ssh免密登录
✅ tar压缩
⏳ 增量备份
⏳ 加密备份
❌ 云端同步
```

## 初始化流程

### Step 1: 创建Workspace
```bash
mkdir -p ~/.openclaw/ai-team/{backup-manager,file-organizer,deploy-manager,research-assistant,ios-automation}
```

### Step 2: 创建MEMORY.md模板
每个AI一个独立MEMORY.md

### Step 3: Spawn Persistent Sessions
```bash
# 不设cleanup=delete，让它们持续存在
sessions_spawn --label backup-manager \
  --task "初始化备份管理员，读取workspace，准备接受任务" \
  --cleanup keep
```

### Step 4: 注册到主AI
主AI维护一个`ai-team-roster.json`：
```json
{
  "backup-manager": {
    "sessionKey": "...",
    "status": "ready",
    "expertise": ["backup", "rsync", "vps"],
    "taskCount": 0,
    "level": 1
  }
}
```

## 主AI的角色

### 任务路由器
```
用户: "备份Claude Desktop"
主AI: 分析任务 → 路由到 backup-manager
```

### 进度监控
```
主AI: 定期检查各AI状态
如果卡住 → 介入帮助
如果完成 → 记录到总日志
```

### 知识共享
```
Backup Manager学到的技巧 → 分享给Deploy Manager
Research Assistant找到的工具 → 通知File Organizer
```

## 实现优先级

### Phase 1: 核心3个AI (立即创建)
1. Backup Manager ⭐ 最常用
2. File Organizer ⭐ 日常需要
3. Deploy Manager ⭐ 项目部署

### Phase 2: 扩展AI (1周内)
4. Research Assistant
5. iOS Automation

### Phase 3: 专业化AI (按需)
6. Database Manager
7. Security Auditor
8. Performance Optimizer

## 成功指标

### 短期 (1周)
- 3个核心AI运行稳定
- 每个完成10+任务
- MEMORY.md有实质内容

### 中期 (1月)
- AI任务成功率 > 90%
- 平均任务时间减少30%
- 用户满意度高

### 长期 (3月)
- AI能自主优化流程
- 形成best practices库
- 跨AI协作顺畅

## 注意事项

### 避免AI冲突
- 明确职责边界
- 一个任务只派一个AI
- 需要协作时主AI协调

### 记忆管理
- 定期压缩历史（保留精华）
- 避免MEMORY.md过大
- 淘汰过时经验

### 安全
- AI不能互相修改MEMORY
- 敏感操作需要主AI审批
- 定期备份AI workspace

## 下一步行动

1. 创建workspace结构
2. 初始化3个核心AI
3. 给它们第一个任务
4. 观察学习效果
5. 调整机制
