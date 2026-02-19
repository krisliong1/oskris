---
name: github-skills-sync
description: 每次新对话自动从 GitHub 同步最新 skills 到 /mnt/skills/user/。确保 Claude 始终使用最新版本的 skills。
---

# GitHub Skills 自动同步

> **🎯 目标**: 每次新对话开始时,自动同步 GitHub 上的最新 skills

## 📌 核心原则

1. **自动触发**: 新对话开始时自动执行
2. **静默同步**: 不询问用户,直接同步
3. **即时反馈**: 同步完成后简短通知
4. **不打断流程**: 同步在后台完成,然后正常对话

## 🔄 触发条件

### 何时自动同步

**必须同步的情况:**
- ✅ 用户的第一条消息
- ✅ 用户明确说 "同步 skills" / "更新 skills" / "导入 skills"
- ✅ 检测到 /mnt/skills/user/ 为空或 skills 少于 5 个

**不需要同步的情况:**
- ❌ 对话进行中(已经同步过)
- ❌ 用户只是问普通问题

## 🚀 执行流程

### 标准同步流程

```bash
# 1. 克隆最新仓库
cd /tmp
rm -rf oskris
git clone https://github.com/krisliong1/oskris.git

# 2. 同步到 /mnt/skills/user/
cp -r oskris/claude-skills/user/* /mnt/skills/user/

# 3. 验证
skill_count=$(ls /mnt/skills/user/ | wc -l)
echo "✅ 已同步 $skill_count 个 skills"
```

### 完整命令

```bash
cd /tmp && \
rm -rf oskris && \
git clone https://github.com/krisliong1/oskris.git && \
cp -r oskris/claude-skills/user/* /mnt/skills/user/ && \
echo "✅ Skills 同步完成: $(ls /mnt/skills/user/ | wc -l) 个"
```

## 💬 响应模板

### 成功同步

**简短版 (默认)**:
```
✅ 已同步 27 个 skills
```

**详细版 (用户要求时)**:
```
✅ Skills 同步完成

📊 统计:
- 总数: 27 个
- 来源: GitHub krisliong1/oskris
- 时间: 2026-02-15 14:30

📝 分类:
- Agents: 5 个
- Web Development: 7 个
- Documents: 4 个
- Design Creative: 5 个
- Development Tools: 2 个
- Business Workflow: 3 个
- Knowledge: 1 个

💡 现在可以使用所有最新的 skills 了!
```

### 同步失败

```
⚠️ Skills 同步失败

可能原因:
- GitHub 连接问题
- 仓库地址变更
- 网络问题

你可以:
1. 稍后重试: 说 "同步 skills"
2. 手动上传 skills 到 Claude.ai Settings
```

## 🎯 使用示例

### 示例 1: 新对话自动同步

```
用户: "你好,帮我做个 PPT"

Claude:
[自动执行同步]
✅ 已同步 27 个 skills

好的,我来帮你制作 PPT。你想做什么主题的?
```

### 示例 2: 用户主动同步

```
用户: "同步我的 GitHub skills"

Claude:
[执行同步命令]
✅ Skills 同步完成

📊 统计:
- 总数: 27 个
- 最新版本已加载

现在可以使用所有更新后的 skills 了!
```

### 示例 3: 检测到需要同步

```
用户: "用我的 app-recommendations skill 帮我推荐 App"

Claude:
[检查 /mnt/skills/user/ 是否有此 skill]
[发现没有 → 自动同步]
✅ 已同步 skills

好的,我来用 app-recommendations skill 帮你推荐...
```

## 🔍 自检逻辑

### 决定是否同步的检查

```python
# 伪代码
def should_sync_skills():
    # 检查 1: 是否是新对话的第一条消息
    if is_first_message:
        return True
    
    # 检查 2: 用户明确要求同步
    if user_message.contains("同步", "更新", "导入") and user_message.contains("skill"):
        return True
    
    # 检查 3: skills 目录为空或太少
    skill_count = count_skills_in_user_dir()
    if skill_count < 5:
        return True
    
    # 检查 4: 用户提到某个 skill,但找不到
    mentioned_skill = extract_skill_name(user_message)
    if mentioned_skill and not skill_exists(mentioned_skill):
        return True
    
    return False
```

## ⚠️ 重要注意事项

### 安全检查

1. **GitHub 地址验证**
   - 仓库: `krisliong1/oskris`
   - 路径: `claude-skills/user/`

2. **文件完整性**
   - 每个 skill 必须有 `SKILL.md`
   - 验证文件数量 (应该是 27 个)

3. **错误处理**
   - Git clone 失败 → 通知用户
   - 复制失败 → 通知用户
   - Skills 数量不对 → 警告用户

### 性能考虑

1. **只在需要时同步**
   - 不要每条消息都同步
   - 第一条消息同步一次就够了

2. **超时处理**
   - Git clone 最多等待 30 秒
   - 失败后提示用户

## 📝 实现细节

### 完整的同步命令

```bash
#!/bin/bash
set -e

echo "🔄 开始同步 GitHub skills..."

# 1. 清理旧的克隆
cd /tmp
rm -rf oskris

# 2. 克隆最新版本
git clone https://github.com/krisliong1/oskris.git

# 3. 验证目录存在
if [ ! -d "oskris/claude-skills/user" ]; then
    echo "❌ 错误: claude-skills/user 目录不存在"
    exit 1
fi

# 4. 同步到 skills 目录
cp -r oskris/claude-skills/user/* /mnt/skills/user/

# 5. 验证同步结果
skill_count=$(ls /mnt/skills/user/ | wc -l)

if [ "$skill_count" -lt 20 ]; then
    echo "⚠️ 警告: 只同步了 $skill_count 个 skills,可能不完整"
else
    echo "✅ Skills 同步完成: $skill_count 个"
fi
```

## 🎛️ 配置选项

### 可自定义的参数

```yaml
github:
  repo: "krisliong1/oskris"
  branch: "main"
  path: "claude-skills/user"

sync:
  auto_sync_first_message: true
  min_skills_threshold: 5
  timeout_seconds: 30
  
notifications:
  verbose: false  # false=简短通知, true=详细统计
```

## ✅ 测试清单

- [ ] 新对话第一条消息自动同步
- [ ] 用户说 "同步 skills" 能正确执行
- [ ] 同步后 skills 数量正确 (27 个)
- [ ] 同步失败时有错误提示
- [ ] 不会重复同步同一对话
- [ ] 响应简洁不啰嗦

## 📚 相关文档

- GitHub 仓库: https://github.com/krisliong1/oskris
- Skills 目录: `claude-skills/user/`
- 变更日志: `claude-skills/CHANGELOG.md`

## 🔗 相关 Skills

- `github-change-tracker` - 追踪 GitHub 文件变更
- `smart-info-manager` - 自动保存信息到 GitHub

---

**记住**: 
- ✅ 第一条消息 → 自动同步
- ✅ 简短通知 → 不啰嗦
- ✅ 静默执行 → 不打断
