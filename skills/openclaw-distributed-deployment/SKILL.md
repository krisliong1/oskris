# OpenClaw Distributed Deployment

**类型**: Infrastructure / DevOps  
**难度**: 中级  
**维护者**: VPS Distributed Systems Researcher  
**版本**: 1.0  
**最后更新**: 2026-02-22  

---

## 概述

本skill提供OpenClaw的分布式部署指南，实现Mac mini和VPS之间的数据同步和故障转移能力。

**核心目标**：
- 🔄 自动同步workspace和配置到VPS
- 🛡️ 提供disaster recovery能力
- ⚡ 支持快速failover（<15分钟）
- 💰 零成本（使用Oracle Free Tier）

**架构模式**: Active-Standby（主备模式）

---

## 前置要求

### Mac mini（Primary）
- ✅ OpenClaw已安装并运行
- ✅ SSH访问到VPS
- ✅ 至少20GB可用空间

### VPS（Standby）
- ✅ Ubuntu 20.04+ 或 Debian 11+
- ✅ 1GB+ RAM（推荐2GB）
- ✅ 20GB+ 存储空间
- ✅ 公网IP或Tailscale
- ✅ SSH访问权限

### 网络
- ✅ Mac到VPS的SSH连接
- ✅ 低延迟网络（<200ms RTT优先）

---

## 快速开始（30分钟）

### 步骤1: VPS初始化（10分钟）

```bash
# 在VPS上执行
# 1. 更新系统
sudo apt update && sudo apt upgrade -y

# 2. 安装Node.js 20+
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 3. 安装pnpm
npm install -g pnpm

# 4. 安装OpenClaw
pnpm install -g openclaw

# 5. 创建目录结构
mkdir -p ~/.openclaw/workspace
mkdir -p ~/.openclaw/backups
mkdir -p ~/.openclaw/logs
mkdir -p ~/.openclaw/scripts

# 6. 验证安装
openclaw --version
```

### 步骤2: SSH密钥配置（5分钟）

```bash
# 在Mac上
# 1. 生成SSH密钥（如果没有）
ssh-keygen -t ed25519 -C "openclaw-sync"

# 2. 复制公钥到VPS
ssh-copy-id user@vps-ip

# 3. 测试免密登录
ssh user@vps-ip "echo 'SSH works!'"

# 4. 配置SSH别名（可选）
cat >> ~/.ssh/config << EOF
Host openclaw-vps
    HostName vps-ip
    User user
    IdentityFile ~/.ssh/id_ed25519
EOF

# 现在可以用：ssh openclaw-vps
```

### 步骤3: 同步脚本部署（10分钟）

#### 3.1 创建workspace同步脚本

```bash
# 在Mac上：~/.openclaw/scripts/sync-to-vps.sh
cat > ~/.openclaw/scripts/sync-to-vps.sh << 'EOF'
#!/bin/bash

# 配置
VPS_HOST="openclaw-vps"  # 或 "user@vps-ip"
LOCAL_BASE="$HOME/.openclaw"
REMOTE_BASE="/home/user/.openclaw"
LOG_FILE="$LOCAL_BASE/logs/sync.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Starting sync to VPS ==="

# 1. 同步workspace（skills, memory, agents配置）
log "Syncing workspace..."
rsync -avz --delete \
    --exclude '.git' \
    --exclude 'node_modules' \
    --exclude '*.log' \
    --exclude '.DS_Store' \
    --exclude 'logs/' \
    "$LOCAL_BASE/workspace/" \
    "$VPS_HOST:$REMOTE_BASE/workspace/" \
    >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "✅ Workspace synced successfully"
else
    log "❌ Workspace sync failed!"
    exit 1
fi

# 2. 同步配置文件（不包括敏感credentials）
log "Syncing config..."
rsync -avz \
    "$LOCAL_BASE/openclaw.json" \
    "$LOCAL_BASE/exec-approvals.json" \
    "$VPS_HOST:$REMOTE_BASE/" \
    >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "✅ Config synced successfully"
else
    log "❌ Config sync failed!"
    exit 1
fi

# 3. 统计信息
WORKSPACE_SIZE=$(du -sh "$LOCAL_BASE/workspace" | cut -f1)
log "Workspace size: $WORKSPACE_SIZE"
log "=== Sync completed ==="
EOF

chmod +x ~/.openclaw/scripts/sync-to-vps.sh
```

#### 3.2 创建完整备份脚本

```bash
# 在Mac上：~/.openclaw/scripts/backup-state.sh
cat > ~/.openclaw/scripts/backup-state.sh << 'EOF'
#!/bin/bash

# 配置
VPS_HOST="openclaw-vps"
LOCAL_BASE="$HOME/.openclaw"
BACKUP_DIR="$LOCAL_BASE/backups"
DATE=$(date +%Y-%m-%d-%H%M)
LOG_FILE="$LOCAL_BASE/logs/backup.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Starting full state backup ==="

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份文件名
BACKUP_FILE="$BACKUP_DIR/openclaw-state-$DATE.tar.gz"

# 备份整个state（包括credentials）
log "Creating backup archive..."
tar -czf "$BACKUP_FILE" \
    -C "$LOCAL_BASE" \
    --exclude='logs/*' \
    --exclude='backups/*' \
    --exclude='*.log' \
    credentials/ \
    browser/ \
    devices/ \
    agents/ \
    cron/ \
    exec-approvals.json \
    openclaw.json \
    >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    BACKUP_SIZE=$(du -sh "$BACKUP_FILE" | cut -f1)
    log "✅ Backup created: $BACKUP_FILE ($BACKUP_SIZE)"
else
    log "❌ Backup creation failed!"
    exit 1
fi

# 上传到VPS
log "Uploading to VPS..."
scp "$BACKUP_FILE" "$VPS_HOST:$REMOTE_BASE/backups/" >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "✅ Backup uploaded to VPS"
else
    log "❌ Upload failed!"
    exit 1
fi

# 清理旧备份（保留最近7天）
log "Cleaning old backups..."
find "$BACKUP_DIR" -name "openclaw-state-*.tar.gz" -mtime +7 -delete
ssh "$VPS_HOST" "find $REMOTE_BASE/backups -name 'openclaw-state-*.tar.gz' -mtime +7 -delete"

log "=== Backup completed ==="
EOF

chmod +x ~/.openclaw/scripts/backup-state.sh
```

### 步骤4: 配置自动化（5分钟）

```bash
# 在Mac上添加cron任务
crontab -e

# 添加以下行：
# 每5分钟同步workspace
*/5 * * * * /Users/openclaw/.openclaw/scripts/sync-to-vps.sh >> /Users/openclaw/.openclaw/logs/cron.log 2>&1

# 每天3AM完整备份
0 3 * * * /Users/openclaw/.openclaw/scripts/backup-state.sh >> /Users/openclaw/.openclaw/logs/cron.log 2>&1

# 保存退出（:wq）
```

### 步骤5: 验证部署

```bash
# 在Mac上
# 1. 手动运行一次同步
~/.openclaw/scripts/sync-to-vps.sh

# 2. 检查VPS
ssh openclaw-vps "ls -lh ~/.openclaw/workspace/"

# 3. 手动运行一次备份
~/.openclaw/scripts/backup-state.sh

# 4. 检查日志
tail -f ~/.openclaw/logs/sync.log
```

---

## 故障转移（Failover）流程

### 场景：Mac Gateway挂了，需要切换到VPS

#### 前置条件检查
```bash
# 1. VPS可访问
ssh openclaw-vps

# 2. 最新备份存在
ls -lh ~/.openclaw/backups/

# 3. workspace已同步
ls -lh ~/.openclaw/workspace/SOUL.md
```

#### Failover步骤（15分钟）

##### 1. 恢复State（5分钟）

```bash
# 在VPS上
cd ~/.openclaw/backups

# 找到最新备份
LATEST_BACKUP=$(ls -t openclaw-state-*.tar.gz | head -1)
echo "Restoring from: $LATEST_BACKUP"

# 解压到正确位置
tar -xzf "$LATEST_BACKUP" -C ~/.openclaw/

# 验证
ls -lh ~/.openclaw/credentials/
```

##### 2. 重新登录消息Channels（5-10分钟）

```bash
# 在VPS上

# WhatsApp（需要扫码）
openclaw channels login whatsapp
# 用手机WhatsApp扫描二维码

# Telegram（需要验证码）
openclaw channels login telegram
# 输入手机号，输入收到的验证码

# Discord（使用bot token，无需重新登录）
# 已包含在openclaw.json中
```

##### 3. 启动VPS Gateway（2分钟）

```bash
# 在VPS上
# 1. 前台测试启动
openclaw gateway

# 观察日志，确保无错误

# 2. 如果正常，按Ctrl+C停止，安装为服务
openclaw gateway install

# 3. 启动服务
openclaw gateway start

# 4. 检查状态
openclaw gateway status
```

##### 4. 验证（3分钟）

```bash
# 在Discord/Telegram发送消息测试
# 检查agent是否响应

# 检查workspace
openclaw workspace ls

# 检查logs
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
```

#### Failback到Mac（切换回来）

```bash
# 1. 在VPS上停止Gateway
ssh openclaw-vps "openclaw gateway stop"

# 2. 在Mac上恢复最新state（如果需要）
# VPS可能产生了新数据，同步回Mac
rsync -avz openclaw-vps:~/.openclaw/workspace/ ~/.openclaw/workspace/

# 3. 在Mac上启动Gateway
openclaw gateway start

# 4. 验证
openclaw status
```

---

## VPS监控脚本

### 备份验证脚本

在VPS上创建 `~/.openclaw/scripts/verify-backup.sh`：

```bash
#!/bin/bash

WORKSPACE="$HOME/.openclaw/workspace"
BACKUPS="$HOME/.openclaw/backups"
LOG_FILE="$HOME/.openclaw/logs/verify.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Backup Verification Start ==="

# 检查关键文件
check_file() {
    if [ -f "$1" ]; then
        log "✅ $1 exists"
        return 0
    else
        log "❌ $1 MISSING!"
        return 1
    fi
}

ERRORS=0

# 检查workspace关键文件
check_file "$WORKSPACE/SOUL.md" || ((ERRORS++))
check_file "$WORKSPACE/AGENTS.md" || ((ERRORS++))
check_file "$WORKSPACE/USER.md" || ((ERRORS++))
check_file "$HOME/.openclaw/openclaw.json" || ((ERRORS++))

# 检查backup存在
LATEST_BACKUP=$(ls -t $BACKUPS/openclaw-state-*.tar.gz 2>/dev/null | head -1)
if [ -n "$LATEST_BACKUP" ]; then
    BACKUP_AGE=$(stat -c %Y "$LATEST_BACKUP")
    NOW=$(date +%s)
    AGE_HOURS=$(( ($NOW - $BACKUP_AGE) / 3600 ))
    log "✅ Latest backup: $LATEST_BACKUP (${AGE_HOURS}h old)"
    
    if [ $AGE_HOURS -gt 48 ]; then
        log "⚠️  WARNING: Backup is older than 48h!"
        ((ERRORS++))
    fi
else
    log "❌ No backups found!"
    ((ERRORS++))
fi

# 检查workspace同步时间
if [ -f "$WORKSPACE/SOUL.md" ]; then
    SYNC_AGE=$(stat -c %Y "$WORKSPACE/SOUL.md")
    SYNC_AGE_MIN=$(( ($NOW - $SYNC_AGE) / 60 ))
    log "ℹ️  Last sync: ${SYNC_AGE_MIN} minutes ago"
    
    if [ $SYNC_AGE_MIN -gt 15 ]; then
        log "⚠️  WARNING: No sync in 15+ minutes!"
        ((ERRORS++))
    fi
fi

# 总结
log "=== Verification Complete ==="
if [ $ERRORS -eq 0 ]; then
    log "✅ All checks passed!"
    exit 0
else
    log "❌ $ERRORS errors found!"
    exit 1
fi
```

### 健康检查脚本

在VPS上创建 `~/.openclaw/scripts/health-check.sh`：

```bash
#!/bin/bash

MAC_HOST="mac-mini-ip"  # 或Tailscale地址
GATEWAY_PORT=18789
LOG_FILE="$HOME/.openclaw/logs/health.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查Mac Gateway是否响应
log "Checking Mac Gateway at $MAC_HOST:$GATEWAY_PORT..."

# 尝试连接（超时5秒）
timeout 5 bash -c "cat < /dev/null > /dev/tcp/$MAC_HOST/$GATEWAY_PORT" 2>/dev/null

if [ $? -eq 0 ]; then
    log "✅ Mac Gateway is UP"
    exit 0
else
    log "❌ Mac Gateway is DOWN!"
    
    # 可选：发送告警
    # curl -X POST https://your-webhook-url \
    #     -H "Content-Type: application/json" \
    #     -d '{"text": "Mac Gateway is DOWN!"}'
    
    exit 1
fi
```

### 配置VPS上的监控cron

```bash
# 在VPS上
crontab -e

# 每天9AM验证备份
0 9 * * * /home/user/.openclaw/scripts/verify-backup.sh

# 每小时检查Mac健康状态
0 * * * * /home/user/.openclaw/scripts/health-check.sh
```

---

## 维护和运维

### 日常检查清单

**每天**：
- [ ] 检查sync.log确保同步正常
- [ ] 检查backup.log确保备份成功
- [ ] 查看VPS verify报告邮件

**每周**：
- [ ] 在VPS上验证workspace完整性
- [ ] 测试SSH连接
- [ ] 检查磁盘空间

**每月**：
- [ ] 完整Failover演练（Mac → VPS → Mac）
- [ ] 更新OpenClaw到最新版本（Mac和VPS）
- [ ] 清理旧日志和备份

### 监控指标

```bash
# 在Mac上
# 检查同步状态
tail -20 ~/.openclaw/logs/sync.log

# 检查磁盘使用
du -sh ~/.openclaw/*

# 检查cron任务
crontab -l
ps aux | grep openclaw

# 在VPS上
ssh openclaw-vps "du -sh ~/.openclaw/*"
ssh openclaw-vps "df -h"
```

### 故障排查

#### 问题：rsync连接失败

**症状**：
```
rsync: connection unexpectedly closed
ssh: connect to host vps-ip port 22: Connection refused
```

**解决**：
```bash
# 1. 检查SSH连接
ssh openclaw-vps "echo OK"

# 2. 检查SSH配置
cat ~/.ssh/config

# 3. 检查防火墙
ssh openclaw-vps "sudo ufw status"

# 4. 检查VPS SSH服务
ssh openclaw-vps "sudo systemctl status ssh"
```

#### 问题：VPS启动后收不到消息

**症状**：
- Gateway启动正常
- 但Discord/Telegram bot无响应

**解决**：
```bash
# 1. 检查channel登录状态
openclaw channels status

# 2. 重新登录
openclaw channels login whatsapp
openclaw channels login telegram

# 3. 检查配置
cat ~/.openclaw/openclaw.json | grep -A 10 "channels"

# 4. 检查logs
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -i "channel\|login\|auth"
```

#### 问题：workspace文件冲突

**症状**：
```
rsync: some files could not be transferred
```

**解决**：
```bash
# 1. 强制同步（Mac覆盖VPS）
rsync -avz --delete ~/.openclaw/workspace/ openclaw-vps:~/.openclaw/workspace/

# 2. 检查文件权限
ssh openclaw-vps "ls -la ~/.openclaw/workspace/"

# 3. 清理VPS workspace重新同步
ssh openclaw-vps "rm -rf ~/.openclaw/workspace/*"
~/.openclaw/scripts/sync-to-vps.sh
```

---

## 高级配置

### 使用Tailscale提高安全性

```bash
# 在Mac和VPS上安装Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# 获取VPS的Tailscale IP
ssh vps-ip "tailscale ip -4"
# 例如：100.64.1.2

# 更新sync脚本使用Tailscale地址
VPS_HOST="user@100.64.1.2"
```

**优点**：
- 加密连接
- 无需公网IP
- 自动穿透NAT

### 增量备份优化

```bash
# 修改backup-state.sh，使用增量备份
# 在tar命令后添加：

# 只备份变化的文件
PREV_BACKUP=$(ls -t $BACKUP_DIR/openclaw-state-*.tar.gz 2>/dev/null | head -2 | tail -1)

if [ -n "$PREV_BACKUP" ]; then
    tar -czf "$BACKUP_FILE" \
        --newer-mtime="$(stat -c %y "$PREV_BACKUP")" \
        -C "$LOCAL_BASE" \
        credentials/ browser/ devices/ agents/ ...
fi
```

### 只读VPS Gateway（未来）

```bash
# 在VPS上以只读模式启动Gateway
# 可以查询状态，但不处理消息

# 修改openclaw.json
{
  "channels": {
    "whatsapp": { "enabled": false },
    "telegram": { "enabled": false },
    "discord": { "enabled": false }
  }
}

# 启动Gateway（只提供查询API）
openclaw gateway start
```

---

## 成本分析

### Oracle Cloud Free Tier（推荐）

| 资源 | Free Tier配额 | 本方案使用 |
|------|--------------|----------|
| ARM Compute | 4 OCPUs | 1 OCPU ✅ |
| RAM | 24GB | 1GB ✅ |
| 存储 | 200GB | 20GB ✅ |
| 出站流量 | 10TB/月 | ~3GB/月 ✅ |

**成本**: **$0/月** ✅ 永久免费

### 其他VPS选项

| 提供商 | 配置 | 价格/月 |
|--------|------|--------|
| Hetzner | 2GB RAM, 20GB SSD | €4.15 (~$4.5) |
| DigitalOcean | 1GB RAM, 25GB SSD | $6 |
| Vultr | 1GB RAM, 25GB SSD | $6 |
| Linode | 1GB RAM, 25GB SSD | $5 |

### 流量消耗估算

| 项目 | 频率 | 大小 | 月流量 |
|------|------|------|--------|
| workspace同步 | 每5分钟 | ~1MB（增量） | ~9GB |
| 完整备份 | 每天 | ~100MB | ~3GB |
| 监控/心跳 | 每小时 | ~1KB | ~1MB |
| **总计** | - | - | **~12GB/月** ✅ |

---

## 安全建议

### SSH安全
- ✅ 使用SSH密钥，禁用密码登录
- ✅ 修改默认SSH端口（可选）
- ✅ 启用UFW防火墙
- ✅ 定期轮换密钥

### 备份加密
```bash
# 加密备份文件
tar -czf - credentials/ | gpg -c > backup-encrypted.tar.gz.gpg

# 解密
gpg -d backup-encrypted.tar.gz.gpg | tar -xz
```

### Credentials管理
- ⚠️ 不要将credentials放入Git
- ✅ 使用rsync传输，确保SSH加密
- ✅ VPS上的备份文件设置权限600

```bash
chmod 600 ~/.openclaw/backups/*
chmod 700 ~/.openclaw/credentials
```

---

## 参考资料

### OpenClaw官方文档
- [VPS Hosting](https://docs.openclaw.ai/vps)
- [Remote Access](https://docs.openclaw.ai/platforms/mac/remote)
- [Multiple Gateways](https://docs.openclaw.ai/gateway/multiple-gateways)
- [Configuration](https://docs.openclaw.ai/gateway/configuration)

### 本地文档路径
- VPS部署：`/opt/homebrew/lib/node_modules/openclaw/docs/vps.md`
- Remote控制：`/opt/homebrew/lib/node_modules/openclaw/docs/platforms/mac/remote.md`
- Gateway配置：`/opt/homebrew/lib/node_modules/openclaw/docs/gateway/configuration-reference.md`

### 相关Skill
- `backup-and-restore` - 备份恢复流程
- `system-monitoring` - 系统监控

---

## 更新日志

### v1.0 (2026-02-22)
- ✅ 初始版本
- ✅ Active-Standby架构
- ✅ rsync同步方案
- ✅ Failover流程
- ✅ 监控脚本

### 未来计划
- [ ] 自动failover检测
- [ ] Grafana监控Dashboard
- [ ] 增量备份优化
- [ ] 多region支持

---

**维护者**: VPS Distributed Systems Researcher  
**联系方式**: 通过AI Team roster  
**最后审核**: 2026-02-22  
