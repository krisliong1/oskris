---
name: dns-adblock
description: DNS广告屏蔽+CDN加速技能。制作多层DNS屏蔽方案(AdGuard+Cloudflare+Quad9)，生成mobileconfig/hosts等格式。当用户要屏蔽广告、制作DNS配置、查找广告域名、优化网络速度时触发。包含YouTube广告屏蔽研究、成人网站兼容性、多DNS方案对比。
---

# DNS 广告屏蔽 + CDN加速

## Overview

制作多层DNS屏蔽+CDN加速方案。配合 `ios-mobileconfig` skill 生成iOS描述文件。

**核心认知**:
- DNS级别屏蔽对大多数App广告有效,但对YouTube视频广告(SSAI)无效
- AdGuard Family / Cloudflare Family 会屏蔽成人网站，导致Grindr/Tinder/Blued等App自动登出
- 用户需要"不屏蔽成人网站"的方案时，使用AdGuard Default + Cloudflare Security + Quad9

## Quick Start

### DNS屏蔽能力边界

| 能屏蔽 | 不能屏蔽 |
|--------|----------|
| 独立广告域名(第三方SDK) | YouTube视频内嵌广告(SSAI) |
| 网页横幅/弹窗广告 | 与内容共享域名的广告 |
| App追踪器和分析 | 加密流内的广告 |
| 恶意软件/钓鱼域名 | 服务器端拼接的广告流 |

### YouTube广告屏蔽层级（2026-02研究）

| 方法 | 屏蔽率 | 说明 |
|------|--------|------|
| DNS级别 | 30-50% | googlevideo.com广告和视频混用，无法区分 |
| 浏览器扩展(uBlock Origin) | 95%+ | 只在Safari/浏览器中生效 |
| AdGuard iOS App内置播放器 | 99% | 通过App内播放YouTube实现 |
| YouTube Premium | 100% | $13.99/月 |

NextDNS官方确认：无法通过DNS完全屏蔽YouTube广告。
最佳方案：mobileconfig(DNS层) + AdGuard iOS App(应用层) = 最大覆盖。

### ⚠️ 成人网站兼容性警告

| DNS | 屏蔽成人网站 | 影响 |
|-----|-------------|------|
| AdGuard **Family** | ✅ 屏蔽 | Grindr/Tinder/Blued会登出 |
| Cloudflare **Family** (1.1.1.3) | ✅ 屏蔽 | 同上 |
| AdGuard **Default** | ❌ 不屏蔽 | 安全 ✅ |
| Cloudflare **Security** (1.1.1.2) | ❌ 不屏蔽 | 安全 ✅ |
| Quad9 | ❌ 不屏蔽 | 安全 ✅ |

**规则：除非用户明确要求屏蔽成人内容，否则永远用Default/Security版本。**

### 推荐方案（当前最新v2）

**方案1：🛡️全屏蔽+⚡️全加速**（5个DNS选项）
- AdGuard Default — 广告+追踪屏蔽（不屏蔽成人）
- Cloudflare Security — 恶意网站屏蔽+CDN（不屏蔽成人）
- Quad9 — 威胁+钓鱼屏蔽（不屏蔽成人）
- Cloudflare 1.1.1.1 — 纯速度CDN
- 阿里DNS — 亚洲加速

**方案2：⚡CDN+DNS全加速**（4个DNS选项）
- Cloudflare 1.1.1.1 — 全球最快
- 阿里DNS — 亚洲加速
- Google DNS — 全球基础设施
- 腾讯DNSPod — 中国大陆加速

## Workflow

### DNS服务器完整列表

**屏蔽类（不屏蔽成人）：**
AdGuard Default: DoH `https://dns.adguard-dns.com/dns-query` | 94.140.14.14/94.140.15.15 | IPv6 2a10:50c0::ad1:ff/2a10:50c0::ad2:ff
Cloudflare Security: DoH `https://security.cloudflare-dns.com/dns-query` | 1.1.1.2/1.0.0.2 | IPv6 2606:4700:4700::1112/2606:4700:4700::1002
Quad9: DoH `https://dns.quad9.net/dns-query` | 9.9.9.9/149.112.112.112 | IPv6 2620:fe::fe/2620:fe::9

**屏蔽类（屏蔽成人⚠️）：**
AdGuard Family: DoH `https://family.adguard-dns.com/dns-query` | 94.140.14.15/94.140.15.16 | IPv6 2a10:50c0::bad1:ff/2a10:50c0::bad2:ff
Cloudflare Family: DoH `https://family.cloudflare-dns.com/dns-query` | 1.1.1.3/1.0.0.3 | IPv6 2606:4700:4700::1113/2606:4700:4700::1003

**纯加速类：**
Cloudflare: DoH `https://cloudflare-dns.com/dns-query` | 1.1.1.1/1.0.0.1 | IPv6 2606:4700:4700::1111/2606:4700:4700::1001
阿里DNS: DoH `https://dns.alidns.com/dns-query` | 223.5.5.5/223.6.6.6 | IPv6 2400:3200::1/2400:3200:baba::1
Google DNS: DoH `https://dns.google/dns-query` | 8.8.8.8/8.8.4.4 | IPv6 2001:4860:4860::8888/2001:4860:4860::8844
腾讯DNSPod: DoH `https://doh.pub/dns-query` | 119.29.29.29/119.28.28.28

### 当前配置文件位置

最新v2: `projects/dns-profiles/fullblock-fullspeed.mobileconfig` + `projects/dns-profiles/cdn-dns-fullspeed.mobileconfig`
旧版: `projects/beautycam-adblock/configs/` (已废弃)

### 已收集广告域名

美颜相机: ad.meitu.com, ads.meitu.com, track.meitu.com, stat.meitu.com等
穿山甲: ad.toutiao.com, ad.oceanengine.com
广点通: mi.gdt.qq.com, sdk.e.qq.com
百度: mobads.baidu.com, cpro.baidu.com

### iOS WebContentFilter限制（2026-02研究）

- `com.apple.webcontent-filter` payload 需要Supervised设备，个人iPhone不支持
- Safari Content Blocker 必须通过App Store安装独立App
- DNS Proxy payload 需要配套App Bundle ID
- 全局HTTP代理 同样需要Supervised
- **结论：mobileconfig无法嵌入浏览器扩展或内容过滤器**

### 推荐App配合

| App | 功能 | 价格 |
|-----|------|------|
| AdGuard iOS | Safari屏蔽+DNS过滤+内置YouTube播放器 | 免费基础/RM29.90高级 |
| 1Blocker | Safari内容屏蔽 | 免费基础 |
| Brave Browser | 内置广告屏蔽浏览器 | 免费 |

## Guidelines

- 默认用AdGuard Default（不是Family），避免屏蔽成人网站
- mobileconfig必须包含IPv4+IPv6双栈+DoH加密
- YouTube视频广告无法DNS屏蔽，推荐AdGuard iOS App
- CDN加速优先：马来西亚→Cloudflare+阿里DNS，中国大陆→腾讯DNSPod+阿里DNS
- 描述文件名称格式：emoji+功能名 oskris.com（如：🛡️全屏蔽+⚡️全加速）
- 配置文件统一存 `projects/dns-profiles/`
- 一个描述文件可包含多个DNS payload，用户在设置中切换选择
