# Claude Skills 完整汇总
*生成日期: 2026-02-14*

本文档包含了当前系统中所有可用的 Claude 技能的完整信息。

---

## 📚 目录

### 公共技能 (Public Skills) - 6个
1. [docx](#1-docx) - Word文档处理
2. [pdf](#2-pdf) - PDF文件处理
3. [pptx](#3-pptx) - PowerPoint演示文稿
4. [xlsx](#4-xlsx) - Excel电子表格
5. [frontend-design](#5-frontend-design) - 前端设计
6. [product-self-knowledge](#6-product-self-knowledge) - Anthropic产品知识

### 示例技能 (Example Skills) - 11个
7. [algorithmic-art](#7-algorithmic-art) - 算法艺术
8. [benepass-reimbursement](#8-benepass-reimbursement) - Benepass报销
9. [brand-guidelines](#9-brand-guidelines) - 品牌指南
10. [canvas-design](#10-canvas-design) - 画布设计
11. [doc-coauthoring](#11-doc-coauthoring) - 文档协作
12. [internal-comms](#12-internal-comms) - 内部沟通
13. [mcp-builder](#13-mcp-builder) - MCP服务器构建
14. [skill-creator](#14-skill-creator) - 技能创建器
15. [slack-gif-creator](#15-slack-gif-creator) - Slack GIF创建
16. [theme-factory](#16-theme-factory) - 主题工厂
17. [web-artifacts-builder](#17-web-artifacts-builder) - Web组件构建器

---

## 公共技能详解

### 1. docx
**路径**: `/mnt/skills/public/docx/SKILL.md`

**描述**: Word文档的创建、读取、编辑和操作

**主要功能**:
- 创建新的Word文档（使用docx-js库）
- 编辑现有文档（解包→编辑XML→重新打包）
- 读取和分析文档内容
- 添加跟踪更改和评论
- 插入图片、表格、目录等
- 转换.doc到.docx格式

**关键工具**:
- `pandoc` - 文本提取
- `docx-js` (npm) - 创建新文档
- `python scripts/office/unpack.py` - 解包XML
- `python scripts/office/pack.py` - 重新打包
- LibreOffice - PDF转换

**重要规则**:
- 永远不要使用Unicode子弹符号，使用`LevelFormat.BULLET`
- 表格需要双重宽度设置
- 使用美国Letter纸张（12240 x 15840 DXA）
- 使用智能引号的XML实体

---

### 2. pdf
**路径**: `/mnt/skills/public/pdf/SKILL.md`

**描述**: PDF文件的所有操作

**主要功能**:
- 读取和提取文本/表格
- 合并和分割PDF
- 旋转页面
- 添加水印
- 创建新的PDF
- 填写PDF表单
- 加密/解密PDF
- 提取图片
- OCR扫描的PDF

**关键库**:
- `pypdf` - 基本操作（合并、分割、旋转）
- `pdfplumber` - 文本和表格提取
- `reportlab` - 创建PDF
- `pytesseract` - OCR功能
- `qpdf` - 命令行工具

**重要提示**:
- 不要在ReportLab中使用Unicode上标/下标字符
- 使用`<sub>`和`<super>`标签

---

### 3. pptx
**路径**: `/mnt/skills/public/pptx/SKILL.md`

**描述**: PowerPoint演示文稿的创建和编辑

**主要功能**:
- 从头创建幻灯片
- 编辑现有演示文稿
- 读取和提取内容
- 应用主题和模板
- 添加演讲者备注和评论

**工作流程**:
1. **读取内容**: `python -m markitdown presentation.pptx`
2. **编辑**: 解包→操作幻灯片→编辑内容→清理→打包
3. **从头创建**: 使用pptxgenjs

**设计原则**:
- 选择大胆的主题调色板
- 每张幻灯片需要视觉元素
- 不要创建无聊的幻灯片
- 使用有趣的字体配对
- 避免AI常见的设计模式

**QA流程**:
- 内容QA：检查缺失内容、拼写错误
- 视觉QA：使用子代理检查重叠元素、文本溢出等
- 转换为图片进行检查

---

### 4. xlsx
**路径**: `/mnt/skills/public/xlsx/SKILL.md`

**描述**: Excel电子表格处理

**主要功能**:
- 创建和编辑Excel文件
- 数据分析（pandas）
- 公式和格式化（openpyxl）
- 清理混乱的表格数据
- 财务模型构建

**关键要求**:
- **零公式错误** - 必须零#REF!、#DIV/0!等错误
- **使用公式而非硬编码值**
- **颜色编码标准**:
  - 蓝色：硬编码输入
  - 黑色：所有公式
  - 绿色：工作表内链接
  - 红色：外部链接
  - 黄色背景：关键假设

**工作流程**:
1. 选择工具（pandas用于数据，openpyxl用于公式）
2. 创建/加载工作簿
3. 修改数据
4. 保存
5. **必须**: 重新计算公式 `python scripts/recalc.py output.xlsx`
6. 验证和修复错误

**重要库**:
- `pandas` - 数据分析
- `openpyxl` - 公式和格式化
- LibreOffice - 公式重新计算

---

### 5. frontend-design
**路径**: `/mnt/skills/public/frontend-design/SKILL.md`

**描述**: 创建独特的、生产级的前端界面

**核心原则**:
- 避免通用的AI美学
- 选择大胆的美学方向
- 实施精确的设计

**设计思考**:
- **目的**: 界面解决什么问题？
- **基调**: 极简/最大主义/复古未来/有机等
- **差异化**: 什么使其令人难忘？

**重点领域**:
- **排版**: 选择美丽、独特、有趣的字体
- **颜色和主题**: 提交到一个连贯的美学
- **动效**: 使用动画进行效果和微交互
- **空间构图**: 意外的布局、不对称、重叠
- **背景和视觉细节**: 创造氛围和深度

**避免**:
- 过度使用的字体（Inter、Roboto、Arial）
- 陈词滥调的配色方案（特别是紫色渐变）
- 可预测的布局和组件模式
- 千篇一律的设计

---

### 6. product-self-knowledge
**路径**: `/mnt/skills/public/product-self-knowledge/SKILL.md`

**描述**: Anthropic产品的准确知识

**覆盖范围**:
- **Claude Code**: 安装、配置、MCP服务器集成
- **Claude API**: 函数调用、批处理、SDK、定价、模型
- **Claude.ai**: Pro vs Team vs Enterprise计划

**核心原则**:
1. 准确性优先于猜测
2. 区分产品
3. 所有内容都要有来源
4. 首先使用正确的资源

**问题路由**:
- **Claude API/Code**: 先检查文档地图
- **Claude.ai**: 浏览支持页面

**快速参考**:
- Claude API文档: https://docs.claude.com/en/api/overview
- Claude Code文档: https://docs.claude.com/en/docs/claude-code/overview
- Claude.ai支持: https://support.claude.com

---

## 示例技能详解

### 7. algorithmic-art
**路径**: `/mnt/skills/examples/algorithmic-art/SKILL.md`

**描述**: 使用p5.js创建算法艺术

**核心概念**:
- 计算美学运动
- 种子随机性
- 交互式参数探索

**工作流程**:
1. 创建算法哲学（.md文件）
2. 通过p5.js表达（.html + .js文件）

**输出**:
- .md文件（哲学）
- .html文件（交互查看器）
- .js文件（生成算法）

**关键元素**:
- 计算过程、涌现行为
- 种子随机性、噪声场
- 粒子、流场、力场

---

### 8. benepass-reimbursement
**路径**: `/mnt/skills/examples/benepass-reimbursement/SKILL.md`

**描述**: 通过Benepass提交费用报销

**功能**:
- 自动化Benepass报销流程
- 从登录到提交的完整流程
- Gmail集成获取验证码
- 收据上传

**先决条件**:
- 启用浏览器访问（计算机工具）
- 启用代码执行和文件创建
- 配置Gmail MCP
- 获取收据图片

---

### 9. brand-guidelines
**路径**: `/mnt/skills/examples/brand-guidelines/SKILL.md`

**描述**: 应用Anthropic的官方品牌颜色和排版

**用途**:
- 品牌颜色
- 视觉识别
- 企业身份
- 排版标准

**何时使用**:
- 品牌颜色或风格指南
- 视觉格式化
- 公司设计标准

---

### 10. canvas-design
**路径**: `/mnt/skills/examples/canvas-design/SKILL.md`

**描述**: 创建美丽的视觉艺术（.png和.pdf）

**工作流程**:
1. 设计哲学创建（.md文件）
2. 通过在画布上创建来表达（.pdf或.png文件）

**输出**:
- .md文件
- .pdf文件
- .png文件

**设计元素**:
- 形式、空间、颜色、构图
- 图像、图形、形状、图案
- 最小文本作为视觉重点

**注意**: 创建原创视觉设计，避免复制现有艺术家的作品

---

### 11. doc-coauthoring
**路径**: `/mnt/skills/examples/doc-coauthoring/SKILL.md`

**描述**: 结构化的文档协作工作流程

**三个阶段**:
1. **上下文收集**: 用户提供相关上下文
2. **改进和结构**: 迭代改进内容
3. **读者测试**: 验证文档对读者有效

**何时使用**:
- 编写文档、提案、技术规范
- 创建决策文档、RFC
- 开始实质性写作任务

**文档类型**:
- PRD（产品需求文档）
- 设计文档
- 决策文档
- RFC（征求意见稿）

---

### 12. internal-comms
**路径**: `/mnt/skills/examples/internal-comms/SKILL.md`

**描述**: 编写各种内部沟通

**涵盖类型**:
- 3P更新（进展、计划、问题）
- 公司通讯
- FAQ回应
- 状态报告
- 领导层更新
- 项目更新
- 事件报告

**何时使用**:
被要求编写任何形式的内部沟通时

---

### 13. mcp-builder
**路径**: `/mnt/skills/examples/mcp-builder/SKILL.md`

**描述**: 创建高质量的MCP服务器

**概述**:
- 使LLM能够通过工具与外部服务交互
- 支持Python（FastMCP）和Node/TypeScript（MCP SDK）

**四个主要阶段**:
1. 设计
2. 实施
3. 测试
4. 优化

**质量标准**:
通过MCP服务器使LLM能够完成实际任务的能力来衡量

---

### 14. skill-creator
**路径**: `/mnt/skills/examples/skill-creator/SKILL.md`

**描述**: 创建新技能和改进现有技能

**功能**:
- 从头创建技能
- 更新或优化现有技能
- 运行评估测试技能
- 基准测试技能性能

**高级流程**:
1. 决定技能应该做什么
2. 编写技能草稿
3. 创建测试提示
4. 评估结果
5. 根据反馈重写技能
6. 重复直到满意
7. 扩展测试集

---

### 15. slack-gif-creator
**路径**: `/mnt/skills/examples/slack-gif-creator/SKILL.md`

**描述**: 为Slack创建优化的动画GIF

**Slack要求**:
- **表情GIF**: 128x128（推荐）
- **消息GIF**: 480x480
- **FPS**: 10-30（较低=较小文件）
- **颜色**: 48-128（较少=较小文件）
- **时长**: 表情GIF保持在3秒以下

**何时使用**:
用户请求为Slack创建动画GIF时

---

### 16. theme-factory
**路径**: `/mnt/skills/examples/theme-factory/SKILL.md`

**描述**: 为文档应用主题样式

**功能**:
- 10个预设主题
- 可以动态生成新主题
- 应用于幻灯片、文档、HTML页面等

**每个主题包括**:
- 连贯的调色板（十六进制代码）
- 互补的字体配对（标题和正文）
- 适合不同上下文和受众的独特视觉识别

**可应用于**:
- 演示幻灯片
- 文档
- 报告
- HTML落地页

---

### 17. web-artifacts-builder
**路径**: `/mnt/skills/examples/web-artifacts-builder/SKILL.md`

**描述**: 创建复杂的多组件Web组件

**技术栈**:
- React 18 + TypeScript
- Vite + Parcel（打包）
- Tailwind CSS
- shadcn/ui

**工作流程**:
1. 使用`scripts/init-artifact.sh`初始化前端仓库
2. 编辑生成的代码开发组件
3. 使用`scripts/bundle-artifact.sh`打包成单个HTML文件
4. 向用户显示组件
5. （可选）测试组件

**何时使用**:
- 复杂组件需要状态管理
- 需要路由
- 需要shadcn/ui组件
- **不适用于**简单的单文件HTML/JSX组件

**设计指南**:
避免"AI废话"：
- 不要过度使用居中布局
- 不要使用紫色渐变
- 不要使用统一的圆角
- 不要使用Inter字体

---

## 📊 技能统计

- **总技能数**: 17个
- **公共技能**: 6个（核心基础功能）
- **示例技能**: 11个（高级专业功能）
- **用户技能**: 0个（当前系统中没有）

---

## 🔍 技能使用建议

### 何时使用公共技能:
- 处理常见文件格式（docx, pdf, pptx, xlsx）
- 创建前端界面
- 查询Anthropic产品信息

### 何时使用示例技能:
- 创建艺术和设计作品
- 构建复杂的Web应用
- 自动化工作流程
- 开发MCP服务器
- 应用品牌标准

---

## 📝 重要提示

1. **所有技能都是完全可用的** - "示例技能"不是演示或模板，它们是完全功能性的生产级工具

2. **技能可以组合使用** - 例如，可以使用docx技能创建文档，然后使用theme-factory应用主题

3. **始终阅读SKILL.md** - 在使用任何技能之前，应先读取相应的SKILL.md文件以了解最佳实践

4. **质量保证很重要** - 特别是对于pptx和xlsx，始终进行验证和QA步骤

5. **使用正确的工具** - 根据任务选择最合适的技能和库

---

## 🚀 快速开始指南

### 创建Word文档:
```bash
# 读取docx技能
view /mnt/skills/public/docx/SKILL.md
# 然后使用docx-js创建文档
```

### 处理PDF:
```bash
# 读取pdf技能
view /mnt/skills/public/pdf/SKILL.md
# 使用pypdf、pdfplumber或reportlab
```

### 创建演示文稿:
```bash
# 读取pptx技能
view /mnt/skills/public/pptx/SKILL.md
# 使用pptxgenjs或编辑现有模板
```

### 处理电子表格:
```bash
# 读取xlsx技能
view /mnt/skills/public/xlsx/SKILL.md
# 使用pandas或openpyxl
```

---

*本文档由Claude生成，包含截至2026-02-14的所有可用技能信息。*
