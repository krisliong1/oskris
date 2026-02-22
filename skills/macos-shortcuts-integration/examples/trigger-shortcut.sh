#!/bin/bash
# trigger-shortcut.sh - Shortcuts调用示例脚本
# 用法: ./trigger-shortcut.sh "快捷指令名称" [输入文件] [输出文件]

set -e  # 遇到错误立即退出

SHORTCUT_NAME="$1"
INPUT_PATH="${2:-}"
OUTPUT_PATH="${3:-}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查参数
if [ -z "$SHORTCUT_NAME" ]; then
    echo -e "${RED}错误: 请提供Shortcut名称${NC}"
    echo "用法: $0 <快捷指令名称> [输入文件] [输出文件]"
    exit 1
fi

# 检查Shortcut是否存在
echo -e "${YELLOW}检查Shortcut: $SHORTCUT_NAME${NC}"
if ! shortcuts list | grep -q "$SHORTCUT_NAME"; then
    echo -e "${RED}错误: Shortcut '$SHORTCUT_NAME' 不存在${NC}"
    echo "可用的Shortcuts:"
    shortcuts list
    exit 1
fi

# 构建命令
CMD="shortcuts run \"$SHORTCUT_NAME\""

if [ -n "$INPUT_PATH" ]; then
    # 检查输入文件
    if [ ! -e "$INPUT_PATH" ]; then
        echo -e "${RED}错误: 输入文件不存在: $INPUT_PATH${NC}"
        exit 1
    fi
    CMD="$CMD --input-path \"$INPUT_PATH\""
fi

if [ -n "$OUTPUT_PATH" ]; then
    # 确保输出目录存在
    OUTPUT_DIR=$(dirname "$OUTPUT_PATH")
    mkdir -p "$OUTPUT_DIR"
    CMD="$CMD --output-path \"$OUTPUT_PATH\""
fi

# 执行
echo -e "${YELLOW}执行命令: $CMD${NC}"
eval "$CMD"

# 检查结果
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 成功执行！${NC}"
    
    if [ -n "$OUTPUT_PATH" ] && [ -e "$OUTPUT_PATH" ]; then
        echo -e "${GREEN}输出文件: $OUTPUT_PATH${NC}"
        ls -lh "$OUTPUT_PATH"
    fi
else
    echo -e "${RED}❌ 执行失败${NC}"
    exit 1
fi
