# Skills 重组计划

## 目标
- 按功能类型分类
- 便于查找和调用
- 保持 skills 之间的关联性

## 新结构

### 1. 📄 documents/ - 文档处理类
**用途**: 创建、编辑、转换各类文档
- docx (Word 文档)
- pdf (PDF 处理)
- pptx (演示文稿)
- xlsx (表格处理)

### 2. 🌐 web-development/ - 网页开发类
**用途**: 网站设计和开发
- frontend-design (前端设计)
- frontend-builder (前端构建) 
- web-artifacts-builder (Web artifacts)

### 3. 🎨 design-creative/ - 设计创意类
**用途**: 视觉设计和创意内容
- canvas-design (画布设计)
- algorithmic-art (算法艺术)
- brand-guidelines (品牌指南)
- theme-factory (主题工厂)
- slack-gif-creator (GIF 创建)

### 4. 💼 business-workflow/ - 业务工作流类
**用途**: 项目管理和业务流程
- project-workflow (项目工作流)
- requirements-analyst (需求分析)
- design-consultant (设计咨询)
- internal-comms (内部沟通)
- benepass-reimbursement (报销处理)

### 5. 🛠️ development-tools/ - 开发工具类
**用途**: 开发辅助工具
- mcp-builder (MCP 构建)
- skill-creator (Skill 创建器)
- doc-coauthoring (文档协作)

### 6. 🧠 ai-automation/ - AI 自动化类
**用途**: 智能自动化和记忆管理
- smart-info-manager (智能信息管理)
- work-rules (工作规则)

### 7. 📚 knowledge/ - 知识库类
**用途**: 产品和知识管理
- product-self-knowledge (产品知识)

## Skill 跨类别使用

某些 skills 可以被多个类别使用:

- **frontend-design** 可以用于:
  - web-development (主要用途)
  - design-creative (设计参考)
  
- **theme-factory** 可以用于:
  - design-creative (主要用途)
  - documents (文档主题)
  - web-development (网站主题)

- **smart-info-manager** 可以用于:
  - ai-automation (主要用途)
  - 所有其他类别(记录工作内容)

## 实现方式

1. **保持原有结构** - 不破坏现有的 claude-skills/
2. **创建新分类目录** - 在 skills/ 下按类型组织
3. **使用符号链接** - 让 skills 可以出现在多个分类中
4. **添加索引文件** - 每个分类目录有 README 说明

## 目录结构示例

```
skills/
├── README.md                    # 总体说明
├── documents/
│   ├── README.md               # 文档类 skills 说明
│   ├── docx/                   # 实际 skill
│   ├── pdf/
│   ├── pptx/
│   └── xlsx/
├── web-development/
│   ├── README.md
│   ├── frontend-design/
│   ├── frontend-builder/
│   └── web-artifacts-builder/
├── design-creative/
│   ├── README.md
│   ├── canvas-design/
│   ├── algorithmic-art/
│   └── ...
└── ...
```

## Claude 调用方式

```bash
# 方式 1: 直接调用
/mnt/skills/user/documents/docx/SKILL.md

# 方式 2: 通过类别查找
ls /mnt/skills/user/web-development/

# 方式 3: 搜索功能
find /mnt/skills/user/ -name "frontend*"
```
