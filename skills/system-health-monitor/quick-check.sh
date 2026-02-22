#!/bin/bash
# System Health Monitor - 快速系统检查
# 用途: 一条命令了解系统所有关键状态

set -e

# 颜色定义
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 参数解析
JSON_OUTPUT=false
SILENT=false
CHECK_ALL=true

for arg in "$@"; do
  case $arg in
    --json) JSON_OUTPUT=true ;;
    --silent) SILENT=true ;;
    --processes) CHECK_ALL=false; CHECK_PROCESSES=true ;;
    --disk) CHECK_ALL=false; CHECK_DISK=true ;;
    --memory) CHECK_ALL=false; CHECK_MEMORY=true ;;
    --network) CHECK_ALL=false; CHECK_NETWORK=true ;;
  esac
done

# 收集数据
collect_data() {
  # 系统基础
  UPTIME=$(uptime | awk '{print $3,$4}' | sed 's/,//')
  LOAD=$(uptime | awk -F'load average:' '{print $2}' | xargs)
  
  # 磁盘
  DISK_ROOT=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
  DISK_USERS=$(df -h /Users 2>/dev/null | tail -1 | awk '{print $5}' | sed 's/%//' || echo "0")
  
  # 内存
  MEM_TOTAL=$(sysctl hw.memsize | awk '{print int($2/1024/1024/1024)"GB"}')
  MEM_USED=$(vm_stat | grep "Pages active" | awk '{print int($3*4096/1024/1024/1024)"GB"}')
  
  # 进程
  OLLAMA_PID=$(pgrep -x ollama || echo "")
  RSYNC_PID=$(pgrep rsync || echo "")
  OPENCLAW_PID=$(pgrep -f "openclaw" | head -1 || echo "")
  
  # 网络
  VPS_REACHABLE=$(ping -c 1 -W 1 76.13.191.45 > /dev/null 2>&1 && echo "yes" || echo "no")
  
  # iPhone
  IPHONE_CONNECTED=$(system_profiler SPUSBDataType 2>/dev/null | grep -q "iPhone" && echo "yes" || echo "no")
}

# JSON输出
json_output() {
  cat << EOF
{
  "timestamp": "$(date +%Y-%m-%d\ %H:%M:%S)",
  "uptime": "$UPTIME",
  "load": "$LOAD",
  "disk": {
    "root_usage": $DISK_ROOT,
    "users_usage": $DISK_USERS
  },
  "memory": {
    "total": "$MEM_TOTAL",
    "used": "$MEM_USED"
  },
  "processes": {
    "ollama": "${OLLAMA_PID:-null}",
    "rsync": "${RSYNC_PID:-null}",
    "openclaw": "${OPENCLAW_PID:-null}"
  },
  "network": {
    "vps_reachable": "$VPS_REACHABLE"
  },
  "iphone_connected": "$IPHONE_CONNECTED"
}
EOF
}

# 人类可读输出
human_output() {
  echo ""
  echo "╔══════════════════════════════════════════════╗"
  echo "║     Mac Mini M4 系统健康状态                 ║"
  echo "╚══════════════════════════════════════════════╝"
  echo ""
  
  echo -e "📅 时间: $(date +'%Y-%m-%d %H:%M:%S')"
  echo -e "⏰ 运行时间: $UPTIME"
  echo -e "📊 负载: $LOAD"
  echo ""
  
  # 磁盘
  echo "💾 磁盘使用:"
  if [ "$DISK_ROOT" -lt 80 ]; then
    echo -e "  /          : ${DISK_ROOT}% ${GREEN}✅${NC}"
  elif [ "$DISK_ROOT" -lt 95 ]; then
    echo -e "  /          : ${DISK_ROOT}% ${YELLOW}⚠️${NC}"
  else
    echo -e "  /          : ${DISK_ROOT}% ${RED}🔴${NC}"
  fi
  
  if [ "$DISK_USERS" -lt 80 ]; then
    echo -e "  /Users     : ${DISK_USERS}% ${GREEN}✅${NC}"
  elif [ "$DISK_USERS" -lt 95 ]; then
    echo -e "  /Users     : ${DISK_USERS}% ${YELLOW}⚠️ 接近满${NC}"
  else
    echo -e "  /Users     : ${DISK_USERS}% ${RED}🔴 需要清理${NC}"
  fi
  echo ""
  
  # 内存
  echo "🧠 内存:"
  echo -e "  总计: $MEM_TOTAL"
  echo -e "  已用: $MEM_USED ${GREEN}✅${NC}"
  echo ""
  
  # 进程
  echo "🔄 关键进程:"
  if [ -n "$OLLAMA_PID" ]; then
    echo -e "  ${GREEN}✅${NC} Ollama     : 运行中 (PID $OLLAMA_PID)"
  else
    echo -e "  ${YELLOW}⏸${NC}  Ollama     : 未运行"
  fi
  
  if [ -n "$RSYNC_PID" ]; then
    echo -e "  ${GREEN}✅${NC} rsync      : 运行中 (PID $RSYNC_PID)"
  else
    echo -e "  ${BLUE}ℹ${NC}  rsync      : 未运行（正常）"
  fi
  
  if [ -n "$OPENCLAW_PID" ]; then
    echo -e "  ${GREEN}✅${NC} OpenClaw   : 运行中 (PID $OPENCLAW_PID)"
  else
    echo -e "  ${RED}❌${NC} OpenClaw   : 未运行"
  fi
  echo ""
  
  # 网络
  echo "🌐 网络:"
  if [ "$VPS_REACHABLE" = "yes" ]; then
    echo -e "  ${GREEN}✅${NC} VPS (76.13.191.45): 可达"
  else
    echo -e "  ${RED}❌${NC} VPS (76.13.191.45): 不可达"
  fi
  echo ""
  
  # iPhone
  if [ "$IPHONE_CONNECTED" = "yes" ]; then
    echo -e "📱 ${GREEN}✅${NC} iPhone: 已连接"
  else
    echo -e "📱 ${BLUE}ℹ${NC}  iPhone: 未连接"
  fi
  echo ""
  
  # 智能建议
  WARNINGS=0
  echo "💡 建议:"
  
  if [ "$DISK_USERS" -gt 90 ]; then
    echo -e "  ${YELLOW}⚠️${NC}  用户磁盘使用${DISK_USERS}%，建议清理"
    WARNINGS=$((WARNINGS + 1))
  fi
  
  if [ -z "$OLLAMA_PID" ]; then
    echo -e "  ${BLUE}ℹ${NC}  Ollama未运行，需要时可启动"
  fi
  
  if [ "$WARNINGS" -eq 0 ]; then
    echo -e "  ${GREEN}✅${NC} 一切正常！"
  fi
  
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  if [ "$WARNINGS" -eq 0 ]; then
    echo -e "${GREEN}✅ 状态: 系统正常${NC}"
  else
    echo -e "${YELLOW}⚠️  状态: 系统正常，${WARNINGS}个警告${NC}"
  fi
  echo ""
}

# 主函数
main() {
  collect_data
  
  if [ "$JSON_OUTPUT" = true ]; then
    json_output
  elif [ "$SILENT" = true ]; then
    # Silent模式只在有问题时输出
    if [ "$DISK_ROOT" -gt 90 ] || [ "$DISK_USERS" -gt 90 ] || [ -z "$OPENCLAW_PID" ]; then
      human_output
    fi
  else
    human_output
  fi
}

main "$@"
