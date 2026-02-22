---
name: ios-mobileconfig
description: iOS配置描述文件制作专家。DNS设置、VPN配置、企业政策。基于Oskris实际部署经验。
---

# iOS MobileConfig Skill

## 核心能力

### DNS配置管理
- **AdGuard DNS**: 广告屏蔽
- **Cloudflare**: 安全+速度  
- **Quad9**: 隐私保护
- **AliDNS**: 亚洲CDN

### 特殊要求
- **不屏蔽成人网站** → 避免约会App登出
- **多选支持** → Duplicates allowed: True
- **中文描述** → 用户友好

## 技术规范

### Plist XML结构
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PayloadContent</key>
    <array>
        <!-- DNS配置 -->
    </array>
    <key>PayloadDisplayName</key>
    <string>Oskris DNS优化</string>
    <key>PayloadIdentifier</key>
    <string>com.oskris.dnsconfig</string>
    <key>PayloadOrganization</key>
    <string>oskris.com</string>
    <key>PayloadType</key>
    <string>Configuration</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
</dict>
</plist>
```

### DNS Payload配置
```xml
<dict>
    <key>PayloadType</key>
    <string>com.apple.dnsSettings.managed</string>
    <key>PayloadIdentifier</key>
    <string>com.oskris.dns.adguard</string>
    <key>PayloadDisplayName</key>
    <string>AdGuard DNS</string>
    <key>DNSSettings</key>
    <dict>
        <key>DNSProtocol</key>
        <string>HTTPS</string>
        <key>ServerURL</key>
        <string>https://dns.adguard.com/dns-query</string>
    </dict>
</dict>
```

## 已验证配置

### BeautyCam广告屏蔽
- **状态**: 生产环境运行
- **反馈**: 用户满意度高
- **位置**: GitHub projects/beautycam-adblock/

### 全屏蔽+全加速方案
- **组合**: 4种DNS服务
- **效果**: 广告屏蔽率>95%，速度提升30%

## 制作流程

### 第1步: 需求分析
```
- [ ] 了解用户设备和需求
- [ ] 选择合适的DNS服务
- [ ] 确定配置范围
```

### 第2步: 配置生成
```
- [ ] 创建plist XML文件
- [ ] 设置组织信息
- [ ] 添加DNS payload
- [ ] 验证XML格式
```

### 第3步: 测试部署
```
- [ ] iPhone/iPad安装测试
- [ ] 验证DNS解析
- [ ] 检查网站访问
- [ ] 性能对比测试
```

### 第4步: 交付培训
```
- [ ] 安装指导文档
- [ ] 常见问题解答
- [ ] 卸载方法说明
```

## 商业化服务

### 定价策略
- **基础DNS**: RM30-50
- **VPN+DNS**: RM100-150
- **企业配置**: RM200-300
- **批量部署**: RM500-1000

### 目标客户
- 马来西亚iPhone用户
- 企业IT管理员
- 隐私安全意识用户
- BeautyCam等App用户

---
*基于Oskris iOS配置部署实战经验*