---
name: project-workflow
description: Complete project management workflow for web development projects. Use when managing client projects from initial contact to final delivery, coordinating between different phases, tracking progress, handling client communication, and ensuring timely delivery. Orchestrates all other web development skills.
---

# Project Workflow Skill

管理网站开发项目从接洽到交付的完整流程。协调所有其他skills。

## 项目生命周期

```
1. 获客 → 2. 初步咨询(requirements-analyst)
  → 3. 提案与合同 → 4. 设计阶段(design-consultant)
  → 5. 开发阶段(frontend-builder) → 6. 测试审查
  → 7. 上线部署 → 8. 培训交接 → 9. 后续支持
```

## Phase 1: 获客

**渠道**: 本地商家拜访、商业活动、老客户转介、KKH客户网络、社交媒体、WhatsApp群组
**关键**: 30分钟内响应询盘

## Phase 2: 初步咨询

调用 `requirements-analyst` skill:
- 收集业务目标和目标受众
- 了解竞争对手
- 确定项目范围和预算
- 输出: requirements.md

**首次咨询清单**:
- [ ] 业务类型和行业
- [ ] 网站目标(获客/品牌/销售)
- [ ] 目标受众
- [ ] 现有品牌资产
- [ ] 参考网站
- [ ] 预算范围
- [ ] 时间线

## Phase 3: 提案与合同

### 提案核心内容
1. **理解客户需求** — 证明你听懂了
2. **解决方案** — 网站结构+功能+设计方向
3. **时间线** — 各阶段起止时间
4. **投资** — 价格分解+付款安排
5. **为什么选择我们** — 差异化优势
6. **下一步** — 明确行动号召

### 付款安排
- 50% 签约预付
- 30% 设计稿通过后
- 20% 上线验收后

### 合同要点
- 项目范围(含什么不含什么)
- 时间线和里程碑
- 修改次数(建议含3次免费修改)
- 知识产权归属
- 域名/主机责任
- 后续维护条款

## Phase 4: 设计阶段

调用 `design-consultant` skill:
1. 品牌风格分析
2. 配色+字体方案
3. 线框图(所有页面)
4. 高保真设计稿
5. **客户确认** ← 必须获得书面确认

**时间**: 3-5个工作日
**交付**: brand-kit.md + design-spec.md + 线框图

## Phase 5: 开发阶段

调用 `frontend-builder` skill:
1. 搭建项目结构
2. 实现设计稿
3. 响应式开发
4. 功能开发(表单/支付/SEO)
5. 性能优化

**时间**: 7-14个工作日
**交付**: 可运行的网站代码

## Phase 6: 测试审查

### 测试清单
- [ ] 所有页面功能正常
- [ ] 响应式: Mobile/Tablet/Desktop
- [ ] 跨浏览器: Chrome/Safari/Firefox
- [ ] 表单提交正常
- [ ] 链接无404
- [ ] 图片加载正常
- [ ] PageSpeed ≥80
- [ ] SEO meta完整
- [ ] 无障碍基础检查

### 客户预览
- 部署到测试URL
- 发客户预览链接
- 收集反馈(限3轮修改)
- **获得客户书面确认**

## Phase 7: 上线部署

1. 域名DNS配置
2. SSL证书安装
3. 网站文件部署
4. 功能最终测试
5. Google Analytics + Search Console
6. 网站地图提交

## Phase 8: 培训交接

**交付给客户**:
- 网站管理文档(如用WordPress)
- 登录信息
- 内容更新教程
- 紧急联系方式

## Phase 9: 后续支持

- 第1个月: 免费bug修复
- 月度维护套餐: RM200-500/月
- 紧急修复: 24小时响应

## 客户沟通规则

- 使用客户熟悉的语言(中文/马来文/英文)
- 避免技术术语
- 每周进度更新(WhatsApp)
- 关键决策必须书面确认
- 24小时内回复客户消息

## 处理困难情况

**范围蔓延**: "这超出了原始范围。我们可以作为额外项目处理，费用是RM X。"
**延迟付款**: 设定付款里程碑，未付款暂停项目。
**不满意设计**: 提供3个方向选择，超过免费修改次数收费。
**紧急变更**: 评估影响，提供时间和成本估算，获得确认后执行。

## 项目管理工具

- 进度跟踪: GitHub Issues / 简单表格
- 文件存储: GitHub (krisliong1/oskris/projects/)
- 沟通: WhatsApp
- 设计: Figma / Claude直接生成

## 完整项目检查清单

- [ ] 需求文档完成
- [ ] 提案已发送+确认
- [ ] 合同已签署+预付已收
- [ ] 设计方案已确认
- [ ] 网站开发完成
- [ ] 响应式+性能测试通过
- [ ] 客户预览+确认
- [ ] 网站已上线
- [ ] 培训+交接完成
- [ ] 尾款已收
- [ ] 后续维护协议
