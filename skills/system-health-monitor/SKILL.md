# System Health Monitor Skill

## 目的
**一条命令快速了解整个系统状态**，避免每次都手动执行多个检查命令。

## 设计理念

主AI每次重启、接收新任务、或者不确定系统状态时，不应该：
- ❌ 执行多个单独命令（uptime, ps aux, df -h, free...）
- ❌ 花费大量时间逐个检查
- ❌ 重复相同的检查模式

应该：
- ✅ 一条命令获取所有关键指标
- ✅ 快速识别异常和问题
- ✅ 节省token和时间

---

## 快速使用

### 完整健康检查
```bash
~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh
```

**输出示例**:
```
╔══════════════════════════════════════════════╗
║     Mac Mini M4 系统健康状态               ║
╚══════════════════════════════════════════════╝

📅 时间: 2026-02-21 10:45:30
⏰ 运行时间: 25 minutes
📊 负载: 0.90 1.40 1.62 (1/5/15分钟)

💾 磁盘使用:
  /          : 6.3GB / 96GB (7%)  ✅
  /Users     : 123GB / 128GB (96%) ⚠️  接近满

🧠 内存使用:
  总计: 16GB
  已用: 8.2GB (51%) ✅
  可用: 7.8GB

🔄 关键进程:
  ✅ Ollama     : 运行中 (PID 1234)
  ❌ rsync      : 未运行
  ✅ OpenClaw   : 运行中 (PID 5678)

🌐 网络连接:
  ✅ VPS (76.13.191.45): 可达
  ✅ Internet: 正常

📱 iPhone连接:
  ✅ iPhone 15 Pro: 已连接
     存储: 123.72GB / 128GB (97%) ⚠️

⚠️  发现问题:
  1. iPhone存储接近满（97%）
  2. Downloads文件夹未整理（50+文件）

✅ 状态: 系统正常，2个警告
```

### 仅检查特定部分

```bash
# 仅检查进程
~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh --processes

# 仅检查磁盘
~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh --disk

# 仅检查内存
~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh --memory

# JSON输出（方便解析）
~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh --json
```

---

## 检查项目

### 1. 系统基础
- ✅ 运行时间（uptime）
- ✅ 系统负载（load average）
- ✅ 当前时间和时区
- ✅ 操作系统版本

### 2. 磁盘空间
- ✅ 主磁盘使用率
- ✅ 用户目录使用率
- ⚠️ >90%警告
- 🔴 >95%严重警告

### 3. 内存使用
- ✅ 总内存
- ✅ 已用内存
- ✅ 可用内存
- ⚠️ >85%警告

### 4. 关键进程
- ✅ Ollama状态
- ✅ rsync进程（备份相关）
- ✅ OpenClaw gateway
- ✅ Claude Desktop（如果在运行）
- ✅ 其他重要进程

### 5. 网络状态
- ✅ VPS连接（76.13.191.45）
- ✅ Internet连通性
- ✅ DNS解析

### 6. iOS设备
- ✅ iPhone连接状态
- ✅ iPhone存储使用
- ⚠️ 存储警告

### 7. 智能建议
根据检测结果给出：
- 🧹 Downloads需要整理
- 📦 大文件需要清理
- 🔄 备份任务需要执行
- ⚡ 服务需要重启

---

## 警告阈值

| 指标 | 正常 | 警告 | 严重 |
|------|------|------|------|
| 磁盘使用 | <80% | 80-95% | >95% |
| 内存使用 | <80% | 80-90% | >90% |
| 负载 (15min) | <2.0 | 2.0-4.0 | >4.0 |
| iPhone存储 | <80% | 80-95% | >95% |

---

## 使用场景

### 场景1: 系统刚重启
```bash
# 快速确认一切正常
~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh
```

### 场景2: 接收新任务前
```bash
# 确保有足够资源执行任务
~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh --memory --disk
```

### 场景3: 备份任务前
```bash
# 检查rsync进程和磁盘空间
~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh --processes --disk
```

### 场景4: 调试问题
```bash
# 完整检查，JSON输出方便分析
~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh --json > system-status.json
```

---

## 脚本设计

### quick-check.sh
主检查脚本，使用颜色和emoji让输出易读。

**特性**:
- 自动检测异常
- 智能建议
- 可选JSON输出
- 模块化设计

### health-monitor.json
配置文件，定义：
- 检查项目
- 警告阈值
- 监控频率
- 通知规则

---

## 集成到其他skills

### Backup Manager使用
```bash
# 备份前检查
if ! quick-check.sh --disk | grep -q "✅"; then
  echo "⚠️  磁盘空间不足，备份可能失败"
  exit 1
fi
```

### Deploy Manager使用
```bash
# 部署前检查网络
if ! quick-check.sh --network | grep -q "✅"; then
  echo "⚠️  VPS连接失败，无法部署"
  exit 1
fi
```

### File Organizer使用
```bash
# 检查是否需要整理
downloads_count=$(ls -1 ~/Downloads | wc -l)
if [ "$downloads_count" -gt 50 ]; then
  echo "📂 Downloads有${downloads_count}个文件，建议整理"
fi
```

---

## 定期检查（可选）

### 每小时检查（Heartbeat）
在 `HEARTBEAT.md` 中添加：
```markdown
# 每次heartbeat检查系统健康
~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh --silent
```

如果发现问题，自动通知用户。

### Cron定期检查
```bash
# 每6小时完整检查
0 */6 * * * ~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh --json > /tmp/health-$(date +\%Y\%m\%d-\%H).json
```

---

## 故障排查

### 脚本执行失败
```bash
# 检查执行权限
chmod +x ~/.openclaw/workspace/skills/system-health-monitor/quick-check.sh

# 检查依赖
which jq || brew install jq
```

### 输出乱码
```bash
# 设置正确的locale
export LANG=zh_CN.UTF-8
```

---

## 未来扩展

### v2.0 (计划中)
- [ ] GPU使用监控（如果有）
- [ ] 网络流量统计
- [ ] 温度监控（Apple Silicon）
- [ ] 电池状态（Mac笔记本）
- [ ] Docker容器状态

### v3.0 (长期)
- [ ] Web界面实时监控
- [ ] 历史趋势图表
- [ ] 智能异常检测（机器学习）
- [ ] 自动修复常见问题

---

## 总结

这个skill的核心价值：
1. **节省时间** - 1条命令 vs 10+条命令
2. **避免遗漏** - 自动检查所有关键指标
3. **智能提示** - 不只是数据，还有建议
4. **易于集成** - 其他AI可以调用

**使用原则**: 不确定系统状态时，先运行quick-check.sh！
