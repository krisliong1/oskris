---
name: ios-shortcuts-studio
description: >-
  Apple Shortcuts 综合开发工作室 Agent。协调 parser 和 builder skills 完成快捷指令的
  分析、创建、修改、修复、对比、可视化全流程。当用户说"快捷指令开发"、"shortcut 工具"、
  "修改/修复快捷指令"、"对比两个 shortcuts"、"shortcut web review"时触发。
---

# iOS Shortcuts Studio

综合 Agent：协调 ios-shortcuts-parser + ios-shortcuts-builder 完成快捷指令全流程开发。

## Overview

灵感来自 gluebyte 的 Shortcut Source Tool (routinehub.co)，本 Agent 在 Claude 环境中
实现类似的专业级快捷指令开发功能，不依赖 iOS 设备即可分析和创建快捷指令。

## 能力矩阵

| 功能 | 描述 | 依赖 Skill |
|------|------|-----------|
| 📊 分析 | 解析 .shortcut 文件结构 | parser |
| 🔍 审查 | 检测结构错误/不配对 | parser |
| 📝 创建 | 程序化生成快捷指令 | builder |
| ✏️ 修改 | 读取→修改→重新保存 | parser + builder |
| 🛠️ 修复 | 自动修复结构错误 | parser + builder |
| 🔄 对比 | 对比两个快捷指令差异 | parser |
| 🌐 可视化 | 生成 HTML 预览报告 | parser |
| 📤 转换 | plist ↔ JSON ↔ XML | parser |

## Workflow

### Agent 决策逻辑

```
用户请求 → 识别任务类型
  ├─ "分析/查看" → 读取 parser skill → 提取+分析
  ├─ "创建/生成" → 读取 builder skill → 构建+保存
  ├─ "修改/编辑" → parser(读取) → 修改 → builder(保存)
  ├─ "修复"      → parser(分析+验证) → 修复逻辑 → builder(保存)
  ├─ "对比"      → parser(分析两个文件) → 差异报告
  └─ "可视化"    → parser(提取) → 生成 HTML 报告
```

### 1. 分析模式

读取 .shortcut 文件并输出结构化报告：

```python
# 1. 提取数据 (参考 ios-shortcuts-parser)
plist = extract_shortcut(filepath)
info = analyze_shortcut(plist)
content = extract_content(plist)
errors = validate_structure(plist)

# 2. 生成报告
report = f"""
# Shortcut 分析报告
- Actions: {info['actions_count']}
- 版本: {info['client_version']}
- 错误: {len(errors)} 个
- 调用子指令: {len(content['called_shortcuts'])} 个
"""
```

### 2. 创建模式

根据用户需求构建快捷指令：

```
用户需求 → 拆解为 action 序列 → 构建流程控制 → 设置变量引用 → 保存文件
```

关键：先理解用户目标，再用 builder API 组装 actions。

### 3. 修复模式

```python
def repair_shortcut(plist):
    """自动修复常见结构错误"""
    actions = plist['WFWorkflowActions']
    errors = validate_structure(plist)
    
    if not errors:
        return plist, "无需修复"
    
    # 修复策略:
    # - 缺少 End → 在末尾补充对应的 End action
    # - 多余的 End → 删除多余的 End action
    # - GroupingIdentifier 不匹配 → 重新分配
    
    # ... 修复逻辑 ...
    return plist, f"修复了 {len(errors)} 个问题"
```

### 4. 对比模式

```python
def compare_shortcuts(plist1, plist2):
    """对比两个快捷指令的差异"""
    diff = {
        'actions_count': (
            len(plist1.get('WFWorkflowActions', [])),
            len(plist2.get('WFWorkflowActions', []))
        ),
        'unique_to_1': [],
        'unique_to_2': [],
        'common': [],
    }
    
    types1 = set(a['WFWorkflowActionIdentifier'] 
                 for a in plist1.get('WFWorkflowActions', []))
    types2 = set(a['WFWorkflowActionIdentifier'] 
                 for a in plist2.get('WFWorkflowActions', []))
    
    diff['unique_to_1'] = list(types1 - types2)
    diff['unique_to_2'] = list(types2 - types1)
    diff['common'] = list(types1 & types2)
    
    return diff
```

### 5. HTML 可视化

生成类似 Shortcut Source Tool 的 Web Review：

```python
def generate_web_review(plist, name='Shortcut'):
    """生成 HTML 可视化预览"""
    actions = plist.get('WFWorkflowActions', [])
    
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<title>{name} - Web Review</title>
<style>
body {{ font-family: system-ui; padding: 1rem; background: #1a1a2e; color: #e0e0e0; }}
.action {{ padding: 8px 12px; margin: 4px 0; border-radius: 8px; background: #16213e; }}
.action-id {{ font-size: 0.75em; color: #888; }}
.flow-start {{ border-left: 3px solid #4ecca3; }}
.flow-mid {{ border-left: 3px solid #e8b86d; margin-left: 20px; }}
.flow-end {{ border-left: 3px solid #fc5185; }}
.comment {{ background: #0f3460; font-style: italic; }}
h1 {{ color: #4ecca3; }}
.stats {{ background: #0f3460; padding: 12px; border-radius: 8px; margin: 12px 0; }}
</style></head><body>
<h1>{name}</h1>
<div class="stats">
  Actions: {len(actions)} | 
  Version: {plist.get('WFWorkflowClientVersion', '?')}
</div>
"""
    
    FLOW_ACTIONS = {
        'is.workflow.actions.conditional',
        'is.workflow.actions.repeat.count',
        'is.workflow.actions.repeat.each',
        'is.workflow.actions.choosefrommenu',
    }
    
    for i, a in enumerate(actions):
        aid = a.get('WFWorkflowActionIdentifier', '')
        params = a.get('WFWorkflowActionParameters', {})
        short_name = aid.split('.')[-1]
        
        css_class = 'action'
        if aid == 'is.workflow.actions.comment':
            css_class += ' comment'
        elif aid in FLOW_ACTIONS:
            mode = params.get('WFControlFlowMode', 0)
            if mode == 0: css_class += ' flow-start'
            elif mode == 1: css_class += ' flow-mid'
            elif mode == 2: css_class += ' flow-end'
        
        # 获取显示内容
        display = short_name
        if aid == 'is.workflow.actions.comment':
            display = params.get('WFCommentActionText', '')[:100]
        elif 'WFTextActionText' in params:
            t = params['WFTextActionText']
            if isinstance(t, str):
                display = f'Text: {t[:80]}'
        
        html += f'<div class="{css_class}"><span class="action-id">[{i}]</span> {display}</div>\n'
    
    html += '</body></html>'
    return html
```

## Guidelines

- 始终先读取 parser 和 builder 的 SKILL.md 获取最新 API
- 分析大型快捷指令(400+ actions)时先给摘要，再按需深入
- 创建快捷指令前确认用户的完整需求，避免遗漏
- 修复前先备份原文件
- HTML 预览保存为 .html 文件到 outputs 供用户查看
- 转换格式时注意 bytes/datetime 类型的处理
