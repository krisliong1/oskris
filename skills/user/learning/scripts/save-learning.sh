#!/bin/bash
# save-learning.sh — 学习完成后自动存储到GitHub
# 用法: bash save-learning.sh [文件路径] [commit消息]

FILE_PATH=$1
COMMIT_MSG=$2
REPO_DIR="/tmp/oskris"
GITHUB_USER="${GITHUB_USER:-krisliong1}"
GITHUB_TOKEN="${GITHUB_TOKEN}"

if [ -z "$FILE_PATH" ] || [ -z "$COMMIT_MSG" ]; then
    echo "用法: bash save-learning.sh [文件路径] [commit消息]"
    exit 1
fi

if [ ! -d "$REPO_DIR/.git" ]; then
    cd /tmp
    git clone https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_USER}/oskris.git
fi

cd $REPO_DIR
git config user.email "oskrismy@gmail.com"
git config user.name "krisliong1"
git pull origin main

git add "$FILE_PATH"
git commit -m "$COMMIT_MSG"
git push origin main

echo "✅ 已推送到 GitHub: $FILE_PATH"
