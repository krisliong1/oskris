# Skills 管理完整指南

## 🎯 目录结构说明

### 1. Claude 系统 (只读,自动加载)
```
/mnt/skills/
├── public/       # Anthropic 官方 skills (12个) - 只读
├── user/         # 你的 skills (27个) - 从 GitHub 同步
└── examples/     # Anthropic 示例 (22个) - 只读
```

### 2. GitHub 仓库 - 双重备份

#### A. skills/ - 原始分类目录
```
skills/
├── agents/              # 5个 - 你的自定义代理
├── business-workflow/   # 3个 - 业务流程
├── design-creative/     # 5个 - 设计创意
├── development-tools/   # 2个 - 开发工具
├── documents/          # 4个 - 文档处理
├── knowledge/          # 1个 - 知识库
└── web-development/    # 7个 - Web开发
```

#### B. claude-skills/ - 镜像 Claude 系统
```
claude-skills/
├── public/      # 空 (暂时)
├── user/        # 27个 - 完全镜像 /mnt/skills/user/
├── examples/    # 空 (暂时)
├── README.md    # 说明文档
└── CHANGELOG.md # 变更日志
```

---

## 🔄 工作流程

### 每次新对话时 (你需要做的)

**场景**: 开始一个新的 Claude 对话

```bash
# 在 Claude 对话框中说:
"同步我的 GitHub skills"
```

Claude 会自动执行:
```bash
git clone https://github.com/krisliong1/oskris.git
cp -r oskris/claude-skills/user/* /mnt/skills/user/
```

### 修改 Skill 时 (完整流程)

**步骤 1: 修改原始文件**
```bash
# 在 skills/ 目录修改
vim skills/agents/app-recommendations/SKILL.md
```

**步骤 2: 运行同步脚本**
```bash
./sync-skills.sh
```

这会:
- ✅ 复制到 claude-skills/user/
- ✅ 自动更新版本号
- ✅ 更新 VERSION.md 时间戳

**步骤 3: 更新 CHANGELOG**
```bash
# 在 claude-skills/CHANGELOG.md 顶部添加
## 2026-02-16

### UPDATE - app-recommendations v1.0.1
- 优化推荐逻辑
- 添加新的 App 数据库
```

**步骤 4: 提交到 GitHub**
```bash
git add .
git commit -m "Update app-recommendations v1.0.1"
git push
```

### 新增 Skill 时

**步骤 1: 创建在 skills/ 目录**
```bash
mkdir -p skills/agents/new-skill
vim skills/agents/new-skill/SKILL.md
```

**步骤 2: 运行同步脚本**
```bash
./sync-skills.sh
```

**步骤 3: 更新 CHANGELOG**
```bash
# 添加到 claude-skills/CHANGELOG.md
### ADD - new-skill v1.0.0
- 功能说明
```

**步骤 4: 提交**
```bash
git add .
git commit -m "Add new-skill v1.0.0"
git push
```

---

## 🔍 如何识别新旧 Skill

### 方法 1: 查看 VERSION.md (最简单)

```bash
# 查看单个 skill
cat claude-skills/user/app-recommendations/VERSION.md

# 查看所有 skills 的更新时间
grep -h "日期:" claude-skills/user/*/VERSION.md | sort -r
```

输出示例:
```
- **日期**: 2026-02-16 14:30:00  ← 最新
- **日期**: 2026-02-15 10:20:00
- **日期**: 2026-02-14 16:45:00
```

### 方法 2: 查看 CHANGELOG.md

```bash
head -50 claude-skills/CHANGELOG.md
```

最新的修改在最上面!

### 方法 3: Git 历史

```bash
# 查看某个 skill 的修改历史
git log --oneline claude-skills/user/app-recommendations/

# 查看最近修改的文件
git log --name-only --since="1 week ago"
```

---

## 📊 对比表格

| 位置 | 路径 | 数量 | 作用 | 可修改 |
|------|------|------|------|--------|
| Claude 系统 | `/mnt/skills/user/` | 27 | 运行时使用 | ❌ 每次重置 |
| GitHub 原始 | `oskris/skills/` | 27 | 源代码管理 | ✅ 主要编辑这里 |
| GitHub 镜像 | `oskris/claude-skills/user/` | 27 | 同步到 Claude | ✅ 自动同步 |

---

## ⚙️ 自动化脚本

### sync-skills.sh - 同步脚本

**功能**:
- 从 skills/ 复制到 claude-skills/user/
- 自动更新版本号
- 更新 VERSION.md 时间戳

**使用**:
```bash
./sync-skills.sh
```

**输出**:
```
🔄 开始同步 skills...
📁 清空目标目录...
📦 复制 skills...
  ✓ agents: 5 个 skills
  ✓ development-tools: 2 个 skills
  ...
📝 更新版本信息...
  ✓ app-recommendations - v1.0.1
  ✓ auto-translate - v1.0.0
  ...
✅ 全部完成!
```

---

## 🚨 常见问题

### Q: 为什么要有两个目录 (skills/ 和 claude-skills/)?

**A**: 
- **skills/** - 按功能分类,方便人类查看和管理
- **claude-skills/** - 镜像 Claude 系统结构,方便直接同步

### Q: 我修改了 skill,但 Claude 没用到新版本?

**A**: 两个可能:
1. ❌ 没推送到 GitHub → `git push`
2. ❌ 没在新对话中同步 → 说 "同步我的 GitHub skills"

### Q: 怎么知道哪个是新的 skill?

**A**: 3个方法任选:
1. 看 `VERSION.md` 的日期
2. 看 `CHANGELOG.md` 的记录
3. 用 `git log` 查看历史

### Q: sync-skills.sh 做了什么?

**A**: 
```
skills/ (分类结构)
    ↓ 复制
claude-skills/user/ (扁平结构)
    ↓ 添加 VERSION.md
    ↓ 更新版本号
完成!
```

---

## ✅ 最佳实践

### 1. 修改 Skill 的标准流程

```
修改 skills/xxx/SKILL.md
    ↓
运行 ./sync-skills.sh
    ↓
更新 CHANGELOG.md
    ↓
git commit + push
    ↓
新对话中同步
```

### 2. 版本号规则

- **v1.0.0** - 初始版本
- **v1.0.x** - 小修改 (修bug,调参数)
- **v1.x.0** - 中等修改 (新功能,优化逻辑)
- **vx.0.0** - 大改版 (重构,API变更)

### 3. CHANGELOG 记录规范

```markdown
## 2026-02-16

### UPDATE - app-recommendations v1.0.1
- 修改内容: 优化推荐算法
- 影响: 推荐更准确
- 测试: 已验证

### ADD - new-skill v1.0.0
- 功能: 新的自动化工具
- 场景: XX场景使用
```

---

## 📝 总结

**你需要记住的**:
1. ✅ 修改在 `skills/` 目录
2. ✅ 运行 `./sync-skills.sh`
3. ✅ 更新 `CHANGELOG.md`
4. ✅ Git commit + push
5. ✅ 新对话说 "同步 GitHub skills"

**识别新旧的方法**:
1. 🔍 看 `VERSION.md` 日期
2. 📋 看 `CHANGELOG.md` 
3. 🔄 用 Git 历史

就这么简单! 🎉
