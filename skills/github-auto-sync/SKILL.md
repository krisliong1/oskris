# GitHub自动同步机制

## 功能
自动将 `skills/` 目录的变化同步到GitHub，保护所有研究成果免受本地故障影响。

## 机制
- **Git post-commit hook** (`.git/hooks/post-commit`)
- 每次commit后自动检测skills/目录变化
- 检测到变化时自动执行 `git push origin main`
- 记录同步日志到 `logs/skills-sync.log`

## 安装
Hook已自动安装到 `~/.openclaw/workspace/.git/hooks/post-commit`

验证安装:
```bash
ls -lh ~/.openclaw/workspace/.git/hooks/post-commit
# 应该显示可执行权限 (-rwxr-xr-x)
```

## 使用
创建或编辑skill后，只需正常commit：

```bash
cd ~/.openclaw/workspace
git add skills/your-skill/
git commit -m "add/update: your skill"
# 🔄 自动触发GitHub推送！
```

Hook会：
1. ✅ 检测本次commit是否涉及 `skills/` 目录
2. ✅ 如果是，自动执行 `git push origin main`
3. ✅ 显示同步状态并记录日志

## 查看同步日志
```bash
tail -f ~/.openclaw/workspace/logs/skills-sync.log
```

## 前置条件
需要配置GitHub SSH认证（一次性设置）：

### 方法1: SSH Key (推荐)
```bash
# 1. 查看公钥
cat ~/.ssh/id_ed25519.pub

# 2. 添加到GitHub
# - 访问 https://github.com/settings/keys
# - 点击 "New SSH key"
# - 粘贴公钥内容
# - 保存

# 3. 测试连接
ssh -T git@github.com
# 应该显示: Hi krisliong1! You've successfully authenticated
```

### 方法2: Personal Access Token
```bash
# 如果使用HTTPS，需要更新token
git remote set-url origin https://YOUR_TOKEN@github.com/krisliong1/openclaw.git
```

## 故障排查

### 问题1: "Permission denied (publickey)"
**原因**: SSH key未添加到GitHub  
**解决**: 参见上方"前置条件" → 方法1

### 问题2: "Authentication failed"
**原因**: Personal Access Token过期  
**解决**: 
1. 生成新token: https://github.com/settings/tokens
2. 更新remote URL (参见方法2)

### 问题3: 自动push失败
**临时方案**: 手动推送
```bash
cd ~/.openclaw/workspace
git push origin main
```

**根本解决**: 检查网络连接和GitHub认证

### 问题4: Hook未触发
**检查执行权限**:
```bash
chmod +x ~/.openclaw/workspace/.git/hooks/post-commit
```

## 监控
定期检查同步日志，确保skills持续备份：
```bash
# 查看最近5次同步
tail -5 ~/.openclaw/workspace/logs/skills-sync.log

# 查看失败记录
grep FAILED ~/.openclaw/workspace/logs/skills-sync.log
```

## 设计理念
**自动化 > 手动**  
创建skill时不应该还要想"记得push"，系统应该自动保护你的工作成果。

**无感知保护**  
正常的git workflow不变，只是多了一层自动保护网。

**可观测**  
日志让你知道备份是否成功，出问题能快速发现。

---

**创建时间**: 2026-02-22  
**创建原因**: 14个新skills差点因本地故障丢失  
**创建者**: Backup Manager (subagent)
