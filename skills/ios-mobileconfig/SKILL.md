---
name: ios-mobileconfig
description: 制作iOS配置描述文件(.mobileconfig),包括DNS设置、广告屏蔽、企业证书屏蔽等。当用户需要制作iOS描述文件、DNS配置、广告屏蔽配置时触发此skill。
---

# iOS Mobileconfig 配置文件制作

## Overview

制作 `.mobileconfig` 描述文件用于 iOS/iPadOS/macOS 设备的系统级配置。主要用途：DNS广告屏蔽、企业证书验证屏蔽、加密DNS配置。

## Quick Start

### 基本结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PayloadContent</key>
    <array>
        <!-- DNS Payload 放这里，可放多个 -->
    </array>
    <key>PayloadDisplayName</key>
    <string>配置文件名称</string>
    <key>PayloadIdentifier</key>
    <string>com.example.config</string>
    <key>PayloadType</key>
    <string>Configuration</string>
    <key>PayloadUUID</key>
    <string>唯一UUID</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
</dict>
</plist>
```

### DNS Payload 模板

```xml
<dict>
    <key>DNSSettings</key>
    <dict>
        <key>DNSProtocol</key>
        <string>HTTPS</string>
        <key>ServerAddresses</key>
        <array>
            <string>94.140.14.14</string>
        </array>
        <key>ServerURL</key>
        <string>https://dns.adguard-dns.com/dns-query</string>
    </dict>
    <key>OnDemandRules</key>
    <array>
        <dict>
            <key>Action</key>
            <string>Connect</string>
        </dict>
    </array>
    <key>PayloadDisplayName</key>
    <string>显示名称</string>
    <key>PayloadIdentifier</key>
    <string>com.example.dns1</string>
    <key>PayloadType</key>
    <string>com.apple.dnsSettings.managed</string>
    <key>PayloadUUID</key>
    <string>唯一UUID</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
</dict>
```

## Workflow

### 多选功能（关键技巧）

Apple 文档明确说明 `com.apple.dnsSettings.managed` 的 **Duplicates allowed: True**。

在一个 `.mobileconfig` 的 `PayloadContent` 数组里放多个 DNS payload，每个用不同的 `PayloadUUID` 和 `PayloadIdentifier`，安装后在 **设置 → 通用 → DNS** 页面会显示多个选项，全部可以打勾。

这就是小白签(xb51.cn)实现多个"屏蔽企业证书验证"同时勾选的原理。

### 常用 DNS 服务器

| 服务 | DoH地址 | IP | 功能 |
|------|---------|-----|------|
| AdGuard DNS | `https://dns.adguard-dns.com/dns-query` | 94.140.14.14, 94.140.15.15 | 屏蔽广告+追踪 |
| AdGuard Family | `https://family.adguard-dns.com/dns-query` | 94.140.14.15, 94.140.15.16 | 广告+成人内容 |
| Cloudflare Security | `https://security.cloudflare-dns.com/dns-query` | 1.1.1.2, 1.0.0.2 | 屏蔽恶意软件 |
| Quad9 | `https://dns.quad9.net/dns-query` | 9.9.9.9, 149.112.112.112 | 屏蔽恶意域名 |
| 阿里DNS | `https://dns.alidns.com/dns-query` | 223.5.5.5, 223.6.6.6 | 中国加速 |
| DNSPod | `https://doh.pub/dns-query` | 119.29.29.29 | 中国加速 |

### 验证文件格式

```python
python3 -c "import plistlib; plistlib.load(open('file.mobileconfig','rb')); print('格式正确')"
```

### 安装方式

1. 用 iPhone **Safari** 打开文件（其他浏览器不行）
2. 允许下载 → 设置 → 通用 → VPN、DNS与设备管理 → 安装
3. DNS设置在 设置 → 通用 → VPN、DNS与设备管理 → DNS

## Guidelines

- 每个 payload 必须有唯一的 `PayloadUUID` 和 `PayloadIdentifier`
- iOS 限制：描述文件只能指定DNS服务器，不能像hosts文件直接屏蔽单个域名
- 要屏蔽特定域名，需要用带广告过滤的DNS（AdGuard DNS）或自建AdGuard Home
- `PayloadRemovalDisallowed` 设为 `false` 允许用户删除
- `ConsentText` 可添加中英文安装说明
- DNSProtocol 支持: HTTPS (DoH) 和 TLS (DoT)
- 企业证书屏蔽原理：DNS屏蔽 ppq.apple.com, ocsp.apple.com, crl.apple.com 等域名
