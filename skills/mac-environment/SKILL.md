---
name: mac-environment
description: >-
  Mac Mini M4环境管理和文件操作。当Claude需要访问用户Mac文件、检查已安装应用、
  管理iCloud文件、操作本地Git仓库时触发。触发词: "Mac文件"、"本地文件"、
  "iCloud"、"桌面文件"、"检查Mac"、"Mac应用"、"本地操作"。
  包含完整的应用清单、路径映射和安全规则。
---

# Mac Environment — 环境管理Skill

## 核心路径

### 文件系统访问范围
- MCP scope: `/Users/oskris` (全用户目录)
- 配置: `~/Library/Application Support/Claude/claude_desktop_config.json`

### 常用路径速查
| 用途 | 路径 |
|------|------|
| 桌面 | ~/Desktop |
| 文档 | ~/Documents |
| 下载 | ~/Downloads |
| iCloud主目录 | ~/Library/Mobile Documents/com~apple~CloudDocs/ |
| iCloud/kris | .../kris/ |
| Claude备份 | .../kris/claudecode-backup/ |
| Git活跃仓库 | ~/oskris |
| Git副本 | ~/oskris-github |
| Skills开发 | ~/Projects/skills |
| SSH密钥 | ~/.ssh/ |
| Node.js | ~/.nvm/versions/node/v20.20.0 |
| Claude Code | ~/.local/bin/claude |
| Homebrew | /opt/homebrew |

### 代理配置
- Stash(Vortex): ~/.config/com.vortex.helper/config.yaml
- GeoIP数据: ~/.config/com.vortex.helper/*.mmdb

## 安全规则（绝对遵守）

1. **永不删除文件** — 除非列出文件清单并获得用户明确确认
2. **修改前备份** — 改任何文件前先备份到 claudecode-backup/
3. **不碰敏感目录** — ~/Desktop/账号重要/, ~/Library/Keychains/ 等
4. **不改系统文件** — /Library/, /System/ 等
5. **iCloud文件注意同步** — 写入后可能需要等iCloud同步

## 环境检测流程

检测到 `filesystem:` MCP工具时:
1. 确认scope = /Users/oskris
2. 可读写: Desktop, Documents, Downloads, Library, iCloud
3. 自动开启Mac本地同步模式
4. 文件同时写入Mac + 上传GitHub

## 已安装应用清单

### 浏览器(10个)
Arc, Brave, Chrome, Chromium, Edge, Firefox, Opera, Safari, Vivaldi, Tor

### 网络代理(5个)
Stash(主力), Shadowrocket, QuickFox(回国), FOB WiFi, Surge

### 通讯(4个)
WhatsApp, WeChat, Telegram, FaceTime

### AI(3个)
Claude Desktop+Code+Chrome, Doubao(豆包)

### 开发(7个)
Xcode, Source, CodeReplay, Bazinga, Alignment, Swifter, GitLab MR

### 办公(4个)
Pages, Numbers, Templates for Office, Set for Business

### 工具(8个)
Phone Mechanic, TunesMedic, MKPlayer, AliPrice Shopee Tracker, YA Ad Blocker, 爱思助手, Avast, Brother iPrint

## 典型操作

### 读取iCloud文件
```
路径: ~/Library/Mobile Documents/com~apple~CloudDocs/kris/[文件名]
```

### 备份到iCloud
```
目标: ~/Library/Mobile Documents/com~apple~CloudDocs/kris/claudecode-backup/
```

### 检查应用配置
```
路径: ~/Library/Application Support/[AppName]/
或: ~/Library/Containers/[BundleID]/Data/Library/Application Support/
```
