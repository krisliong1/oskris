---
name: ios-mobileconfig
description: 制作iOS/iPadOS/macOS配置描述文件(.mobileconfig)。支持DNS设置、VPN配置、Wi-Fi、证书、企业证书屏蔽等所有payload类型。当用户需要制作任何iOS描述文件时触发。
---

# iOS Mobileconfig 配置描述文件制作

## Overview

制作 `.mobileconfig` 配置描述文件，用于 iOS/iPadOS/macOS 设备系统级配置。一个文件可包含多个 payload，实现DNS、VPN、Wi-Fi、证书等多种功能组合。

## Quick Start

### 外层结构（所有描述文件通用）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PayloadContent</key>
    <array>
        <!-- 这里放一个或多个 payload -->
    </array>
    <key>PayloadDisplayName</key>
    <string>描述文件名称（用户看到的）</string>
    <key>PayloadIdentifier</key>
    <string>com.oskris.配置名</string>
    <key>PayloadOrganization</key>
    <string>Oskris</string>
    <key>PayloadRemovalDisallowed</key>
    <false/>
    <key>PayloadType</key>
    <string>Configuration</string>
    <key>PayloadUUID</key>
    <string>唯一UUID-外层</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
    <key>ConsentText</key>
    <dict>
        <key>default</key>
        <string>安装说明文字</string>
    </dict>
</dict>
</plist>
```

## Workflow

### Payload类型速查

| PayloadType | 用途 | 多个允许 |
|-------------|------|----------|
| `com.apple.dnsSettings.managed` | DNS设置(DoH/DoT) | ✅ True |
| `com.apple.vpn.managed` | VPN配置 | ✅ True |
| `com.apple.wifi.managed` | Wi-Fi网络 | ✅ True |
| `com.apple.security.root` | 根证书 | ✅ True |
| `com.apple.security.pkcs1` | 证书 | ✅ True |
| `com.apple.webClip.managed` | 桌面快捷方式 | ✅ True |
| `com.apple.mail.managed` | 邮件账户 | ✅ True |
| `com.apple.domains` | 域名管理 | ❌ False |

### DNS Payload 模板

```xml
<dict>
    <key>DNSSettings</key>
    <dict>
        <key>DNSProtocol</key>
        <string>HTTPS</string>
        <key>ServerAddresses</key>
        <array>
            <string>IP地址</string>
        </array>
        <key>ServerURL</key>
        <string>https://DoH地址/dns-query</string>
    </dict>
    <key>OnDemandRules</key>
    <array>
        <dict>
            <key>Action</key>
            <string>Connect</string>
        </dict>
    </array>
    <key>PayloadDisplayName</key>
    <string>DNS名称</string>
    <key>PayloadIdentifier</key>
    <string>com.oskris.xxx.dns1</string>
    <key>PayloadType</key>
    <string>com.apple.dnsSettings.managed</string>
    <key>PayloadUUID</key>
    <string>唯一UUID</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
</dict>
```

### 多选功能（关键技巧）

`Duplicates allowed: True` 的 payload 类型，在 `PayloadContent` 数组里放多个同类型 payload（每个不同UUID），安装后全部独立显示，可同时勾选。小白签(xb51.cn)就是用这个原理实现多个DNS同时勾选。

### 排除特定Wi-Fi网络

在 `OnDemandRules` 中添加排除规则：

```xml
<dict>
    <key>Action</key>
    <string>Disconnect</string>
    <key>SSIDMatch</key>
    <array>
        <string>家里Wi-Fi名称</string>
    </array>
</dict>
```

### 验证格式

```python
python3 -c "import plistlib; plistlib.load(open('file.mobileconfig','rb')); print('✅ 格式正确')"
```

### 安装方式

1. iPhone **Safari** 打开文件（其他浏览器不弹安装提示）
2. 允许下载 → 设置 → 通用 → VPN、DNS与设备管理 → 安装
3. 网页托管时 Content-Type 设为 `application/x-apple-aspen-config`

## Guidelines

- 每个 payload 必须有唯一 `PayloadUUID` + `PayloadIdentifier`
- DNSProtocol 支持 `HTTPS`(DoH) 和 `TLS`(DoT)
- `PayloadRemovalDisallowed` 设 `false` 允许用户卸载
- 文件可通过 Safari URL 直接安装，或 AirDrop 传输
- 已有项目参考: `projects/beautycam-adblock/configs/` 里的多选DNS示例
