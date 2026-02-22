---
name: oskris-infrastructure
description: Oskris完整基础设施管理。VPS+共享主机+域名+API管理。不包含敏感凭据，仅流程和标准。
---

# Oskris Infrastructure Management

## 服务器架构

### VPS (独立服务器)
- **Provider**: Hostinger
- **Location**: Malaysia
- **Specs**: 2核8GB Ubuntu 25.10
- **用途**: Python应用、数据库、AI服务
- **IP**: 76.13.191.45

### 共享主机 (WordPress)
- **Provider**: Hostinger 
- **用途**: oskris.com主站
- **特点**: WordPress专用环境

## 域名管理策略

### 主域名: oskris.com
- **用途**: 主业务展示
- **平台**: WordPress + 自定义
- **到期**: 2027+

### 子域名架构
- `kkh.oskris.com` → Kong Kiong Hardware
- `websitedesign.oskris.com` → 网站设计服务
- `api.oskris.com` → API服务端点

## API集成标准

### Hostinger API
- **用途**: DNS管理、VPS控制
- **认证**: Bearer token
- **端点**: developers.hostinger.com/api

### GitHub API  
- **用途**: 代码管理、自动部署
- **认证**: Personal Access Token
- **权限**: repo, workflow, admin:repo_hook

## 部署工作流

### 静态网站 (GitHub Pages)
```
1. 本地开发 → workspace/
2. Git提交 → krisliong1/项目名
3. GitHub Pages自动部署
4. DNS指向 → Hostinger
```

### Python应用 (VPS)
```
1. 本地开发 → 推送GitHub
2. VPS拉取 → git pull
3. 依赖安装 → pip install
4. 服务启动 → systemd
```

## 安全标准

### 密钥管理
- **私钥**: 仅本地和VPS，不上传GitHub
- **API Token**: 环境变量，不硬编码
- **密码**: 复杂度足够，定期轮换

### 备份策略
- **代码**: GitHub自动备份
- **数据**: VPS每日备份
- **配置**: krisliong1/private-config (Private仓库)

## 监控检查

### 健康检查清单
```
- [ ] VPS服务状态
- [ ] 域名解析正常
- [ ] SSL证书有效
- [ ] 网站加载速度
- [ ] API响应时间
```

### 故障处理
```
1. 检查服务日志
2. 重启相关服务
3. 验证网络连接
4. 联系Hostinger支持
```

---
*基于Oskris多年运维经验*