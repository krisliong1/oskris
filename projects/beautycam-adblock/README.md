# 美颜相机 BeautyCam 广告屏蔽

## 文件列表

### 配置描述文件 (.mobileconfig)
| 文件 | 说明 |
|------|------|
| `configs/beautycam-adblock-multi.mobileconfig` | **推荐** 包含4个DNS选项，可多选，和小白签效果一样 |
| `configs/beautycam-adblock-adguard.mobileconfig` | 单DNS版 AdGuard DNS 广告屏蔽 |
| `configs/beautycam-alidns.mobileconfig` | 阿里DNS加速版（中国/东南亚优化） |

### 文档
| 文件 | 说明 |
|------|------|
| `docs/README-beautycam-adblock.md` | 完整方案说明、广告域名列表、安装教程 |

## 安装方法
1. 用 iPhone Safari 打开 .mobileconfig 文件
2. 允许下载 → 设置 → 通用 → VPN、DNS与设备管理 → 安装
3. 设置 → 通用 → DNS → 勾选启用

## 屏蔽的广告域名
美图自有: ad.meitu.com, ads.meitu.com, track.meitu.com 等  
穿山甲: ad.toutiao.com, ad.oceanengine.com 等  
广点通: mi.gdt.qq.com, sdk.e.qq.com 等  
百度: mobads.baidu.com 等  

详见 `docs/README-beautycam-adblock.md`

---
**日期:** 2026-02-17  
**制作:** Oskris
