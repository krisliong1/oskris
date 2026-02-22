---
name: multi-platform-deployment
description: Oskris多平台AI部署策略。Claude.ai/Desktop/Code/OpenClaw环境配置和能力管理。基于实际生产环境经验。
---

# Multi-Platform Deployment Skill

## 平台矩阵

### 平台对比
| 平台 | 工作路径 | 能力 | 最佳用途 |
|------|---------|------|---------|
| **Claude.ai** | 临时/虚拟 | 基础脚本、web搜索 | 移动端、快速咨询 |
| **Claude Desktop** | /Users/oskris/ | MCP工具集 | 本地开发、文件管理 |
| **Claude Code** | 项目目录 | 完整终端 | 代码开发、Git操作 |
| **OpenClaw** | openclaw workspace | 多工具协调 | 生产自动化、跨平台 |

### 环境检测策略
```python
def detect_platform():
    if has_mcp_tools():
        return "claude-desktop"
    elif has_terminal_access():
        return "claude-code"  
    elif has_openclaw_tools():
        return "openclaw"
    else:
        return "claude-ai"
```

## 部署规则

### 文件安全策略
```python
# 新文件 → 直接推送
# 已存在文件 → 显示diff → 确认 → 备份 → 推送 → 记录
# 删除操作 → 必须明确确认
```

### GitHub工作流
```bash
# 通用凭据
repo: krisliong1/oskris  
token: [GITHUB_TOKEN]
branch: main

# 操作流程
1. 本地更改
2. 显示diff (如有)  
3. 用户确认
4. 推送GitHub
5. 通知用户
```

### 敏感数据管理
```
✅ GitHub: 代码、配置模板、说明文档
❌ GitHub: 密钥、密码、token
✅ VPS: 敏感凭据、生产数据
✅ 本地: 开发环境、临时文件
```

## 工具适配

### MCP工具检测
```python
if filesystem_available():
    use_direct_file_operations()
if github_mcp_available():
    use_integrated_git_push()  
if hostinger_api_available():
    use_dns_management()
```

### 降级策略
```python
# MCP不可用时
provide_manual_instructions()
create_downloadable_files()
suggest_alternative_methods()
```

## 质量保证

### 平台一致性
- 相同项目在不同平台产出一致
- 文件路径自动适配
- 权限问题优雅处理

### 错误恢复
- GitHub推送失败 → 本地保存 + 用户指导
- MCP工具故障 → 降级到手动操作
- 网络异常 → 离线模式工作

---
*基于Oskris多平台实际部署经验*