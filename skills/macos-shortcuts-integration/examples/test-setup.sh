#!/bin/bash
# test-setup.sh - 测试macOS自动化环境是否正确配置
# 用法: ./test-setup.sh

echo "🔍 macOS自动化环境检查"
echo "================================"
echo ""

# 颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

success_count=0
total_tests=0

# 测试函数
test_command() {
    local name="$1"
    local command="$2"
    total_tests=$((total_tests + 1))
    
    echo -n "检查 $name ... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ 可用${NC}"
        success_count=$((success_count + 1))
        return 0
    else
        echo -e "${RED}❌ 不可用${NC}"
        return 1
    fi
}

# 1. shortcuts CLI
echo "📱 Shortcuts"
test_command "shortcuts命令" "which shortcuts"
test_command "shortcuts list" "shortcuts list"

echo ""

# 2. AppleScript
echo "📜 AppleScript"
test_command "osascript命令" "which osascript"
test_command "AppleScript执行" "osascript -e 'return 1+1'"

echo ""

# 3. Automator
echo "⚙️  Automator"
test_command "Automator.app" "test -d /System/Applications/Automator.app"

echo ""

# 4. 系统工具
echo "🛠️  系统工具"
test_command "sips (图片处理)" "which sips"
test_command "say (文本转语音)" "which say"
test_command "textutil (文档转换)" "which textutil"
test_command "open命令" "which open"

echo ""

# 5. Node.js (可选)
echo "🟢 Node.js (示例脚本需要)"
test_command "node命令" "which node"
if which node > /dev/null 2>&1; then
    node_version=$(node --version)
    echo "   版本: $node_version"
fi

echo ""

# 6. 检查Shortcuts
echo "📋 已安装的Shortcuts"
shortcuts_count=$(shortcuts list 2>/dev/null | wc -l)
echo "   共 $shortcuts_count 个快捷指令"

if [ "$shortcuts_count" -gt 0 ]; then
    echo "   列表:"
    shortcuts list 2>/dev/null | head -5 | while read line; do
        echo "     - $line"
    done
    if [ "$shortcuts_count" -gt 5 ]; then
        echo "     ... 还有 $((shortcuts_count - 5)) 个"
    fi
fi

echo ""

# 7. 检查示例文件
echo "📂 示例文件"
test_command "trigger-shortcut.sh" "test -f trigger-shortcut.sh"
test_command "batch-process.applescript" "test -f batch-process.applescript"
test_command "ai-to-shortcut.js" "test -f ai-to-shortcut.js"

echo ""

# 总结
echo "================================"
echo "测试完成: $success_count / $total_tests 通过"

if [ "$success_count" -eq "$total_tests" ]; then
    echo -e "${GREEN}🎉 完美！所有功能都可用${NC}"
    exit 0
elif [ "$success_count" -gt $((total_tests * 2 / 3)) ]; then
    echo -e "${YELLOW}⚠️  大部分功能可用，但有些缺失${NC}"
    exit 0
else
    echo -e "${RED}❌ 许多功能不可用，请检查环境${NC}"
    exit 1
fi
