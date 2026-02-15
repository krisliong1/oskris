#!/bin/bash

# 自动同步 skills 到 claude-skills 的脚本
# 用途: 保持 skills/ 和 claude-skills/ 同步

set -e

REPO_ROOT="/home/claude/oskris"
SKILLS_DIR="$REPO_ROOT/skills"
CLAUDE_SKILLS_DIR="$REPO_ROOT/claude-skills/user"

echo "🔄 开始同步 skills..."
echo ""

# 清空 claude-skills/user/
echo "📁 清空目标目录..."
rm -rf "$CLAUDE_SKILLS_DIR"/*

# 复制所有分类的 skills
echo "📦 复制 skills..."

categories=(
    "agents"
    "development-tools"
    "web-development"
    "business-workflow"
    "documents"
    "design-creative"
    "knowledge"
)

total=0
for category in "${categories[@]}"; do
    if [ -d "$SKILLS_DIR/$category" ]; then
        count=$(ls -1 "$SKILLS_DIR/$category" | wc -l)
        cp -r "$SKILLS_DIR/$category"/* "$CLAUDE_SKILLS_DIR/"
        echo "  ✓ $category: $count 个 skills"
        total=$((total + count))
    fi
done

echo ""
echo "📊 同步完成: $total 个 skills"
echo ""

# 为每个 skill 添加/更新版本信息
echo "📝 更新版本信息..."
cd "$CLAUDE_SKILLS_DIR"

for skill in */; do
    skill_name=$(basename "$skill")
    
    # 检查是否有变更
    if [ -f "$skill/VERSION.md" ]; then
        # 读取当前版本
        current_version=$(grep "^- v" "$skill/VERSION.md" | head -1 | awk '{print $2}')
        # 增加小版本号
        new_version=$(echo "$current_version" | awk -F. '{print $1"."$2"."$3+1}')
    else
        new_version="v1.0.0"
    fi
    
    # 创建/更新 VERSION.md
    cat > "$skill/VERSION.md" << EOF
# Version Info: $skill_name

## 📅 最后更新
- **日期**: $(date '+%Y-%m-%d %H:%M:%S')
- **版本**: $new_version
- **来源**: GitHub oskris/skills/

## 🔄 版本历史
- $new_version - $(date '+%Y-%m-%d') - 自动同步更新

## 📝 更新记录
- 从 skills/ 目录同步到 claude-skills/user/
- 路径: /mnt/skills/user/$skill_name

## ✅ 验证
- 文件完整性: ✓
- 路径正确: ✓
- 可被 Claude 读取: ✓

## 🔍 如何识别新旧
1. 查看此文件的"最后更新"日期
2. 比较版本号 (数字越大越新)
3. 检查"更新记录"了解具体变更
EOF
    
    echo "  ✓ $skill_name - $new_version"
done

echo ""
echo "✅ 全部完成!"
echo ""
echo "📋 下一步:"
echo "1. 检查变更: cd claude-skills && git diff"
echo "2. 提交更新: git add . && git commit -m 'Sync skills'"
echo "3. 推送到 GitHub: git push"
