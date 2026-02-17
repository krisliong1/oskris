# 美颜相机 BeautyCam 13.0.20 广告屏蔽方案

## 📋 方案说明

你看到的小白签（xb51.cn）的配置文件原理是：
- 通过 `.mobileconfig` 描述文件安装 **DNS 设置**
- 将苹果企业证书验证域名（ppq.apple.com、ocsp.apple.com 等）屏蔽
- 这样企业签名的 App 不会被撤销

**要屏蔽美颜相机广告**，我们用同样的思路：
- 安装一个 `.mobileconfig` 描述文件
- 把 DNS 指向 **AdGuard DNS**（自带广告过滤）
- AdGuard DNS 会自动屏蔽大部分广告域名

---

## 🔧 方案一：AdGuard DNS 描述文件（推荐）

### 文件：`beautycam-adblock-adguard.mobileconfig`

**功能：**
- 使用 AdGuard DNS (DNS over HTTPS) 加密 DNS
- 自动屏蔽广告、追踪器、恶意网站
- 包含美颜相机广告域名屏蔽规则

**安装步骤：**
1. 用 Safari 打开此文件（不能用其他浏览器）
2. 弹出提示"正尝试下载配置描述文件"→ 点"允许"
3. 去 设置 → 通用 → VPN、DNS与设备管理
4. 点击"已下载的描述文件" → 安装
5. 去 设置 → 通用 → VPN、DNS与设备管理 → DNS
6. 确认选中"美颜相机广告屏蔽 DNS"（蓝色勾勾）

**效果：** 和你截图中小白签的效果一样，DNS设置页面会出现新的选项。

---

## 🔧 方案二：阿里DNS加速（中国用户备选）

### 文件：`beautycam-alidns.mobileconfig`

**功能：**
- 使用阿里公共DNS (DoH)，中国/东南亚速度最快
- 加密 DNS 流量保护隐私
- 需要配合路由器端 hosts 文件或 AdGuard Home 屏蔽广告

---

## 📌 美颜相机需要屏蔽的广告域名完整列表

### 美图自有域名
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

### 第三方广告SDK域名
```
# 穿山甲(字节跳动广告)
ad.toutiao.com
ad.oceanengine.com
is.snssdk.com
pangolin-sdk-toutiao.com
sf3-fe-tos.pglstatp-toutiao.com
toblog.ctobsnssdk.com

# 广点通(腾讯广告)
mi.gdt.qq.com
sdk.e.qq.com
adsmind.gdtimg.com
pgdt.gtimg.cn
win.gdt.qq.com
v.gdt.qq.com

# 百度广告
mobads.baidu.com
mobads-logs.baidu.com
cpro.baidu.com
baidumobad.baidu.com
als.baidu.com

# 快手广告
open.e.kuaishou.com
```

---

## ⚠️ 重要说明

1. **iOS 限制**：iOS 的 `.mobileconfig` DNS 设置**只能指定 DNS 服务器**，不能像电脑 hosts 文件一样直接把单个域名指向 0.0.0.0。所以最佳方案是用 AdGuard DNS 这种自带广告过滤的 DNS 服务。

2. **小白签的原理**：小白签的配置文件是通过 DNS 屏蔽苹果证书验证服务器，它用的是**自定义DNS服务器**来实现的，不是直接在描述文件里写hosts规则。

3. **最强效果**：如果你想要**最精准的美颜相机广告屏蔽**，最佳组合是：
   - iPhone 上安装 AdGuard DNS 描述文件（方案一）
   - 路由器上配置 AdGuard Home + 添加上面所有广告域名到黑名单
   - 或者在VPS上搭建 AdGuard Home，然后描述文件指向你自己的 DNS

4. **如何获取最精确的域名列表**：
   - 用 Charles 或 Stream 抓包美颜相机的所有网络请求
   - 筛选出广告/追踪相关的域名
   - 添加到 AdGuard Home 的黑名单中

---

## 🔗 推荐资源

| 资源 | 链接 | 说明 |
|------|------|------|
| AdGuard DNS 官方 | https://adguard-dns.io/en/public-dns.html | 可直接下载官方描述文件 |
| anti-AD 规则 | https://anti-ad.net | 中文区最强广告过滤规则 |
| AdGuard Home | https://adguard.com/adguard-home/overview.html | 可以在VPS上自建DNS服务器 |
| NextDNS | https://nextdns.io | 免费自定义DNS过滤，支持自定义黑名单 |

---

**制作者：Oskris**  
**日期：2026-02-17**  
**版本：1.0**
