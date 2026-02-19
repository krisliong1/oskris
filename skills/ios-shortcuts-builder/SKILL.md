---
name: ios-shortcuts-builder
description: >-
  程序化创建 Apple Shortcuts (.shortcut) 文件。通过 Python 生成 plist 结构，
  支持所有常用 action 类型、流程控制、变量引用、菜单构建。当用户说"创建快捷指令"、
  "生成 shortcut 文件"、"帮我写一个 iOS 快捷指令"、"make a shortcut"时触发。
---

# iOS Shortcuts Builder

程序化创建 Apple Shortcuts 的 .shortcut 文件（无需签名即可导入）。

## Overview

iOS Shortcuts 的 .shortcut 文件本质是 binary plist。未签名的 plist 文件可以通过
文件共享/AirDrop 导入到 iOS 快捷指令 app。本 skill 提供完整的 action 构建 API。

## Quick Start

```python
import plistlib, uuid

def new_shortcut():
    """创建空白快捷指令结构"""
    return {
        'WFWorkflowMinimumClientVersion': 900,
        'WFWorkflowMinimumClientVersionString': '900',
        'WFWorkflowClientVersion': '4042.0.4',
        'WFWorkflowIcon': {
            'WFWorkflowIconStartColor': 4282601983,  # 蓝色
            'WFWorkflowIconGlyphNumber': 59511,       # 魔法棒图标
        },
        'WFWorkflowInputContentItemClasses': [
            'WFStringContentItem',
            'WFGenericFileContentItem',
        ],
        'WFWorkflowImportQuestions': [],
        'WFWorkflowActions': [],
        'WFWorkflowTypes': ['NCWidget', 'WatchKit'],
    }

def save_shortcut(shortcut, filepath):
    """保存为 .shortcut 文件 (binary plist)"""
    with open(filepath, 'wb') as f:
        plistlib.dump(shortcut, f, fmt=plistlib.FMT_BINARY)
```

## Workflow

### 1. Action 构建函数

每个 action 是一个 dict，包含 `WFWorkflowActionIdentifier` 和 `WFWorkflowActionParameters`。

```python
def make_action(identifier, **params):
    """通用 action 构建器"""
    action = {'WFWorkflowActionIdentifier': identifier}
    if params:
        action['WFWorkflowActionParameters'] = params
    return action

def make_uuid():
    return str(uuid.uuid4()).upper()

# --- 基础 Actions ---

def text_action(text):
    """文本 action"""
    return make_action('is.workflow.actions.gettext',
        WFTextActionText=text)

def comment_action(text):
    """注释 action"""
    return make_action('is.workflow.actions.comment',
        WFCommentActionText=text)

def show_alert(title, message='', show_cancel=True):
    """显示提示框"""
    return make_action('is.workflow.actions.alert',
        WFAlertActionTitle=title,
        WFAlertActionMessage=message,
        WFAlertActionCancelButtonShown=show_cancel)

def ask_input(prompt, input_type='Text', default=''):
    """请求用户输入"""
    params = {
        'WFAskActionPrompt': prompt,
        'WFInputType': input_type,
    }
    if default:
        params['WFAskActionDefaultAnswer'] = default
    return make_action('is.workflow.actions.ask', **params)

def open_url(url):
    """打开 URL"""
    return make_action('is.workflow.actions.openurl',
        WFInput={'Value': {'string': url},
                 'WFSerializationType': 'WFTextTokenString'})

def url_action(url):
    """URL action"""
    return make_action('is.workflow.actions.url', WFURL=url)

def get_contents_of_url(url=None, method='GET', headers=None, body=None):
    """HTTP 请求 (Get Contents of URL)"""
    params = {}
    if url:
        params['WFURL'] = url
    if method != 'GET':
        params['WFHTTPMethod'] = method
    if headers:
        params['WFHTTPHeaders'] = {
            'Value': {
                'WFDictionaryFieldValueItems': [
                    {
                        'WFItemType': 0,
                        'WFKey': {'Value': {'string': k}, 'WFSerializationType': 'WFTextTokenString'},
                        'WFValue': {'Value': {'string': v}, 'WFSerializationType': 'WFTextTokenString'},
                    } for k, v in headers.items()
                ]
            },
            'WFSerializationType': 'WFDictionaryFieldValue',
        }
    if body:
        params['WFHTTPBodyType'] = 'Json'
        params['WFJSONValues'] = body
    return make_action('is.workflow.actions.downloadurl', **params)

# --- 变量 Actions ---

def set_variable(name):
    """设置变量"""
    return make_action('is.workflow.actions.setvariable',
        WFVariableName=name)

def get_variable(name):
    """获取变量"""
    return make_action('is.workflow.actions.getvariable',
        WFVariable={'Value': {'VariableName': name, 'Type': 'Variable'},
                     'WFSerializationType': 'WFTextTokenAttachment'})

# --- 剪贴板 ---

def copy_to_clipboard(expire_at=None, local_only=False):
    """复制到剪贴板"""
    params = {'WFLocalOnly': local_only}
    return make_action('is.workflow.actions.setclipboard', **params)

def get_clipboard():
    """获取剪贴板"""
    return make_action('is.workflow.actions.getclipboard')

# --- 文件操作 ---

def save_file(ask_where=True, dest_path=''):
    """保存文件"""
    params = {'WFAskWhereToSave': ask_where}
    if dest_path:
        params['WFFileDestinationPath'] = dest_path
    return make_action('is.workflow.actions.documentpicker.save', **params)

def quick_look():
    """Quick Look 预览"""
    return make_action('is.workflow.actions.previewdocument')

# --- 脚本 ---

def run_shell_script(script, shell='/bin/zsh', input_mode='stdin'):
    """运行 Shell 脚本"""
    return make_action('is.workflow.actions.runshellscript',
        WFShellScript=script,
        WFShell=shell,
        WFScriptInputMode=input_mode)

def stop_shortcut(output=None):
    """停止快捷指令"""
    params = {}
    if output:
        params['WFResult'] = output
    return make_action('is.workflow.actions.exit', **params)

def nothing():
    """Nothing action (占位)"""
    return make_action('is.workflow.actions.nothing')
```

### 2. 流程控制构建

流程控制 actions (if/repeat/menu) 需要共享 `GroupingIdentifier` 和正确的 `WFControlFlowMode`。

```python
def make_if_block(condition_params=None):
    """创建 If/Otherwise/End If 块
    返回 (if_action, otherwise_action, endif_action)
    """
    gid = make_uuid()
    
    if_params = {
        'GroupingIdentifier': gid,
        'WFControlFlowMode': 0,  # 开始
    }
    if condition_params:
        if_params.update(condition_params)
    
    if_action = make_action('is.workflow.actions.conditional', **if_params)
    
    otherwise = make_action('is.workflow.actions.conditional',
        GroupingIdentifier=gid,
        WFControlFlowMode=1)  # 中间
    
    endif = make_action('is.workflow.actions.conditional',
        GroupingIdentifier=gid,
        WFControlFlowMode=2)  # 结束
    
    return if_action, otherwise, endif

def make_repeat_block(count=None):
    """创建 Repeat N Times 块
    返回 (repeat_action, end_repeat_action)
    """
    gid = make_uuid()
    
    params = {
        'GroupingIdentifier': gid,
        'WFControlFlowMode': 0,
    }
    if count is not None:
        params['WFRepeatCount'] = count
    
    repeat = make_action('is.workflow.actions.repeat.count', **params)
    end_repeat = make_action('is.workflow.actions.repeat.count',
        GroupingIdentifier=gid,
        WFControlFlowMode=2)
    
    return repeat, end_repeat

def make_repeat_each_block():
    """创建 Repeat with Each 块"""
    gid = make_uuid()
    
    repeat = make_action('is.workflow.actions.repeat.each',
        GroupingIdentifier=gid,
        WFControlFlowMode=0)
    end_repeat = make_action('is.workflow.actions.repeat.each',
        GroupingIdentifier=gid,
        WFControlFlowMode=2)
    
    return repeat, end_repeat

def make_menu(prompt, items):
    """创建 Choose from Menu 块
    items: ['选项1', '选项2', ...]
    返回 (menu_start, [menu_item_actions], menu_end)
    用法: 在每个 menu_item 后面插入该选项的 actions
    """
    gid = make_uuid()
    
    menu_start = make_action('is.workflow.actions.choosefrommenu',
        GroupingIdentifier=gid,
        WFControlFlowMode=0,
        WFMenuPrompt=prompt,
        WFMenuItems=items)
    
    menu_items = []
    for item in items:
        menu_items.append(make_action('is.workflow.actions.choosefrommenu',
            GroupingIdentifier=gid,
            WFControlFlowMode=1,
            WFMenuItemTitle=item))
    
    menu_end = make_action('is.workflow.actions.choosefrommenu',
        GroupingIdentifier=gid,
        WFControlFlowMode=2)
    
    return menu_start, menu_items, menu_end
```

### 3. 变量引用 (Token String)

在文本中引用其他 action 的输出：

```python
def make_token_string(text, attachments=None):
    """创建带变量引用的文本
    text: 含 ￼ (U+FFFC) 占位符的字符串
    attachments: {'{位置, 长度}': attachment_dict}
    """
    if not attachments:
        return text
    return {
        'Value': {
            'string': text,
            'attachmentsByRange': attachments,
        },
        'WFSerializationType': 'WFTextTokenString',
    }

def make_variable_attachment(var_name):
    """引用命名变量"""
    return {
        'Type': 'Variable',
        'VariableName': var_name,
    }

def make_action_output_attachment(output_name, output_uuid):
    """引用 action 输出"""
    return {
        'Type': 'ActionOutput',
        'OutputName': output_name,
        'OutputUUID': output_uuid,
    }
```

### 4. 完整示例：创建一个快捷指令

```python
# 创建一个"获取天气"快捷指令
shortcut = new_shortcut()
shortcut['WFWorkflowIcon']['WFWorkflowIconStartColor'] = 1440408063  # 橙色

actions = shortcut['WFWorkflowActions']

# 注释
actions.append(comment_action('天气查询工具 v1.0'))

# 请求输入城市
actions.append(ask_input('请输入城市名称:', default='北京'))
actions.append(set_variable('city'))

# 调用天气 API
actions.append(url_action('https://wttr.in/'))  # 示例
actions.append(get_contents_of_url(method='GET'))

# 显示结果
actions.append(quick_look())

# 保存
save_shortcut(shortcut, '/path/to/天气查询.shortcut')
```

### 5. 图标颜色参考

```python
SHORTCUT_COLORS = {
    'red':        4282601983,
    'dark_orange': 4251333119,
    'orange':     1440408063,
    'yellow':     4294305279,
    'green':      4292093695,
    'teal':       431817727,
    'light_blue': 1440408063,
    'blue':       463140863,
    'dark_blue':  946986751,
    'purple':     2071128575,
    'dark_purple':3679049983,
    'pink':       3980825855,
    'dark_gray':  2846468607,
}
```

### 6. 导入方式

生成的 .shortcut 文件（未签名 bplist）可以通过以下方式导入 iOS：

1. **AirDrop** - 直接传送到 iPhone/iPad
2. **文件共享** - 放入 iCloud Drive，在文件 app 中点击打开
3. **shortcuts:// URL** - `shortcuts://import-shortcut?url=<file_url>&name=<name>`
4. **iCloud 链接** - 上传到 iCloud 后分享链接

## Guidelines

- 未签名的 .shortcut 文件在 iOS 16+ 导入时会提示安全警告，用户确认即可
- `WFControlFlowMode`: 0=开始(If/Repeat/Menu), 1=中间(Otherwise/MenuItem), 2=结束(EndIf/EndRepeat/EndMenu)
- 同一组流程控制 actions 必须共享相同的 `GroupingIdentifier` (UUID)
- 变量引用使用 `WFTextTokenString` 类型，文本中用 U+FFFC 作占位符
- `WFWorkflowActionParameters` 中键名因 action 不同而不同，参考 ios-shortcuts-parser skill 的 action 表
- 输出 UUID 需与目标 action 的 UUID 匹配才能正确引用
- 保存时使用 `plistlib.FMT_BINARY` 生成标准 binary plist
- 复杂快捷指令建议先用 ios-shortcuts-parser 分析现有 shortcut 作为参考模板
