# iOS Shortcuts 深度逆向分析学习报告

最后更新: 2026-02-19
来源: 逆向分析 gluebyte 的 Shortcut Source Tool 工具链 (4个.shortcut文件)

## 核心发现

### 1. AEA1 签名文件格式

iOS 15+ 的 .shortcut 文件使用 Apple Encrypted Archive (AEA1) 签名格式：

```
[AEA1 Header - 12 bytes]
  ├── Magic: "AEA1" (4B)
  ├── Padding: 0x00000000 (4B)
  └── Cert chain offset: little-endian uint32 (4B)

[Certificate Chain - bplist]
  └── SigningCertificateChain (X.509 证书链)

[Compressed Payload]
  ├── Magic: "bvxn" (LZVN) 或 "bvx2" (LZFSE)
  ├── Decompressed size: little-endian uint32 (4B)
  ├── Compressed size: little-endian uint32 (4B)
  └── Compressed data

[Decompressed = Apple Archive Container]
  ├── "AA01" header + metadata
  ├── "Shortcut.wflow" filename
  ├── "DATA" marker
  └── bplist (实际的快捷指令数据)
```

**提取方法（Python）：**
```python
import struct, plistlib, lzfse

def extract_shortcut(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    
    if data[:4] != b'AEA1':
        return plistlib.loads(data)  # 未签名
    
    for magic in [b'bvxn', b'bvx2']:
        off = data.find(magic)
        if off < 0:
            continue
        decompressed = lzfse.decompress(data[off:])
        bp_off = decompressed.find(b'bplist')
        if bp_off >= 0:
            return plistlib.loads(decompressed[bp_off:])
    return None
```

### 2. 签名流程（关键！）

Helper 中发现了签名的具体实现：

**本地签名（macOS/iOS）：**
```bash
cd /tmp
cat > a.wflow          # stdin 接收 plist 数据
shortcuts sign -m anyone -i a.wflow -o a.shortcut
cat a.shortcut         # stdout 输出签名后的文件
```

**SSH 远程签名（通过 Mac）：**
```bash
cd /tmp
gunzip > a.wflow       # 接收 gzip 压缩的 plist
shortcuts sign -m anyone -i a.wflow -o a.shortcut
gzip -9c a.shortcut    # 输出 gzip 压缩的签名文件
```

**Cloudflare Worker 签名（备选）：**
Helper 还使用 `http://shortcuts.gluebyte.workers.dev/` 作为在线签名服务。

### 3. Plist 顶层结构

```
WFWorkflowClientVersion: "4042.0.4"  (当前版本号)
WFWorkflowMinimumClientVersion: 900
WFWorkflowMinimumClientVersionString: "900"
WFWorkflowIcon:
  WFWorkflowIconGlyphNumber: (图标编号)
  WFWorkflowIconStartColor: (颜色值)
WFWorkflowTypes: ["NCWidget", "Watch", "ActionExtension", ...]
WFWorkflowInputContentItemClasses: ["WFGenericFileContentItem", ...]
WFWorkflowOutputContentItemClasses: []
WFWorkflowImportQuestions: []
WFWorkflowHasOutputFallback: false
WFWorkflowHasShortcutInputVariables: true/false
WFQuickActionSurfaces: []
WFWorkflowActions: [action1, action2, ...]
```

### 4. 变量引用系统（三种方式）

**方式A: WFTextTokenAttachment（直接引用）**
```xml
<key>WFInput</key>
<dict>
  <key>Value</key>
  <dict>
    <key>OutputUUID</key><string>UUID</string>
    <key>OutputName</key><string>名称</string>
    <key>Type</key><string>ActionOutput</string>
  </dict>
  <key>WFSerializationType</key>
  <string>WFTextTokenAttachment</string>
</dict>
```

**方式B: WFTextTokenString（字符串内嵌变量）**
```xml
<key>WFURLActionURL</key>
<dict>
  <key>Value</key>
  <dict>
    <key>string</key><string>https://example.com/￼/path</string>
    <key>attachmentsByRange</key>
    <dict>
      <key>{20, 1}</key>
      <dict>
        <key>OutputUUID</key><string>UUID</string>
        <key>OutputName</key><string>Matches</string>
        <key>Type</key><string>ActionOutput</string>
      </dict>
    </dict>
  </dict>
  <key>WFSerializationType</key>
  <string>WFTextTokenString</string>
</dict>
```

位置 `{20, 1}` 表示字符串中第20个字符处的 U+FFFC (￼) 对应该变量。

**方式C: Named Variable（命名变量）**
```xml
<key>Type</key><string>Variable</string>
<key>VariableName</key><string>item</string>
```

### 5. 流程控制结构

**WFControlFlowMode 值：**
| 值 | 含义 |
|----|------|
| 0 | 开始（If/Menu定义/Repeat开始）|
| 1 | 中间（Else/菜单项）|
| 2 | 结束（EndIf/EndMenu/EndRepeat）|

同一个 `GroupingIdentifier` 串联整个流程块。

**WFCondition 值（已验证修正）：**
| 值 | 含义 | 验证来源 |
|----|------|---------|
| 0 | 等于 (is) | — |
| 2 | 包含 (contains) | — |
| 3 | 开头是 (begins with) | — |
| 4 | 大于 (greater than) | Helper[2]: Random Number 比较 |
| 5 | 小于等于 (is less than or equal) | — |
| 8 | 不等于 (is not) | — |
| 99 | 过滤运算符 (filter) | XML_Plist[1]: 文件过滤器 |
| 100 | 有值 (has any value) | Helper[4]: IP地址检查 |
| 101 | 没有值 (does not have any value) | Import[0]: 检查Extension输入 |
| 999 | 介于 (is between) | — |

### 6. Aggrandizements（属性访问）

用于从变量中提取特定属性：
```xml
<key>Aggrandizements</key>
<array>
  <dict>
    <key>PropertyName</key><string>Name</string>
    <key>PropertyUserInfo</key><string>WFItemName</string>
    <key>Type</key><string>WFPropertyVariableAggrandizement</string>
  </dict>
</array>
```

类型转换（Coercion）：
```xml
<dict>
  <key>CoercionItemClass</key><string>WFStringContentItem</string>
  <key>Type</key><string>WFCoercionVariableAggrandizement</string>
</dict>
```

### 7. 魔术变量类型

| Type值 | 含义 |
|--------|------|
| ActionOutput | 某个action的输出（需要OutputUUID） |
| ExtensionInput | 快捷指令的输入（从分享sheet或自动化） |
| Variable | 命名变量（通过Set Variable设置） |
| Clipboard | 剪贴板内容 |
| CurrentDate | 当前日期 |
| Ask | 运行时询问用户 |

### 8. 工具链依赖关系

```
Shortcut Source Tool (424 actions, 主IDE)
  ├── 调用: Shortcut Source Helper (通过 runworkflow)
  ├── 使用: runapplescript (关闭 ShortcutsViewService)
  ├── 使用: runshellscript (文件对比 diff)
  ├── 使用: runjavascriptforautomation (Safari操作)
  └── 使用: runjavascriptonwebpage (Web Review)

Shortcut Source Helper (97 actions, 辅助库)
  ├── 调用: Import Shortcut (通过文件操作)
  ├── 签名: shortcuts sign -m anyone (本地shell)
  ├── 签名: SSH远程签名 (runsshscript)
  ├── 签名: Cloudflare Worker (HTTP POST)
  └── 版本检查: gluebyte.workers.dev

Import Shortcut (7 actions, 导入器)
  └── 转换file链接为 workflow:// URL → openurl

Shortcut to XML Plist (11 actions, 转换器)
  └── getmyworkflows → filter → rename .plist → detect.text → preview/save
```

### 9. 已发现的61种 Action Identifier

```
核心操作: comment, gettext, number, setvariable, getvariable, nothing, exit
流程控制: conditional, choosefrommenu, repeat.count, repeat.each
文件操作: file, file.select, file.getlink, file.move, filter.files, documentpicker.open, documentpicker.save
网络: url, downloadurl, url.expand, openurl, getipaddress
文本处理: text.match, text.match.getgroup, text.replace, base64encode, urlencode
用户交互: alert, ask, choosefromlist, previewdocument, showwebpage
变量: setitemname, getitemname, gettypeaction, getvalueforkey, setvalueforkey
数据: dictionary, list, count, math, number.random, properties.files
剪贴板: getclipboard, setclipboard, share, openin
脚本: runshellscript, runapplescript, runsshscript, runjavascriptforautomation, runjavascriptonwebpage
跨快捷指令: runworkflow, getmyworkflows
压缩: makezip, unzip
延迟: delay, waittoreturn
第三方: AsheKube.app.a-Shell-mini.ExecuteCommandIntent, com.apple.mobilesafari.CreateNewPrivateTab, com.sindresorhus.Actions.SetUniformTypeIdentifier
```

### 10. Claude 生成快捷指令的完整工作流

```
1. 用户描述需求
2. Claude 生成完整 XML plist 文件
3. 保存为 .plist 文件 → /mnt/user-data/outputs/
4. 用户在 iOS 设备打开文件
5. Shortcut Source Helper 自动处理:
   a. 读取 plist 内容
   b. 转换为 binary plist (.wflow)
   c. 调用 shortcuts sign -m anyone 签名
   d. 导入到快捷指令 app
6. 快捷指令就绪 ✅
```

## 关键纠正（之前skill中的错误）

1. **WFCondition 映射完全错误** → 已用实际数据验证修正
2. **缺少 WFWorkflowClientVersion** → 当前版本应该是 `4042.0.4` 不是 `2702`
3. **缺少签名流程的详细说明** → Helper 中有完整的 shell script
4. **缺少 Aggrandizements 说明** → 属性访问和类型转换机制
5. **图标颜色值需要验证** → 从实际文件中提取的值:
   - XML_Plist: 1440408063 (橙色系)
   - Import: 2071128575 (紫色)
   - Helper/Source_Tool: -2873601 (蓝绿色)
