---
name: dns-adblock
description: DNS广告屏蔽技能。收集各App/平台的广告域名，生成mobileconfig/hosts/AdGuard/Surge等格式屏蔽规则。当用户要屏蔽广告、制作DNS配置、查找广告域名时触发。包含YouTube SSAI机制研究和CDN加速方案。
---

# DNS 广告屏蔽

## Overview

收集、整理App和平台的广告/追踪域名，生成多种格式的屏蔽规则。配合 `ios-mobileconfig` skill 可直接生成 iOS 描述文件。

**核心认知**: DNS级别屏蔽对大多数App广告有效,但对YouTube视频广告(SSAI)无效——因为YouTube将广告注入到与视频相同的域名(googlevideo.com)中。

## Quick Start

### DNS屏蔽能力边界

| 能屏蔽 | 不能屏蔽 |
|--------|----------|
| 独立广告域名(第三方SDK) | YouTube视频内嵌广告(SSAI) |
| 网页横幅/弹窗广告 | 与内容共享域名的广告 |
| App追踪器和分析 | 加密流内的广告 |
| 恶意软件/钓鱼域名 | 服务器端拼接的广告流 |

### YouTube SSAI机制

YouTube使用Server-Side Ad Insertion(SSAI),广告在服务器端直接拼接进视频流:
- 广告和视频都通过 `*.googlevideo.com` 传输
- DNS只能解析域名,无法区分URL路径中的广告参数
- 屏蔽 googlevideo.com = 视频完全无法播放
- YouTube视频广告必须用浏览器扩展或YouTube Premium

### 推荐DNS方案

| 场景 | DNS | 效果 |
|------|-----|------|
| 全面屏蔽+家庭保护 | AdGuard Family | 最佳 |
| 标准广告屏蔽 | AdGuard Default | 好 |
| 极速+安全 | Cloudflare Family | 速度最快 |
| 威胁防护+隐私 | Quad9 | 不记录日志 |
| 亚洲CDN加速 | 阿里DNS | 东南亚最快 |

## Workflow

### DNS服务器完整列表

AdGuard Family: DoH `https://family.adguard-dns.com/dns-query` | 94.140.14.15/94.140.15.16 | IPv6 2a10:50c0::bad1:ff/2a10:50c0::bad2:ff
AdGuard Default: DoH `https://dns.adguard-dns.com/dns-query` | 94.140.14.14/94.140.15.15 | IPv6 2a10:50c0::ad1:ff/2a10:50c0::ad2:ff
Cloudflare Family: DoH `https://family.cloudflare-dns.com/dns-query` | 1.1.1.3/1.0.0.3 | IPv6 2606:4700:4700::1113/2606:4700:4700::1003
Cloudflare Security: DoH `https://security.cloudflare-dns.com/dns-query` | 1.1.1.2/1.0.0.2
Quad9: DoH `https://dns.quad9.net/dns-query` | 9.9.9.9/149.112.112.112
阿里DNS: DoH `https://dns.alidns.com/dns-query` | 223.5.5.5/223.6.6.6

### 配置文件

最新: `projects/beautycam-adblock/configs/oskris-adblock-pro-v3.mobileconfig` (6个DNS,DoH,CDN加速,IPv4+IPv6)

### 已收集广告域名

美颜相机: ad.meitu.com, ads.meitu.com, track.meitu.com, stat.meitu.com等
穿山甲: ad.toutiao.com, ad.oceanengine.com
广点通: mi.gdt.qq.com, sdk.e.qq.com
百度: mobads.baidu.com, cpro.baidu.com

## Guidelines

- AdGuard Family DNS效果最好(过滤规则最全面)
- mobileconfig必须包含IPv4+IPv6双栈+DoH加密
- YouTube视频广告无法DNS屏蔽,需告知用户
- CDN加速考虑地理位置:马来西亚优先Cloudflare和阿里DNS
- 配置文件存 `projects/[app名]-adblock/configs/`
