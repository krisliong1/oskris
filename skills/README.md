# Skills 目录

按功能类型分类的 Claude Skills 集合

## 📂 分类结构

### 📄 [documents/](documents/) - 文档处理
创建、编辑、转换各类文档
- **docx** - Word 文档处理
- **pdf** - PDF 创建和编辑
- **pptx** - 演示文稿制作
- **xlsx** - Excel 表格处理

### 🌐 [web-development/](web-development/) - 网页开发
网站设计和前端开发
- **frontend-design** - 前端界面设计
- **web-artifacts-builder** - Web artifacts 构建

### 🎨 [design-creative/](design-creative/) - 设计创意
视觉设计和创意内容生成
- **canvas-design** - 画布设计和海报
- **algorithmic-art** - 算法艺术生成
- **brand-guidelines** - 品牌指南应用
- **theme-factory** - 主题和样式工厂
- **slack-gif-creator** - Slack GIF 创建

### 💼 [business-workflow/](business-workflow/) - 业务工作流
项目管理和业务流程优化
- **internal-comms** - 内部沟通文档
- **benepass-reimbursement** - 报销流程处理
- **doc-coauthoring** - 文档协作编写

### 🛠️ [development-tools/](development-tools/) - 开发工具
开发辅助和工具构建
- **mcp-builder** - MCP 服务器构建
- **skill-creator** - Skill 创建和测试

### 🧠 [ai-automation/](ai-automation/) - AI 自动化
智能自动化和信息管理
- **smart-info-manager** - 自动记录和分类所有对话到 GitHub
- **auto-translate** - 自动识别英文并用中文回复,代码保持英文
- **app-recommendations** - 精准App推荐,默认精简模式节省token

### 📚 [knowledge/](knowledge/) - 知识库
产品知识和文档管理
- **product-self-knowledge** - 产品知识库

## 🔍 如何使用

### 查找 Skill
```bash
# 按类别浏览
ls skills/documents/
ls skills/web-development/

# 搜索特定 skill
find skills/ -name "docx"
```

### 调用 Skill
Claude 会根据任务自动选择合适的 skill,或者你可以明确指定:
```
"使用 docx skill 创建一份报告"
"用 frontend-design 设计一个登录页面"
```

## 📝 Skill 跨类别使用

某些 skills 可以在多个场景使用:
- **theme-factory**: 可用于文档、网页、设计
- **smart-info-manager**: 自动记录所有类别的工作
- **frontend-design**: 网页和设计都可用

## 🆕 添加新 Skill

新 skills 应放在最合适的分类目录中:
```bash
skills/[category]/[skill-name]/
```

## 📊 统计

- 总分类: 7 个
- 总 Skills: 19+ 个
- 最后更新: 2024-02-15

---

*由 Smart Info Manager 自动维护*
