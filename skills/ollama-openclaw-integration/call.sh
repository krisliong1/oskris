#!/bin/bash
# Ollama调用脚本 - OpenClaw集成
# 用途：让OpenClaw通过exec直接调用本地Ollama模型

set -e

# 参数
MODEL="${1:-qwen2.5:14b}"  # 默认使用14B中文模型
PROMPT="$2"
TIMEOUT="${3:-30}"  # 默认30秒超时

# 检查Ollama是否运行
if ! pgrep -x "ollama" > /dev/null; then
  echo "⚠️  Ollama服务未运行，正在启动..."
  ollama serve > /dev/null 2>&1 &
  sleep 2
fi

# 检查模型是否存在
if ! ollama list | grep -q "$MODEL"; then
  echo "❌ 模型 $MODEL 未安装"
  echo "请先运行: ollama pull $MODEL"
  exit 1
fi

# 调用Ollama
echo "🤖 使用模型: $MODEL"
echo "📝 提示词: $PROMPT"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 执行并返回结果
timeout "$TIMEOUT" ollama run "$MODEL" "$PROMPT"

exit_code=$?

if [ $exit_code -eq 124 ]; then
  echo ""
  echo "⚠️  超时（${TIMEOUT}秒）"
  exit 124
elif [ $exit_code -ne 0 ]; then
  echo ""
  echo "❌ 执行失败，退出码: $exit_code"
  exit $exit_code
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 完成 (本地执行，免费，0 tokens)"
