---
name: dns-adblock
description: DNS广告屏蔽技能。收集各App/平台的广告域名，生成多种格式的屏蔽规则(hosts/AdGuard/Surge/Quantumult X/mobileconfig)。当用户要屏蔽某个App广告、查找广告域名、制作屏蔽规则时触发。
---

# DNS 广告屏蔽

## Overview

收集、整理App和平台的广告/追踪域名，生成多种格式的屏蔽规则。配合 `ios-mobileconfig` skill 可直接生成 iOS 描述文件。

## Quick Start

### 查找广告域名的方法

1. **搜索关键词**: `[App名] 广告屏蔽 域名 hosts github`
2. **抓包分析**: Charles/Stream 抓包，筛选 ad/track/log/stat 相关请求
3. **社区规则库**: anti-AD、NobyDa、ConnersHua 等开源项目
4. **APK分析**: 查看App集成了哪些广告SDK，对应查SDK域名

### 中国App常见广告SDK域名

#### 穿山甲（字节跳动广告）
```
ad.toutiao.com
ad.oceanengine.com
is.snssdk.com
pangolin-sdk-toutiao.com
sf3-fe-tos.pglstatp-toutiao.com
toblog.ctobsnssdk.com
```

#### 广点通（腾讯广告）
```
mi.gdt.qq.com
sdk.e.qq.com
adsmind.gdtimg.com
pgdt.gtimg.cn
win.gdt.qq.com
v.gdt.qq.com
```

#### 百度广告
```
mobads.baidu.com
mobads-logs.baidu.com
cpro.baidu.com
baidumobad.baidu.com
als.baidu.com
```

#### 快手广告
```
open.e.kuaishou.com
```

## Workflow

### 已收集的App广告域名

#### 美颜相机 BeautyCam (美图/Meitu)
```
ad.meitu.com
ads.meitu.com
adui.meitu.com
api-ad.meitu.com
sdk.ads.meitu.com
mdap.meitu.com
track.meitu.com
stat.meitu.com
log.meitu.com
analytics.meitu.com
push.meitu.com
msg.meitu.com
crash.meitu.com
```
配置文件: `projects/beautycam-adblock/`

### 规则格式转换

同一组域名可以输出为以下格式：

#### hosts 格式（路由器/电脑）
```
0.0.0.0 ad.example.com
```

#### AdGuard/Pi-hole 格式
```
||ad.example.com^
```

#### Surge/Shadowrocket 格式
```
DOMAIN-SUFFIX,ad.example.com,REJECT
```

#### Quantumult X 格式
```
host-suffix, ad.example.com, reject
```

#### Clash 格式
```yaml
- DOMAIN-SUFFIX,ad.example.com,REJECT
```

### 带广告过滤的公共DNS服务器

| 服务 | DoH地址 | IP | 说明 |
|------|---------|-----|------|
| AdGuard DNS | `https://dns.adguard-dns.com/dns-query` | 94.140.14.14, 94.140.15.15 | 屏蔽广告+追踪 |
| AdGuard Family | `https://family.adguard-dns.com/dns-query` | 94.140.14.15, 94.140.15.16 | +成人内容 |
| Cloudflare Security | `https://security.cloudflare-dns.com/dns-query` | 1.1.1.2, 1.0.0.2 | 屏蔽恶意软件 |
| Quad9 | `https://dns.quad9.net/dns-query` | 9.9.9.9, 149.112.112.112 | 屏蔽恶意域名 |

### 不过滤的加速DNS（配合自建AdGuard Home用）

| 服务 | DoH地址 | IP | 适合 |
|------|---------|-----|------|
| 阿里DNS | `https://dns.alidns.com/dns-query` | 223.5.5.5, 223.6.6.6 | 中国/东南亚 |
| DNSPod | `https://doh.pub/dns-query` | 119.29.29.29 | 中国 |
| Cloudflare | `https://cloudflare-dns.com/dns-query` | 1.1.1.1, 1.0.0.1 | 全球 |
| Google | `https://dns.google/dns-query` | 8.8.8.8, 8.8.4.4 | 全球 |

### 社区广告规则订阅源

| 项目 | 链接 | 说明 |
|------|------|------|
| anti-AD | `https://anti-ad.net/surge2.txt` | 中文区最强 |
| NobyDa | `github.com/NobyDa/Script` | Surge/QX脚本 |
| ConnersHua | `github.com/GoodHolidays/ConnersHua` | 多平台规则 |
| AdGuard DNS filter | 内置于AdGuard DNS | 全球广告 |

## Guidelines

- 每次为新App收集广告域名后，更新本Skill的"已收集App"段落
- 同时生成 mobileconfig + 至少一种文本格式规则
- 广告域名分两类：App自有域名 + 第三方广告SDK域名
- 配置文件存 `projects/[app名]-adblock/`
- iOS限制：mobileconfig只能指定DNS服务器，不能直接屏蔽单个域名。要精确屏蔽需用AdGuard DNS或自建AdGuard Home
