#!/bin/bash
# Claude 调用包装脚本 - 处理返回结果和通知

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SAVE_SCRIPT="$SCRIPT_DIR/auto-save.sh"

# 执行保存
# Token 从环境变量或 Claude memory 获取
export GITHUB_TOKEN="${GITHUB_TOKEN}"
RESULT=$(bash "$SAVE_SCRIPT" "$@" 2>&1)

# 解析结果
if echo "$RESULT" | grep -q '"success": false'; then
    # 失败情况
    echo "$RESULT"
    
    # 提取失败信息
    FAILED_COUNT=$(echo "$RESULT" | grep -o '"failed_count": [0-9]*' | grep -o '[0-9]*')
    WARNING=$(echo "$RESULT" | grep -A 50 '"warning":')
    
    # 输出给 Claude 的通知
    echo ""
    echo "================================"
    echo "🚨 需要通知用户!"
    echo "================================"
    if [ "$FAILED_COUNT" -eq 1 ]; then
        echo "📢 消息: GitHub 推送失败,已本地缓存。下次连接成功时自动推送。"
    elif [ "$FAILED_COUNT" -gt 1 ]; then
        echo "📢 消息: ⚠️ 连续失败!已有 $FAILED_COUNT 条记录未推送到 GitHub。"
        echo "请检查网络连接或 GitHub Token!"
    fi
    echo "================================"
    
elif echo "$RESULT" | grep -q '"cached_pushed"'; then
    # 成功且推送了缓存
    echo "$RESULT"
    
    CACHED=$(echo "$RESULT" | grep -o '"cached_pushed": [0-9]*' | grep -o '[0-9]*')
    if [ "$CACHED" -gt 0 ]; then
        echo ""
        echo "================================"
        echo "✅ 好消息!"
        echo "================================"
        echo "📢 消息: 之前失败的 $CACHED 条记录已全部推送到 GitHub!"
        echo "================================"
    fi
else
    # 正常成功
    echo "$RESULT"
fi
