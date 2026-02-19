---
name: ios-shortcuts-parser
description: >-
  解析和分析 Apple Shortcuts (.shortcut) 文件。支持 AEA1 签名格式的提取、plist 解析、
  action 分析、结构验证、Web Review 生成。当用户说"分析快捷指令"、"解析 shortcut 文件"、
  "查看快捷指令源码"、"shortcut 有多少 actions"时触发。
---

# iOS Shortcuts Parser

解析 Apple Shortcuts 的 .shortcut 文件，提取源码并分析结构。

## Overview

iOS 16+ 的 .shortcut 文件使用 AEA1 (Apple Encrypted Archive) 签名格式包裹 bplist。
本 skill 能解压提取内部 plist 数据，分析 actions 结构，检测错误，生成可视化报告。

## Quick Start

```python
import lzfse, plistlib, struct

def extract_shortcut(filepath):
    """从 AEA1 签名的 .shortcut 文件中提取 plist 数据"""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    # 验证 AEA1 magic header
    if data[:4] != b'AEA1':
        # 可能是旧版未签名 plist，直接解析
        return plistlib.loads(data)
    
    # AEA1 结构:
    # [0:4]   = "AEA1" magic
    # [4:8]   = flags (00000000)
    # [8:12]  = header size (little-endian uint32)
    # [12:12+header_size] = signing certificate bplist
    # [...] = signature + padding
    # 尾部 = LZFSE/LZVN 压缩的 shortcut bplist
    
    # 查找 LZFSE (bvx2) 或 LZVN (bvxn) 压缩块
    for marker in [b'bvxn', b'bvx2', b'bvx1']:
        pos = data.find(marker)
        if pos >= 0:
            decompressed = lzfse.decompress(data[pos:])
            # 在解压数据中找 bplist
            bp = decompressed.find(b'bplist')
            if bp >= 0:
                return plistlib.loads(decompressed[bp:])
    
    raise ValueError("无法提取 shortcut 数据")
```

## Workflow

### 1. 提取 Shortcut 数据

```python
# 安装依赖
# pip install lzfse --break-system-packages

plist = extract_shortcut('/path/to/file.shortcut')
```

### 2. 分析基本信息

```python
def analyze_shortcut(plist):
    """分析快捷指令的基本信息"""
    info = {
        'actions_count': len(plist.get('WFWorkflowActions', [])),
        'client_version': plist.get('WFWorkflowClientVersion', '?'),
        'min_version': plist.get('WFWorkflowMinimumClientVersion', 0),
        'input_types': plist.get('WFWorkflowInputContentItemClasses', []),
        'import_questions': plist.get('WFWorkflowImportQuestions', []),
        'icon': plist.get('WFWorkflowIcon', {}),
    }
    
    # 统计 action 类型
    action_types = {}
    for a in plist.get('WFWorkflowActions', []):
        aid = a.get('WFWorkflowActionIdentifier', 'unknown')
        action_types[aid] = action_types.get(aid, 0) + 1
    info['action_breakdown'] = dict(
        sorted(action_types.items(), key=lambda x: -x[1])
    )
    
    return info
```

### 3. 提取关键内容

```python
def extract_content(plist):
    """提取文本、URL、注释等关键内容"""
    content = {'texts': [], 'urls': [], 'comments': [], 'called_shortcuts': []}
    
    for i, a in enumerate(plist.get('WFWorkflowActions', [])):
        aid = a.get('WFWorkflowActionIdentifier', '')
        params = a.get('WFWorkflowActionParameters', {})
        
        # 注释
        if aid == 'is.workflow.actions.comment':
            text = params.get('WFCommentActionText', '')
            if text:
                content['comments'].append({'index': i, 'text': text})
        
        # 文本
        if 'WFTextActionText' in params:
            tv = params['WFTextActionText']
            if isinstance(tv, str):
                content['texts'].append({'index': i, 'text': tv[:500]})
            elif isinstance(tv, dict):
                s = tv.get('Value', {}).get('string', '')
                if s:
                    content['texts'].append({'index': i, 'template': s[:500]})
        
        # URL
        if 'WFURL' in params:
            url = params['WFURL']
            if isinstance(url, str):
                content['urls'].append({'index': i, 'url': url})
        
        # 调用的子快捷指令
        if 'WFWorkflowName' in params:
            wname = params['WFWorkflowName']
            if isinstance(wname, str):
                content['called_shortcuts'].append({'index': i, 'name': wname})
    
    return content
```

### 4. 验证结构完整性

```python
def validate_structure(plist):
    """检测 if/repeat/menu 的配对完整性"""
    FLOW_ACTIONS = {
        'is.workflow.actions.conditional': ['If', 'Otherwise', 'End If'],
        'is.workflow.actions.repeat.count': ['Repeat', '', 'End Repeat'],
        'is.workflow.actions.repeat.each': ['Repeat with Each', '', 'End Repeat'],
        'is.workflow.actions.choosefrommenu': ['Choose from Menu', 'Menu Item', 'End Menu'],
    }
    
    errors = []
    stack = []
    
    for i, a in enumerate(plist.get('WFWorkflowActions', [])):
        aid = a.get('WFWorkflowActionIdentifier', '')
        if aid not in FLOW_ACTIONS:
            continue
        
        params = a.get('WFWorkflowActionParameters', {})
        flow_mode = params.get('WFControlFlowMode', 0)
        gid = params.get('GroupingIdentifier', '')
        
        if flow_mode == 0:  # 开始
            stack.append({'id': aid, 'gid': gid, 'index': i})
        elif flow_mode == 2:  # 结束
            if stack and stack[-1]['gid'] == gid:
                stack.pop()
            else:
                errors.append(f'[{i}] 不匹配的 End: {FLOW_ACTIONS[aid][2]}')
    
    for item in stack:
        errors.append(f'[{item["index"]}] 缺少 End: {FLOW_ACTIONS[item["id"]][0]}')
    
    return errors
```

### 5. 导出格式

```python
def export_as_xml(plist, output_path):
    """导出为 XML plist"""
    with open(output_path, 'wb') as f:
        plistlib.dump(plist, f, fmt=plistlib.FMT_XML)

def export_as_json(plist, output_path):
    """导出为 JSON (需处理 bytes 类型)"""
    import json, base64
    
    def default_handler(obj):
        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode()
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        raise TypeError(f'Not serializable: {type(obj)}')
    
    with open(output_path, 'w') as f:
        json.dump(plist, f, indent=2, default=default_handler, ensure_ascii=False)
```

## Guidelines

- `.shortcut` 文件有两种格式：旧版直接 bplist，新版 AEA1 签名格式
- AEA1 格式的压缩块在文件尾部，用 LZFSE (bvx2) 或 LZVN (bvxn)
- 需要 `pip install lzfse --break-system-packages`
- plist 中 bytes 类型数据（如图标）导出 JSON 时需 base64 编码
- `WFControlFlowMode`: 0=开始, 1=中间(Otherwise/Menu Item), 2=结束
- `GroupingIdentifier` 用于配对同一组的 if/repeat/menu
- Action 参数中的 `WFTextTokenString` 类型含有变量引用（￼占位符）

## 常用 Action ID 参考

| Action ID | 名称 |
|-----------|------|
| is.workflow.actions.conditional | If/Otherwise/End If |
| is.workflow.actions.repeat.count | Repeat N Times |
| is.workflow.actions.repeat.each | Repeat with Each |
| is.workflow.actions.choosefrommenu | Choose from Menu |
| is.workflow.actions.gettext | Text |
| is.workflow.actions.comment | Comment |
| is.workflow.actions.runworkflow | Run Shortcut |
| is.workflow.actions.downloadurl | Get Contents of URL |
| is.workflow.actions.setvariable | Set Variable |
| is.workflow.actions.getvariable | Get Variable |
| is.workflow.actions.dictionary | Dictionary |
| is.workflow.actions.getvalueforkey | Get Dictionary Value |
| is.workflow.actions.setvalueforkey | Set Dictionary Value |
| is.workflow.actions.alert | Show Alert |
| is.workflow.actions.ask | Ask for Input |
| is.workflow.actions.choosefromlist | Choose from List |
| is.workflow.actions.runshellscript | Run Shell Script |
| is.workflow.actions.runapplescript | Run AppleScript |
| is.workflow.actions.openurl | Open URL |
| is.workflow.actions.setclipboard | Copy to Clipboard |
| is.workflow.actions.getclipboard | Get Clipboard |
| is.workflow.actions.base64encode | Base64 Encode/Decode |
| is.workflow.actions.text.replace | Replace Text |
| is.workflow.actions.text.match | Match Text |
| is.workflow.actions.filter.files | Filter Files |
| is.workflow.actions.getmyworkflows | Get My Shortcuts |
| is.workflow.actions.documentpicker.save | Save File |
| is.workflow.actions.previewdocument | Quick Look |
| is.workflow.actions.exit | Stop Shortcut |
| is.workflow.actions.nothing | Nothing |
| is.workflow.actions.showwebpage | Show Web Page |
