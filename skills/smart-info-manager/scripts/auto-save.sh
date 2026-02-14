#!/bin/bash
# Smart Info Manager - 自动保存脚本
# 由 Claude 直接调用

set -e

# 参数
TEXT="$1"
CATEGORY="${2:-general}"
PRIORITY="${3:-normal}"
TECH_KEYWORDS="$4"

# 配置
REPO_URL="https://github.com/krisliong1/oskris.git"
REPO_PATH="/tmp/oskris"
CACHE_DIR="/tmp/oskris-cache"
FAIL_LOG="$CACHE_DIR/failed.log"
TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
DATE=$(date '+%Y-%m-%d')
DATETIME=$(date '+%Y-%m-%dT%H:%M:%S')

# 创建缓存目录
mkdir -p "$CACHE_DIR"

# 敏感信息检测
SENSITIVE_PATTERNS=(
    "password"
    "passwd"
    "api_key"
    "apikey"
    "secret"
    "private_key"
    "privatekey"
    "ssh-rsa"
    "BEGIN.*PRIVATE KEY"
    "sha256"
    "sk-"
)

echo "🔍 检查敏感信息..."
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    if echo "$TEXT" | grep -iq "$pattern"; then
        # 排除用户自己的 token
        if ! echo "$TEXT" | grep -q "ghp_"; then
            echo "⚠️  警告: 检测到敏感信息 ($pattern)"
            echo "❌ 拒绝保存 - 敏感信息不应存储到 GitHub"
            echo ""
            echo "建议:"
            echo "  - 使用环境变量: export VARIABLE='value'"
            echo "  - 使用密钥管理工具"
            echo "  - 存储到本地加密文件"
            exit 1
        fi
    fi
done
echo "✓ 未检测到敏感信息"

# 检查上次是否有失败记录
if [ -f "$FAIL_LOG" ]; then
    FAIL_COUNT=$(wc -l < "$FAIL_LOG")
    if [ "$FAIL_COUNT" -gt 0 ]; then
        echo "⚠️  检测到 $FAIL_COUNT 条未推送的记录"
    fi
fi
REPO_URL="https://github.com/krisliong1/oskris.git"
REPO_PATH="/tmp/oskris"
TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
DATE=$(date '+%Y-%m-%d')
DATETIME=$(date '+%Y-%m-%dT%H:%M:%S')

# 初始化仓库
echo "📦 初始化仓库..."
if [ -d "$REPO_PATH" ]; then
    cd "$REPO_PATH" && git pull origin main
else
    git clone "$REPO_URL" "$REPO_PATH"
fi

cd "$REPO_PATH"

# 创建目录结构
mkdir -p memories/{personal,preferences,conversations}
mkdir -p tasks/{urgent,important,normal}
mkdir -p notes/{tech,work,learning}
mkdir -p projects
mkdir -p archive/$(date '+%Y/%m/%d')
mkdir -p index

# 确定文件路径
case "$PRIORITY" in
    urgent)
        FILEPATH="tasks/urgent/${TIMESTAMP}-task.md"
        ;;
    important)
        FILEPATH="tasks/important/${TIMESTAMP}-task.md"
        ;;
    *)
        case "$CATEGORY" in
            learning)
                FILEPATH="notes/learning/${DATE}-note.md"
                ;;
            work)
                FILEPATH="notes/work/${DATE}-note.md"
                ;;
            tech)
                FILEPATH="notes/tech/${DATE}-tech.md"
                ;;
            preferences)
                FILEPATH="memories/preferences/${DATE}.md"
                ;;
            *)
                FILEPATH="archive/$(date '+%Y/%m/%d')/${TIMESTAMP}.md"
                ;;
        esac
        ;;
esac

echo "📝 创建文件: $FILEPATH"

# 生成 Markdown 内容
cat > "$FILEPATH" << EOF
---
date: $DATETIME
category: $CATEGORY
priority: $PRIORITY
tech_keywords: [$TECH_KEYWORDS]
---

# ${CATEGORY^} - $DATE

## 内容

$TEXT

## 元数据

- 保存时间: $DATETIME
- 分类: $CATEGORY
- 优先级: $PRIORITY
- 技术关键词: $TECH_KEYWORDS

---

*由 Smart Info Manager 自动生成*
EOF

echo "✓ 文件已创建"

# 更新索引 (简化版)
INDEX_FILE="index/timeline.json"
if [ ! -f "$INDEX_FILE" ]; then
    echo "{}" > "$INDEX_FILE"
fi

# 使用 jq 更新 JSON (如果有的话)
if command -v jq &> /dev/null; then
    jq --arg date "$DATE" --arg file "$FILEPATH" \
       '.[$date].files += [$file]' \
       "$INDEX_FILE" > "${INDEX_FILE}.tmp" && \
       mv "${INDEX_FILE}.tmp" "$INDEX_FILE"
fi

# 提交到 GitHub (带重试机制)
echo "🚀 提交到 GitHub..."
git add .
git commit -m "Auto-save: $CATEGORY - $TIMESTAMP" || echo "No changes to commit"

# 检查是否需要配置 Git
if ! git config user.email > /dev/null 2>&1; then
    git config user.email "claude@smartinfomanager.ai"
    git config user.name "Smart Info Manager"
fi

# 推送函数(带重试)
push_to_github() {
    local max_retries=3
    local retry_count=0
    local success=false
    
    while [ $retry_count -lt $max_retries ]; do
        echo "📤 推送尝试 $((retry_count + 1))/$max_retries..."
        
        if [ -n "$GITHUB_TOKEN" ]; then
            if git push https://${GITHUB_TOKEN}@github.com/krisliong1/oskris.git main 2>&1; then
                success=true
                break
            else
                retry_count=$((retry_count + 1))
                if [ $retry_count -lt $max_retries ]; then
                    echo "⚠️  推送失败,等待 2 秒后重试..."
                    sleep 2
                fi
            fi
        else
            echo "❌ 未设置 GITHUB_TOKEN"
            break
        fi
    done
    
    if [ "$success" = true ]; then
        # 推送成功
        GITHUB_URL="https://github.com/krisliong1/oskris/blob/main/$FILEPATH"
        echo "✅ 推送成功!"
        echo "📍 GitHub 链接: $GITHUB_URL"
        
        # 检查是否有缓存的失败记录,如果有则批量推送
        if [ -f "$FAIL_LOG" ] && [ -s "$FAIL_LOG" ]; then
            echo ""
            echo "🔄 检测到之前失败的记录,正在批量推送..."
            
            # 读取失败记录数量
            CACHED_COUNT=$(wc -l < "$FAIL_LOG")
            echo "📦 发现 $CACHED_COUNT 条缓存记录"
            
            # 尝试推送缓存的内容
            if git push https://${GITHUB_TOKEN}@github.com/krisliong1/oskris.git main 2>&1; then
                echo "✅ 批量推送成功!已推送 $CACHED_COUNT 条缓存记录"
                # 清空失败日志
                > "$FAIL_LOG"
            else
                echo "⚠️  批量推送失败,缓存保留"
            fi
        fi
        
        # 返回成功结果
        cat << RESULT
{
    "success": true,
    "filepath": "$FILEPATH",
    "local_path": "$REPO_PATH/$FILEPATH",
    "github_url": "$GITHUB_URL",
    "timestamp": "$DATETIME",
    "cached_pushed": ${CACHED_COUNT:-0}
}
RESULT
    else
        # 推送失败,记录到缓存
        echo "❌ 推送失败(重试 $max_retries 次后仍失败)"
        echo "💾 本地已保存: $REPO_PATH/$FILEPATH"
        echo "📝 记录到失败日志,将在下次成功时批量推送"
        
        # 记录失败信息
        echo "$DATETIME|$FILEPATH|$CATEGORY|$PRIORITY" >> "$FAIL_LOG"
        
        # 检查连续失败次数
        CURRENT_FAIL_COUNT=$(wc -l < "$FAIL_LOG")
        
        # 生成警告消息
        WARNING_MSG="⚠️ GitHub 连接失败通知
        
📊 失败统计:
- 本次失败: $FILEPATH
- 累计未推送: $CURRENT_FAIL_COUNT 条记录
- 本地路径: $REPO_PATH/$FILEPATH

💡 可能原因:
1. 网络连接问题
2. GitHub Token 过期或权限不足
3. GitHub 服务暂时不可用

🔧 建议操作:
1. 检查网络连接
2. 验证 GitHub Token: echo \$GITHUB_TOKEN
3. 手动推送: cd $REPO_PATH && git push

📦 所有内容已本地保存,下次连接成功时自动批量推送"

        # 返回失败结果(带警告)
        cat << RESULT
{
    "success": false,
    "filepath": "$FILEPATH",
    "local_path": "$REPO_PATH/$FILEPATH",
    "timestamp": "$DATETIME",
    "failed_count": $CURRENT_FAIL_COUNT,
    "warning": $(echo "$WARNING_MSG" | jq -Rs .),
    "retry_attempted": $max_retries
}
RESULT
    fi
}

# 执行推送
push_to_github
