# Website Quality Automation Skill

自动化网站质量检测和Awwwards标准评分系统。

## 触发词

当用户说：
- "检查网站质量"
- "评分这个网站"
- "Awwwards标准评估"
- "网站质量报告"
- "对比竞品网站"

## 功能

### 1. 自动评分
基于Awwwards 7-10分标准评估网站：
```bash
~/.openclaw/ai-team/website-quality-checker/workers/score-website.sh https://example.com
```

### 2. 评分维度
- 🎨 视觉设计 /10
- ⚡ 动画交互 /10
- 📱 响应式 /10
- 🚀 性能 /10
- ✨ 细节 /10
- 📝 内容 /10

### 3. 性能检测
- Lighthouse CI
- Core Web Vitals
- 资源加载分析

### 4. 对比分析
- 和参考网站对比（Apple、Stripe等）
- 竞品质量分析
- 改进建议生成

## 使用场景

### 开发阶段
每次构建后自动检测质量

### 上线前审查
全面评估确保达到7+分

### 持续监控
定期检查线上网站质量

### 竞品分析
学习优秀网站的设计

## 集成到工作流

### P0质量提升任务
配合URGENT-QUALITY-STANDARDS.md使用：
1. Website Builder完成设计
2. Quality Checker自动评分
3. 低于7分 → 返回优化
4. 达到7+分 → 批准上线

### CI/CD集成
```yaml
# .github/workflows/quality-check.yml
- name: Website Quality Check
  run: |
    score=$(~/.openclaw/ai-team/website-quality-checker/workers/score-website.sh $DEPLOY_URL)
    if [ $score -lt 42 ]; then
      echo "质量不达标（低于7分）"
      exit 1
    fi
```

## 技术栈

- **Lighthouse** - 性能检测
- **Puppeteer** - 自动化浏览器
- **axe-core** - 无障碍性审计
- **AI图像分析** - 视觉设计评估

## 报告输出

生成markdown报告：
```
~/.openclaw/ai-team/website-quality-checker/reports/
  └── report-20260222-062800.md
```

包含：
- 详细评分
- 截图对比
- 改进建议
- 优先级排序

## 目标

确保所有Oskris网站达到**Awwwards 7+分**标准！

## 相关AI

- Website Builder - 设计和实现
- Quality Inspector - 人工审查
- Code Reviewer - 代码质量
- Website Quality Checker - 自动评分（本skill）

## 创建日期

2026-02-22

## 状态

✅ 可用（基础版本）  
🔄 持续改进中
